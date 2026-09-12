"""
HealthAware AI - Mental Health Crisis & Self-Harm Detection
Detects self-harm expressions, suicidal thoughts, and acute emotional distress.
Immediately halts normal conversational answers to offer verified crisis lifelines.
"""

import re
from typing import Dict, List
from dataclasses import dataclass, field


@dataclass
class CrisisCheckResult:
    is_crisis: bool
    guidance: str = ""
    resources: List[Dict[str, str]] = field(default_factory=list)


VERIFIED_CRISIS_RESOURCES = [
    {
        "region": "United States & Canada",
        "name": "988 Suicide & Crisis Lifeline",
        "contact": "Call or Text 988 (Available 24/7, Free & Confidential)",
        "website": "https://988lifeline.org"
    },
    {
        "region": "United States & Canada",
        "name": "The Crisis Text Line",
        "contact": "Text HOME to 741741 (Free 24/7 support via SMS)",
        "website": "https://www.crisistextline.org"
    },
    {
        "region": "India",
        "name": "Tele-MANAS (Govt of India)",
        "contact": "Toll-Free 14416 or 1800-891-4416 (24/7 Mental Health Helpline)",
        "website": "https://telemanas.mohfw.gov.in"
    },
    {
        "region": "United Kingdom",
        "name": "Samaritans UK",
        "contact": "Call 116 123 (Free anytime)",
        "website": "https://www.samaritans.org"
    },
    {
        "region": "International",
        "name": "Befrienders Worldwide",
        "contact": "Find confidential emotional support worldwide",
        "website": "https://www.befrienders.org"
    }
]

CRISIS_PATTERNS = [
    r"\b(want\s+to\s+die|kill\s+myself|suicid(e|al)|end\s+my\s+life|don'?t\s+want\s+to\s+live\s+anymore)\b",
    r"\b(better\s+off\s+dead|no\s+reason\s+to\s+live|hanging\s+myself|overdose\s+on\s+pills)\b",
    r"\b(cut(ting)?\s+my\s+wrists|self[\s-]harm|hurting\s+myself)\b",
    r"\b(nobody\s+would\s+care\s+if\s+i\s+was\s+gone|goodbye\s+cruel\s+world)\b",
]


def check_crisis(text: str) -> CrisisCheckResult:
    """Scan user message for indications of self-harm or acute psychological crisis."""
    cleaned = text.lower().strip()

    for pattern in CRISIS_PATTERNS:
        if re.search(pattern, cleaned):
            guidance = (
                "💙 You are not alone, and there is compassionate, free, confidential support available right now. "
                "Please reach out to one of the trained crisis counselors listed below. They are available 24/7 "
                "to listen and help you through this difficult moment."
            )
            return CrisisCheckResult(
                is_crisis=True,
                guidance=guidance,
                resources=VERIFIED_CRISIS_RESOURCES
            )

    return CrisisCheckResult(is_crisis=False, guidance="", resources=[])
