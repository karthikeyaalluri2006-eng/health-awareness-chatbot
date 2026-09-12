"""
HealthAware AI - Unified Safety Service
Orchestrates input validation, emergency detection, crisis detection,
and output compliance verification.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

from safety.input_validation import sanitize_input
from safety.emergency_detection import check_emergency, EmergencyCheckResult
from safety.crisis_detection import check_crisis, CrisisCheckResult
from safety.output_validation import validate_and_sanitize_output


@dataclass
class PreProcessingSafetyResult:
    is_safe_to_proceed: bool
    is_emergency: bool = False
    is_crisis: bool = False
    sanitized_text: str = ""
    rejection_reason: str = ""
    emergency_details: Optional[EmergencyCheckResult] = None
    crisis_details: Optional[CrisisCheckResult] = None


class SafetyService:
    @staticmethod
    def inspect_input(raw_text: str) -> PreProcessingSafetyResult:
        """
        Runs input validation, emergency triage, and crisis detection.
        Returns safety assessment determining if RAG/LLM should run or be interrupted.
        """
        # 1. Input Sanitization
        is_valid, sanitized_text, reason = sanitize_input(raw_text)
        if not is_valid:
            return PreProcessingSafetyResult(
                is_safe_to_proceed=False,
                rejection_reason=reason
            )

        # 2. Emergency Red-Flag Detection
        emergency_result = check_emergency(sanitized_text)
        if emergency_result.is_emergency:
            return PreProcessingSafetyResult(
                is_safe_to_proceed=False,
                is_emergency=True,
                sanitized_text=sanitized_text,
                emergency_details=emergency_result
            )

        # 3. Crisis & Self-Harm Detection
        crisis_result = check_crisis(sanitized_text)
        if crisis_result.is_crisis:
            return PreProcessingSafetyResult(
                is_safe_to_proceed=False,
                is_crisis=True,
                sanitized_text=sanitized_text,
                crisis_details=crisis_result
            )

        # 4. Safe to proceed with RAG / LLM
        return PreProcessingSafetyResult(
            is_safe_to_proceed=True,
            sanitized_text=sanitized_text,
            emergency_details=emergency_result  # May contain URGENT_EVALUATION non-blocking guidance
        )

    @staticmethod
    def inspect_output(generated_text: str) -> str:
        """Applies output safety guardrails and appends required disclaimer."""
        return validate_and_sanitize_output(generated_text)
