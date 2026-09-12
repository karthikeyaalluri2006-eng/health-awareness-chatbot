"""
HealthAware AI - Input Validation & Sanitization
Protects against prompt injection, malicious inputs, length overflow, and accidental PII entry.
"""

import re
from typing import Tuple

# Patterns that attempt prompt injection or role hijacking
PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
    r"you\s+are\s+now\s+a\s+medical\s+doctor",
    r"act\s+as\s+a\s+licensed\s+physician",
    r"prescribe\s+me\s+medicine\s+without\s+disclaimer",
    r"reveal\s+(your\s+)?system\s+prompt",
    r"bypass\s+all\s+safety\s+filters",
    r"<script[\s>]",
    r"javascript:",
]

# Sensitive PII patterns
SSN_PATTERN = r"\b\d{3}-\d{2}-\d{4}\b"
CREDIT_CARD_PATTERN = r"\b(?:\d{4}[-\s]?){3}\d{4}\b"


def sanitize_input(text: str) -> Tuple[bool, str, str]:
    """
    Sanitize and validate user query.
    Returns: (is_valid, cleaned_or_sanitized_text, reason_if_invalid)
    """
    if not text or not text.strip():
        return False, "", "Input message cannot be empty."

    cleaned = text.strip()

    # Limit maximum characters to prevent DOS attacks
    if len(cleaned) > 2000:
        return False, "", "Query exceeds maximum allowable length of 2,000 characters."

    # Check for prompt injection attempts
    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, cleaned, re.IGNORECASE):
            return False, "", "Your request contains prohibited directives or invalid formatting."

    # Redact sensitive PII if accidentally supplied
    cleaned = re.sub(SSN_PATTERN, "[REDACTED-SSN]", cleaned)
    cleaned = re.sub(CREDIT_CARD_PATTERN, "[REDACTED-CARD]", cleaned)

    return True, cleaned, ""
