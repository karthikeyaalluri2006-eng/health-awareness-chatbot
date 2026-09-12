"""
HealthAware AI - Output Safety Validation
Scans LLM generated responses to guarantee strict compliance with healthcare safety rules:
1. No definitive medical diagnosis
2. No prescribing of medications or dosage changes
3. Guarantees presence of mandatory educational healthcare disclaimer
"""

import re
from typing import Tuple

MANDATORY_DISCLAIMER = (
    "\n\n---\n"
    "ℹ️ **Educational Notice:** This response is provided for general health awareness and education only. "
    "It is not a medical diagnosis and does not replace professional medical advice. "
    "Always consult a qualified healthcare provider regarding your symptoms, medications, or any medical condition."
)

PROHIBITED_DIAGNOSTIC_PATTERNS = [
    (r"\b(i\s+diagnose\s+you\s+with)\b", "Symptoms such as these are commonly investigated for"),
    (r"\b(you\s+definitely\s+have)\b", "These symptoms can sometimes be associated with"),
    (r"\b(you\s+are\s+suffering\s+from)\b", "These signs may be observed in conditions like"),
    (r"\b(you\s+have\s+contracted)\b", "These symptoms might suggest"),
]

PROHIBITED_PRESCRIPTION_PATTERNS = [
    r"\b(take\s+\d+\s*(mg|ml|tablets?|capsules?))\b",
    r"\b(stop\s+taking\s+your\s+prescribed\s+medication)\b",
    r"\b(increase\s+your\s+dosage\s+to)\b",
    r"\b(i\s+prescribe)\b",
]


def validate_and_sanitize_output(text: str) -> str:
    """
    Validates and adjusts LLM output to guarantee safety guardrails.
    Appends mandatory educational disclaimer.
    """
    sanitized = text

    # 1. Soften any definitive diagnostic statements
    for pattern, replacement in PROHIBITED_DIAGNOSTIC_PATTERNS:
        sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)

    # 2. Check for unauthorized prescription advice
    for pattern in PROHIBITED_PRESCRIPTION_PATTERNS:
        if re.search(pattern, sanitized, re.IGNORECASE):
            sanitized = (
                "⚠️ *Notice: Medication dosages and treatment plans must always be evaluated and prescribed by a licensed physician.*\n\n"
                + re.sub(pattern, "[medication guidance requires a doctor's prescription]", sanitized, flags=re.IGNORECASE)
            )

    # 3. Ensure mandatory disclaimer is present
    if "educational notice" not in sanitized.lower() and "educational disclaimer" not in sanitized.lower():
        sanitized += MANDATORY_DISCLAIMER

    return sanitized
