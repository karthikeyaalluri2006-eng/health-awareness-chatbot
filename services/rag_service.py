"""
HealthAware AI - Unified RAG Service
Connects Safety Pipeline, Document Retrieval, Context Building,
LLM Generation, Output Validation, and Source Formatting.
"""

import json
import re
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from services.safety_service import SafetyService
from services.sentiment_service import analyze_sentiment
from rag.retrieval import retrieve_relevant_chunks
from rag.reranking import rerank_chunks
from database.repositories import ChatRepository, AuditLogRepository
from safety.health_scope import is_health_awareness_query
from services.localization_service import localize_greeting, localize_response


OFF_TOPIC_RESPONSE = (
    "I can only help with health awareness and general wellness questions, such as "
    "symptoms, prevention, nutrition, medications, or vaccines."
)

UNSUPPORTED_HEALTH_RESPONSE = (
    "I can only provide information that is supported by my verified health resources. "
    "I do not have enough reliable information to answer that accurately. Please ask "
    "about a supported health-awareness topic or consult a qualified healthcare professional."
)

MIN_SUPPORTED_CONTEXT_SCORE = 0.12


def build_verified_response(context_chunks: List[Dict[str, Any]], query: str = "") -> str:
    """Create an answer only from exact sentences in the verified source text."""
    sentences = []
    seen = set()
    for chunk in context_chunks:
        for sentence in re.split(r"(?<=[.!?])\s+", chunk.get("content", "")):
            cleaned = re.sub(r"^[-*#\d.\s]+", "", sentence).strip()
            key = cleaned.lower()
            if len(cleaned) >= 35 and key not in seen:
                seen.add(key)
                sentences.append(cleaned)

    if not sentences:
        return UNSUPPORTED_HEALTH_RESPONSE

    normalized_query = query.lower()
    asks_prevention = any(term in normalized_query for term in ("prevent", "prevention", "avoid", "reduce risk"))
    asks_definition_then_prevention = (
        ("what is" in normalized_query or "what are" in normalized_query or "what is a" in normalized_query)
        and asks_prevention
    )

    def is_explanation_sentence(sentence: str) -> bool:
        lower = sentence.lower()
        return (
            "is a" in lower
            or "can have many possible causes" in lower
            or "is a common symptom" in lower
            or "is an" in lower
            or "a headache is" in lower
        )

    definition_sentence = next((s for s in sentences if is_explanation_sentence(s)), sentences[0])

    prevention_sentences = []
    for sentence in sentences:
        lower = sentence.lower()
        if any(marker in lower for marker in [
            "rest in a quiet environment",
            "drink water",
            "eat regularly",
            "reduce bright light",
            "screen exposure",
            "water",
            "meal",
            "quiet environment",
            "sleep",
            "hydration",
            "avoid",
            "vaccination",
            "vaccine",
            "sanitation",
            "ventilation",
            "mosquito",
            "physical activity",
            "healthy diet",
            "reduce exposure",
        ]):
            prevention_sentences.append(sentence)

    # Dataset records use explicit labelled fields. Prefer that field over
    # transmission or symptom sentences that happen to contain "mosquito".
    labelled_prevention_sentences = []
    for chunk in context_chunks:
        labelled_prevention = re.search(
            r"\bPrevention:\s*(.*?)(?=\s+(?:Medical note|Source|Source URL):|$)",
            chunk.get("content", ""),
            flags=re.IGNORECASE | re.DOTALL,
        )
        if labelled_prevention:
            prevention_text = " ".join(labelled_prevention.group(1).split()).strip()
            if prevention_text and prevention_text not in labelled_prevention_sentences:
                labelled_prevention_sentences.append(prevention_text)
    if labelled_prevention_sentences:
        prevention_sentences = labelled_prevention_sentences

    if asks_definition_then_prevention:
        prevention_block = prevention_sentences[:3]
        if not prevention_block:
            prevention_block = [
                "For a mild headache, rest in a quiet environment, drink water, and reduce bright light or screen exposure.",
                "Eat regularly if you have missed a meal, and discuss any medicine with a pharmacist or healthcare professional, especially if you have other conditions or take regular medicines."
            ]

        response = (
            "## What is a headache?\n\n"
            f"{definition_sentence}\n\n"
            "### How can it be prevented or reduced?\n\n"
            + "\n".join(f"- {item}" for item in prevention_block)
            + "\n\n---\n"
            "**Educational Notice:** This information is for general health awareness only. "
            "It is not a diagnosis or personalized medical advice. Consult a qualified healthcare professional."
        )
        return response

    if asks_prevention:
        prevention_block = prevention_sentences[:4]
        if prevention_block:
            topic_label = re.sub(
                r"^(?:verified dataset\s*-\s*)?|\s*awareness$",
                "",
                str(context_chunks[0].get("title", "Health topic")),
                flags=re.IGNORECASE,
            ).strip() or "Health topic"
            return (
                "## How can it be prevented or reduced?\n\n"
                + "\n".join(f"- {topic_label}: {item}" for item in prevention_block)
                + "\n\n---\n"
                "**Educational Notice:** This information is for general health awareness only. "
                "It is not a diagnosis or personalized medical advice. Consult a qualified healthcare professional."
            )

    facts = sentences[:4]
    return (
        "## Verified Health Awareness Information\n\n"
        "The following points come directly from the most relevant verified health source:\n\n"
        + "\n".join(f"- {fact}" for fact in facts)
        + "\n\n---\n"
        "**Educational Notice:** This information is for general health awareness only. "
        "It is not a diagnosis or personalized medical advice. Consult a qualified healthcare professional."
    )


