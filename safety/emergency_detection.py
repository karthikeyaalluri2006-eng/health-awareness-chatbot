"""
HealthAware AI - Emergency Red-Flag Detection
Detects immediate, life-threatening symptoms and triggers urgent medical triage.
Never invents emergency numbers; uses verified, configuration-driven hotlines.
"""

import re
from typing import Dict, List, Any
from dataclasses import dataclass, field


@dataclass
class EmergencyCheckResult:
    is_emergency: bool
    urgency_level: str  # 'IMMEDIATE_EMERGENCY', 'URGENT_EVALUATION', 'NORMAL'
    matched_flags: List[str] = field(default_factory=list)
    guidance: str = ""
    emergency_contacts: List[Dict[str, str]] = field(default_factory=list)


# Verified emergency contacts by jurisdiction
VERIFIED_EMERGENCY_HOTLINES = [
    {"region": "United States & Canada", "service": "Emergency Medical Services", "number": "911"},
    {"region": "European Union & UK", "service": "European Emergency Number", "number": "112"},
    {"region": "India", "service": "National Emergency & Ambulance", "number": "112 / 108"},
    {"region": "United Kingdom", "service": "NHS Urgent Medical Advice (Non-Emergency)", "number": "111"},
    {"region": "Australia", "service": "Emergency Services", "number": "000"},
]

# Patterns representing immediate, acute life-threatening emergencies
EMERGENCY_PATTERNS = [
    (r"\b(crushing|severe|radiating)\s+(chest\s+pain|chest\s+pressure|heart\s+attack)\b", "Severe Chest Pain / Potential Cardiac Event"),
    (r"\b(chest\s+pain)\b.*\b(left\s+arm|jaw|back|sweat|shortness\s+of\s+breath)\b", "Chest Pain with Radiation / Associated Cardiac Symptoms"),
    (r"\b(can'?t\s+breathe|gasping\s+for\s+air|suffocating|choking|severe\s+difficulty\s+breathing)\b", "Acute Respiratory Distress"),
    (r"\b(face\s+droop|slurred\s+speech|arm\s+weakness|stroke\s+symptoms|FAST\s+symptoms)\b", "Suspected Stroke / Acute Neurological Deficit"),
    (r"\b(loss\s+of\s+consciousness|passed\s+out|unconscious|unresponsive|fainted\s+and\s+not\s+waking)\b", "Loss of Consciousness / Unresponsiveness"),
    (r"\b(coughing\s+up\s+blood|vomiting\s+blood|severe\s+uncontrolled\s+bleeding|hemorrhage)\b", "Severe / Uncontrolled Bleeding"),
    (r"\b(throat\s+closing|anaphylaxis|swollen\s+tongue|severe\s+allergic\s+reaction)\b", "Anaphylactic / Airway Obstruction Reaction"),
    (r"\b(seizure\s+now|continuous\s+convulsion|status\s+epilepticus)\b", "Active Seizure / Convulsions"),
    (r"\b(worst\s+headache\s+of\s+(my\s+)?life|thunderclap\s+headache)\b", "Sudden Explosive Headache (Possible Subarachnoid Event)"),
]

# Patterns for urgent, non-immediate evaluation
URGENT_PATTERNS = [
    (r"\b(high\s+fever)\b.*\b(stiff\s+neck|confusion)\b", "High Fever with Meningismus/Confusion"),
    (r"\b(severe\s+abdominal\s+pain|sharp\s+stomach\s+pain|appendix\s+burst)\b", "Acute Abdominal Distress"),
    (r"\b(sudden\s+vision\s+loss|blind\s+in\s+one\s+eye)\b", "Acute Vision Loss"),
]


def check_emergency(text: str) -> EmergencyCheckResult:
    """
    Scans user message for acute red-flag emergency symptoms.
    Runs BEFORE sending query to LLM or RAG pipeline.
    """
    cleaned = text.lower().strip()
    matched_flags = []

    # 1. Check immediate life-threatening patterns
    for pattern, description in EMERGENCY_PATTERNS:
        if re.search(pattern, cleaned):
            matched_flags.append(description)

    if matched_flags:
        guidance = (
            "🚨 CRITICAL MEDICAL ALERT: The symptoms you described may indicate a life-threatening medical emergency. "
            "Please DO NOT wait for this AI assistant. Immediately call your local emergency medical services (such as 911, 112, or 108) "
            "or proceed to the nearest emergency department right now."
        )
        return EmergencyCheckResult(
            is_emergency=True,
            urgency_level="IMMEDIATE_EMERGENCY",
            matched_flags=matched_flags,
            guidance=guidance,
            emergency_contacts=VERIFIED_EMERGENCY_HOTLINES
        )

    # 2. Check urgent non-immediate patterns
    urgent_flags = []
    for pattern, description in URGENT_PATTERNS:
        if re.search(pattern, cleaned):
            urgent_flags.append(description)

    if urgent_flags:
        guidance = (
            "⚠️ URGENT MEDICAL ATTENTION RECOMMENDED: The symptoms described may require prompt medical evaluation. "
            "We strongly advise consulting an urgent care clinic or speaking with a qualified physician promptly."
        )
        return EmergencyCheckResult(
            is_emergency=False,
            urgency_level="URGENT_EVALUATION",
            matched_flags=urgent_flags,
            guidance=guidance,
            emergency_contacts=VERIFIED_EMERGENCY_HOTLINES[:3]
        )

    return EmergencyCheckResult(
        is_emergency=False,
        urgency_level="NORMAL",
        matched_flags=[],
        guidance="",
        emergency_contacts=[]
    )
