"""
HealthAware AI - Symptom Awareness & Triage Service
Structures symptom inquiries into safe educational awareness tiers:
- Emergency Care Required
- Urgent Medical Evaluation
- Consider Contacting Healthcare Professional
- General Awareness & Self-Monitoring
Strictly educational - never provides definitive diagnosis.
"""

from typing import Dict, Any, List

RED_FLAG_SYMPTOMS = {
    "chest pain", "difficulty breathing", "shortness of breath", "loss of consciousness",
    "stroke signs", "slurred speech", "sudden weakness", "severe allergic reaction",
    "coughing blood", "high fever with stiff neck", "worst headache of life"
}


def evaluate_symptoms(
    age_group: str,
    primary_symptom: str,
    duration_days: int,
    severity: int,  # 1 to 10 scale
    associated_symptoms: List[str],
    chronic_conditions: List[str]
) -> Dict[str, Any]:
    """
    Evaluates symptoms using structured clinical triage rules.
    Categorizes urgency level and provides actionable educational guidance.
    """
    symptom_lower = primary_symptom.lower().strip()
    associated_lower = [s.lower() for s in associated_symptoms]

    # Check for acute red flags
    has_red_flag = any(rf in symptom_lower for rf in RED_FLAG_SYMPTOMS) or any(
        any(rf in a for rf in RED_FLAG_SYMPTOMS) for a in associated_lower
    )

    if has_red_flag or severity >= 9:
        urgency = "🚨 Immediate Emergency Care Recommended"
        color = "#ef4444"
        guidance = (
            "The combination of symptoms or high severity rating indicates a potential medical emergency. "
            "Please call your local emergency number (e.g. 911, 112, or 108) or go to the nearest emergency facility immediately. "
            "Do not drive yourself if you are feeling faint or experiencing chest pain."
        )
        recommended_action = "Seek Immediate Emergency Medical Attention"

    elif severity >= 6 or duration_days > 7 or "Diabetes" in chronic_conditions or "Heart Disease" in chronic_conditions:
        urgency = "⚠️ Urgent Medical Evaluation Recommended"
        color = "#f97316"
        guidance = (
            "Based on the severity rating, duration, or underlying health factors, these symptoms warrant prompt clinical evaluation. "
            "We recommend contacting your primary doctor's office today or visiting an urgent care clinic within 24 to 48 hours."
        )
        recommended_action = "Schedule Prompt Medical Consultation"

    elif duration_days > 3 or severity >= 4:
        urgency = "ℹ️ Consider Contacting a Healthcare Professional"
        color = "#eab308"
        guidance = (
            "Your symptoms have persisted for several days. If they do not improve, or if new symptoms develop, "
            "consult with your doctor or a telehealth practitioner for personalized advice."
        )
        recommended_action = "Monitor Closely and Consult If No Improvement"

    else:
        urgency = "✅ General Health Awareness & Self-Monitoring"
        color = "#10b981"
        guidance = (
            "These symptoms appear to be mild and of short duration. Maintain good hydration, rest, and nutrition. "
            "However, if your condition worsens or red flags appear, seek medical evaluation."
        )
        recommended_action = "Rest, Hydration & Self-Care"

    return {
        "urgency_level": urgency,
        "color": color,
        "guidance": guidance,
        "recommended_action": recommended_action,
        "summary": {
            "Age Group": age_group,
            "Reported Symptom": primary_symptom,
            "Duration": f"{duration_days} days",
            "Severity": f"{severity} / 10",
            "Associated Symptoms": ", ".join(associated_symptoms) if associated_symptoms else "None",
            "Underlying Conditions": ", ".join(chronic_conditions) if chronic_conditions else "None declared"
        },
        "disclaimer": (
            "This symptom assessment tool is strictly for educational guidance and awareness. "
            "It does not perform clinical diagnosis, clinical triage, or replace a doctor's examination."
        )
    }