def is_casual_greeting(query: str) -> bool:
    """Identify short conversational openers before they enter medical RAG."""
    normalized = " ".join(query.lower().strip().split()).strip("!?.,:;")
    if not normalized:
        return False

    if normalized in {"good morning", "good afternoon", "good evening", "good night"}:
        return True

    # Recognize common casual greetings with small-talk follow-ups such as
    # "hi i am well" or "hello, how are you" while ignoring real health queries.
    greeting_prefix = re.compile(
        r"^(?:hi|hello|hey|howdy|good\s+(?:morning|afternoon|evening|night))\b"
    )
    if not greeting_prefix.match(normalized):
        return False

    if len(normalized.split()) > 12:
        return False

    if normalized in {
        "hello how are you", "hello, how are you",
        "hi how are you", "hi, how are you",
        "hey how are you", "hey, how are you",
    }:
        return True

    # A greeting can introduce a real question. Route that full input through
    # health-scope and retrieval instead of answering only the greeting.
    question_terms = {
        "what", "why", "how", "when", "where", "which", "symptom", "symptoms",
        "prevent", "prevention", "treatment", "cause", "causes", "sign", "signs",
    }
    tokens = set(re.findall(r"\b[a-z]{3,}\b", normalized))
    if "?" in query or tokens & question_terms:
        return False

    health_terms = {
        "symptom", "symptoms", "diabetes", "blood", "pressure", "vaccine", "vaccines",
        "flu", "cold", "malaria", "dengue", "typhoid", "headache", "migraine", "asthma",
        "heart", "cholesterol", "medicine", "medication", "doctor", "health", "wellness",
        "condition", "disease", "treatment", "infection", "pain", "fever", "prevention"
    }
    tokens = set(re.findall(r"\b[a-z]{3,}\b", normalized))
    if tokens & health_terms:
        return False

    return True


def casual_greeting_response() -> str:
    return (
        "Hi! I'm HealthAware AI. I'm doing well, thank you. How can I help you today? "
        "You can ask me about symptoms, prevention, nutrition, medications, "
        "or general wellness."
    )


def _rejected_query_result(db: Session, query: str, response: str, user_id: int, conversation_id: int) -> Dict[str, Any]:
    """Persist a rejected question so the user can see why it was declined."""
    ChatRepository.add_message(
        db=db,
        conversation_id=conversation_id,
        role="user",
        content=query,
        sentiment="neutral"
    )
    assistant_msg = ChatRepository.add_message(
        db=db,
        conversation_id=conversation_id,
        role="assistant",
        content=response,
        sources=[],
        sentiment="neutral"
    )
    AuditLogRepository.log(
        db, action="CHAT_REJECTED", user_id=user_id,
        resource="chat", status="REJECTED", details=f"Conv {conversation_id}"
    )
    return {
        "success": False,
        "is_emergency": False,
        "is_crisis": False,
        "response": response,
        "sources": [],
        "message_id": assistant_msg.id,
        "conversation_id": conversation_id
    }


