"""
HealthAware AI - Sentiment & Emotional Signal Service
Analyzes user sentiment and emotional intensity to guide tone modulation.
Does not perform clinical psychiatric diagnosis.
"""

import re
from typing import Dict, Any

ANXIOUS_WORDS = {"worried", "scared", "terrified", "anxious", "panic", "fear", "nervous", "dread", "freaking"}
DISTRESSED_WORDS = {"crying", "hopeless", "unbearable", "desperate", "agony", "depressed", "miserable"}
CALM_WORDS = {"curious", "wondering", "learning", "information", "question", "how to", "understand"}


def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    Evaluates emotional signals in the user query for tone adaptation.
    Returns: {'sentiment': str, 'tone_recommendation': str}
    """
    tokens = set(re.findall(r"\b[a-z]{3,}\b", text.lower()))

    anxiety_hits = len(tokens.intersection(ANXIOUS_WORDS))
    distress_hits = len(tokens.intersection(DISTRESSED_WORDS))

    if distress_hits > 0:
        return {
            "sentiment": "distressed",
            "tone_recommendation": "Use deeply empathetic, reassuring, and gentle guidance. Offer support resources."
        }
    elif anxiety_hits > 0:
        return {
            "sentiment": "anxious",
            "tone_recommendation": "Use calming, clear, grounding language to help de-escalate health anxiety."
        }
    else:
        return {
            "sentiment": "calm",
            "tone_recommendation": "Use professional, encouraging, educational language."
        }
