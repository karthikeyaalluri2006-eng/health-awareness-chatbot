"""Health-awareness scope checks for user questions."""

import re


HEALTH_TERMS = {
    "allergy", "anxiety", "asthma", "blood", "breath", "cancer", "cholesterol",
    "cold", "condition", "cough", "dengue", "diabetes", "diagnosis", "diet", "disease",
    "doctor", "exercise", "fever", "flu", "glucose", "headache", "headaches",
    "health", "heart", "hypertension", "illness", "immunity", "infection", "injury",
    "insulin", "malaria", "medication", "mental", "migraine", "nutrition", "pain", "pregnant",
    "pressure", "prevent", "symptom", "therapy", "vaccine", "vaccines", "wellness", "weight",
    "sleep", "stress", "typhoid", "vitamin", "medical", "medicine", "treatment", "wellbeing",
    "transmit", "transmitted", "transmission",
}

HEALTH_QUESTION_TERMS = {
    "can", "cause", "difference", "help", "mean", "prevent", "risk", "should",
    "explain", "give", "guide", "information", "info", "list", "overview", "tell",
    "experiencing", "feel", "feeling", "have", "having", "sign", "signs", "symptom",
    "symptoms", "what", "when", "which", "why", "how",
}

def is_health_awareness_query(query: str) -> bool:
    """Return True only when a query contains health language and a question intent."""
    tokens = set(re.findall(r"\b[a-zA-Z]{3,}\b", query.lower()))
    return bool(tokens & HEALTH_TERMS) and bool(tokens & HEALTH_QUESTION_TERMS)