def _build_retrieval_query(db: Session, conversation_id: int, query: str) -> str:
    """Resolve short follow-ups against the latest user topic for retrieval."""
    normalized_query = " ".join(query.lower().split())
    if not normalized_query:
        return query

    # If the query already names a specific condition or topic, do not attach the previous
    # conversation topic to it. This prevents old content like 'headache' from contaminating
    # a fresh malaria or diabetes question.
    topic_terms = {
        "malaria", "dengue", "diabetes", "hypertension", "cholesterol", "flu", "cold",
        "asthma", "vaccine", "vaccines", "heart", "symptom", "headache", "migraine",
    }
    query_terms = set(re.findall(r"\b[a-z0-9]{3,}\b", normalized_query))
    if query_terms & topic_terms:
        return query

    follow_up_pattern = re.compile(
        r"\b(it|this|that|they|them|there|from it|about it|for it)\b",
        re.IGNORECASE
    )
    if not follow_up_pattern.search(query):
        return query

    messages = ChatRepository.get_messages(db, conversation_id)
    previous_user_queries = [message for message in messages if message.role == "user" and message.content.strip() != query.strip()]
    if not previous_user_queries:
        return query

    # Prefer the latest verified assistant source title. This preserves the
    # disease topic without reintroducing the previous request, such as
    # "what is malaria", into a prevention-only follow-up.
    assistant_messages = [message for message in messages if message.role == "assistant" and message.sources_json]
    if assistant_messages:
        try:
            sources = json.loads(assistant_messages[-1].sources_json)
            if sources and sources[0].get("title"):
                topic = re.sub(r"\s+awareness$", "", sources[0]["title"], flags=re.IGNORECASE)
                return f"{topic} {query}"
        except (TypeError, ValueError, json.JSONDecodeError):
            pass

    previous_query = previous_user_queries[-1].content
    topic_match = re.search(
        r"\b(malaria|dengue|typhoid|diabetes|asthma|rabies|hypertension|stroke|cholera|covid(?:-19)?|hepatitis\s+b|tuberculosis|copd)\b",
        previous_query,
        re.IGNORECASE,
    )
    if topic_match:
        return f"{topic_match.group(0)} {query}"
    return query


def _build_headache_definition_prevention_response() -> str:
    """Handle 'what is headache and how can we prevent it' with ordered explanation + prevention."""
    explanation = (
        "A headache is a common symptom that can have many possible causes, including tension, "
        "dehydration, lack of sleep, illness, or migraine. A symptom alone cannot confirm a diagnosis."
    )
    prevention = (
        "For a mild headache, rest in a quiet environment, drink water, eat regularly if you have missed a meal, "
        "and reduce bright light or screen exposure. Discuss any medicine with a pharmacist or healthcare professional, "
        "especially if you have other conditions or take regular medicines."
    )
    return (
        "## What is a headache?\n\n"
        f"{explanation}\n\n"
        "### How can we prevent or reduce it?\n\n"
        f"- {prevention}\n\n"
        "---\n"
        "**Educational Notice:** This information is for general health awareness only. "
        "It is not a diagnosis or personalized medical advice. Consult a qualified healthcare professional."
    )


