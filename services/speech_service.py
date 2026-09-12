"""
HealthAware AI - Speech-to-Text Service
Python-based audio processing abstraction without any JavaScript APIs.
Supports audio input uploads and transcribes speech using a clean provider pattern.
"""

from typing import Tuple, Optional


class SpeechToTextProvider:
    def transcribe(self, audio_bytes: bytes, filename: str) -> Tuple[bool, str]:
        raise NotImplementedError


class MockSpeechProvider(SpeechToTextProvider):
    """
    Fallback speech-to-text provider for local development.
    Transcribes test queries or returns guidance.
    """
    def transcribe(self, audio_bytes: bytes, filename: str) -> Tuple[bool, str]:
        if not audio_bytes or len(audio_bytes) < 10:
            return False, "Empty or invalid audio input received."
        # Demo simulation for audio uploaded in Streamlit
        return True, "What are healthy daily habits to support heart health and prevent high blood pressure?"


def get_speech_provider() -> SpeechToTextProvider:
    return MockSpeechProvider()
