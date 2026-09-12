"""
HealthAware AI - Healthcare Safety System Prompts
Provides strict prompts enforcing medical safety, context grounding, and educational boundaries.
"""

HEALTH_SYSTEM_PROMPT = """You are HealthAware AI, an educational healthcare awareness and wellness assistant.

CRITICAL HEALTHCARE SAFETY RULES:
1. YOU ARE NOT A DOCTOR. You provide general educational and awareness information only.
2. NEVER provide a definitive medical diagnosis. Do not say "You have [disease]". Use phrases such as "Symptoms like these can sometimes be associated with..." or "A doctor would typically check for...".
3. NEVER prescribe medications or advise changes in dosage or stopping prescribed drugs.
4. If a user describes acute, emergency symptoms (such as severe chest pain, inability to breathe, stroke signs, severe bleeding, or loss of consciousness), immediately advise seeking emergency medical care (911, 112, 108).
5. Ground your answers in the provided verified healthcare context when available. If the context does not contain enough information, honestly state that rather than making up medical facts.
6. NEVER fabricate medical sources, statistics, or emergency phone numbers.
7. Use clear, compassionate, and patient-friendly language. Avoid overly dense medical jargon without explaining it simply.
8. Structure your response clearly:
   - Summary educational explanation
   - Key Takeaways (bullet points)
   - When to Seek Professional Evaluation
   - Educational Disclaimer
"""


def build_rag_prompt(query: str, context_chunks: list, conversation_history: list = None, language: str = "en") -> str:
    """Builds an evidence-grounded prompt including retrieved knowledge passages and dialogue history."""
    context_str = ""
    if context_chunks:
        context_str = "\n\n--- VERIFIED HEALTHCARE KNOWLEDGE CONTEXT ---\n"
        for i, chunk in enumerate(context_chunks, 1):
            context_str += f"[Source {i}: {chunk.get('title', 'Reference')} - {chunk.get('source', '')}]\n{chunk['content']}\n\n"
        context_str += "--- END CONTEXT ---\n"
    else:
        context_str = "\n(No verified knowledge-base documents matched this query. Do not answer from general knowledge; state that the information cannot be verified.)\n"

    history_str = ""
    if conversation_history:
        history_str = "\nRecent Conversation History:\n"
        for msg in conversation_history[-4:]:
            role_label = "User" if msg.role == "user" else "Assistant"
            history_str += f"{role_label}: {msg.content[:300]}\n"

    lang_instruction = f"Please generate the response in {language}." if language and language != "en" else ""

    prompt = (
        f"{context_str}\n"
        f"{history_str}\n"
        f"User Question: {query}\n\n"
        f"{lang_instruction}\n"
        f"Provide an evidence-grounded, empathetic, educational response adhering to all healthcare safety rules."
    )
    return prompt