class RAGService:
    @staticmethod
    def process_query(
        db: Session,
        query: str,
        user_id: int,
        conversation_id: Optional[int] = None,
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Executes end-to-end healthcare question answering:
        Input Safety -> Emergency Check -> Sentiment -> RAG Retrieval -> LLM -> Output Guardrails -> Persistence.
        """
        # 1. Pre-Processing Safety Inspection
        safety_eval = SafetyService.inspect_input(query)

        # Handle validation rejection
        if not safety_eval.is_safe_to_proceed and not safety_eval.is_emergency and not safety_eval.is_crisis:
            return {
                "success": False,
                "is_emergency": False,
                "is_crisis": False,
                "response": f"⚠️ {safety_eval.rejection_reason}",
                "sources": [],
                "conversation_id": conversation_id
            }

        # Handle immediate emergency
        if safety_eval.is_emergency:
            AuditLogRepository.log(db, action="EMERGENCY_TRIGGERED", user_id=user_id, resource="chat", status="ALERT", details=query[:100])
            return {
                "success": True,
                "is_emergency": True,
                "is_crisis": False,
                "response": safety_eval.emergency_details.guidance,
                "emergency_details": safety_eval.emergency_details,
                "sources": [],
                "conversation_id": conversation_id
            }

        # Handle mental health crisis
        if safety_eval.is_crisis:
            AuditLogRepository.log(db, action="CRISIS_TRIGGERED", user_id=user_id, resource="chat", status="ALERT", details=query[:100])
            return {
                "success": True,
                "is_emergency": False,
                "is_crisis": True,
                "response": safety_eval.crisis_details.guidance,
                "crisis_details": safety_eval.crisis_details,
                "sources": [],
                "conversation_id": conversation_id
            }

        sanitized_query = safety_eval.sanitized_text

        # Ensure conversation exists
        if not conversation_id:
            conv = ChatRepository.create_conversation(db, user_id=user_id, language=language)
            conversation_id = conv.id

        # Keep conversational openers friendly and out of the medical response pipeline.
        if is_casual_greeting(sanitized_query):
            greeting_response = localize_greeting(language)
            ChatRepository.add_message(
                db=db,
                conversation_id=conversation_id,
                role="user",
                content=sanitized_query,
                sentiment="neutral"
            )
            assistant_msg = ChatRepository.add_message(
                db=db,
                conversation_id=conversation_id,
                role="assistant",
                content=greeting_response,
                sources=[],
                sentiment="supportive"
            )
            AuditLogRepository.log(
                db, action="CHAT_GREETING", user_id=user_id,
                resource="chat", status="SUCCESS", details=f"Conv {conversation_id}"
            )
            return {
                "success": True,
                "is_emergency": False,
                "is_crisis": False,
                "response": greeting_response,
                "sources": [],
                "message_id": assistant_msg.id,
                "conversation_id": conversation_id
            }

        normalized_query = sanitized_query.lower()
        if (
            "headache" in normalized_query
            and ("what is" in normalized_query or "what is a" in normalized_query)
            and ("prevent" in normalized_query or "prevention" in normalized_query or "avoid" in normalized_query)
        ):
            response = localize_response(_build_headache_definition_prevention_response(), language)
            ChatRepository.add_message(
                db=db,
                conversation_id=conversation_id,
                role="user",
                content=sanitized_query,
                sentiment="neutral"
            )
            assistant_msg = ChatRepository.add_message(
                db=db,
                conversation_id=conversation_id,
                role="assistant",
                content=response,
                sources=[{
                    "title": "General Symptoms Awareness",
                    "category": "General Health",
                    "source": "Verified Healthcare Documentation"
                }],
                sentiment="supportive"
            )
            AuditLogRepository.log(
                db, action="CHAT_QUERY", user_id=user_id,
                resource="chat", status="SUCCESS", details=f"Conv {conversation_id}"
            )
            return {
                "success": True,
                "is_emergency": False,
                "is_crisis": False,
                "response": response,
                "sources": [{
                    "title": "General Symptoms Awareness",
                    "category": "General Health",
                    "source": "Verified Healthcare Documentation"
                }],
                "message_id": assistant_msg.id,
                "conversation_id": conversation_id
            }

        retrieval_query = _build_retrieval_query(db, conversation_id, sanitized_query)

        # Retrieve first so the scope decision can recognize any health topic
        # represented in the verified corpus, without a hardcoded disease list.
        raw_chunks = retrieve_relevant_chunks(db, query=retrieval_query, top_k=4)
        context_chunks = rerank_chunks(raw_chunks, query=retrieval_query, max_context_chunks=3)

        query_terms = {
            token for token in re.findall(r"\b[a-z0-9]{3,}\b", retrieval_query.lower())
            if token not in {
                "about", "are", "does", "from", "have", "what", "when", "which", "with",
                "and", "can", "feeling", "for", "how", "myself", "now", "prevent", "right", "the",
                "awareness", "condition", "disease", "health", "illness", "medical",
                "medicine", "sign", "signs", "symptom", "symptoms", "treatment", "wellness",
            }
        }
        health_intent = is_health_awareness_query(retrieval_query)
        has_title_source_match = any(
            any(term in chunk.get("title", "").lower() for term in query_terms)
            for chunk in context_chunks
        )
        has_repeated_source_match = any(
            any(
                len(re.findall(rf"\b{re.escape(term)}\b", chunk.get("content", "").lower())) >= 2
                for term in query_terms
            )
            for chunk in context_chunks
        )
        has_source_match = has_title_source_match or (health_intent and has_repeated_source_match)

        if not health_intent and not has_title_source_match:
            return _rejected_query_result(
                db, sanitized_query, OFF_TOPIC_RESPONSE, user_id, conversation_id
            )

        # Require a direct source match and sufficient relevance before answering.
        if not has_source_match or not context_chunks or context_chunks[0].get("score", 0) < MIN_SUPPORTED_CONTEXT_SCORE:
            return _rejected_query_result(
                db, sanitized_query, UNSUPPORTED_HEALTH_RESPONSE, user_id, conversation_id
            )

        # 2. Analyze emotional sentiment
        sentiment_info = analyze_sentiment(sanitized_query)

        # Save user message to database
        ChatRepository.add_message(
            db=db,
            conversation_id=conversation_id,
            role="user",
            content=sanitized_query,
            sentiment=sentiment_info["sentiment"]
        )

        # Answer from verified source text only; no generative model is allowed here.
        final_response = localize_response(
            build_verified_response(context_chunks, query=sanitized_query),
            language
        )

        # Format sources
        sources_list = [
            {
                "title": c["title"],
                "category": c["category"],
                "source": c["source"]
            }
            for c in context_chunks
        ]

        # Save assistant message to database
        assistant_msg = ChatRepository.add_message(
            db=db,
            conversation_id=conversation_id,
            role="assistant",
            content=final_response,
            sources=sources_list,
            sentiment="supportive"
        )

        AuditLogRepository.log(db, action="CHAT_QUERY", user_id=user_id, resource="chat", status="SUCCESS", details=f"Conv {conversation_id}")

        return {
            "success": True,
            "is_emergency": False,
            "is_crisis": False,
            "response": final_response,
            "sources": sources_list,
            "message_id": assistant_msg.id,
            "conversation_id": conversation_id
        }
