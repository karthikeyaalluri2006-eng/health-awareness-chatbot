"""
HealthAware AI - EHR / EMR Interoperability Adapter
Architecture supporting future FHIR (Fast Healthcare Interoperability Resources) standard connections.
Includes MockEHRProvider with demo medical summary data clearly labeled.
"""

from typing import Dict, Any, List


class EHRProvider:
    def get_patient_summary(self, patient_id: str) -> Dict[str, Any]:
        raise NotImplementedError


class MockEHRProvider(EHRProvider):
    """Provides sample FHIR-structured educational health records (Demo Mode)."""
    def get_patient_summary(self, patient_id: str) -> Dict[str, Any]:
        return {
            "resourceType": "Bundle",
            "type": "collection",
            "is_demo_data": True,
            "patient": {
                "id": "PATIENT-DEMO-001",
                "name": "Alex Morgan",
                "gender": "Non-Disclosed",
                "birthDate": "1988-04-12"
            },
            "allergies": [
                {"substance": "Penicillin", "reaction": "Mild Rash", "severity": "Mild"},
                {"substance": "Peanuts", "reaction": "Anaphylaxis", "severity": "Severe"}
            ],
            "immunizations": [
                {"vaccine": "Influenza (Annual)", "date": "2025-10-15", "status": "Completed"},
                {"vaccine": "Tetanus, Diphtheria, Pertussis (Tdap)", "date": "2022-06-20", "status": "Completed"},
                {"vaccine": "COVID-19 Updated Booster", "date": "2025-11-02", "status": "Completed"}
            ],
            "recent_labs": [
                {"test": "Fasting Blood Glucose", "value": "94 mg/dL", "reference": "70-99 mg/dL", "status": "Normal"},
                {"test": "Total Cholesterol", "value": "182 mg/dL", "reference": "< 200 mg/dL", "status": "Normal"},
                {"test": "Blood Pressure", "value": "118/76 mmHg", "reference": "< 120/80 mmHg", "status": "Optimal"},
                {"test": "HbA1c", "value": "5.4 %", "reference": "< 5.7 %", "status": "Normal"}
            ],
            "disclaimer": "This is simulated demonstration EHR data. It does not reflect actual medical history."
        }


def get_ehr_provider() -> EHRProvider:
    return MockEHRProvider()
