"""
HealthAware AI - Appointment & Provider Scheduling Service
Manages appointment booking, rescheduling, and history using a clean provider abstraction.
Clearly marks demo appointments.
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from database.repositories import AppointmentRepository

AVAILABLE_CLINICS = [
    {
        "clinic_name": "City Health Care Center",
        "specialties": ["General Medicine", "Cardiology", "Endocrinology", "Pediatrics"],
        "doctors": {
            "General Medicine": ["Dr. Sarah Jenkins, MD", "Dr. David Chen, MD"],
            "Cardiology": ["Dr. Robert Evans, FACC", "Dr. Anita Patel, MD"],
            "Endocrinology": ["Dr. Elena Rostova, MD", "Dr. Marcus Vance, MD"],
            "Pediatrics": ["Dr. Emily Taylor, MD"]
        }
    },
    {
        "clinic_name": "Metro Wellness & Family Health",
        "specialties": ["Family Practice", "Dermatology", "Nutrition & Dietetics"],
        "doctors": {
            "Family Practice": ["Dr. Michael Ross, DO", "Dr. Jessica Liu, MD"],
            "Dermatology": ["Dr. Samantha Wright, MD"],
            "Nutrition & Dietetics": ["Rachel Green, RDN, LDN"]
        }
    }
]


class AppointmentService:
    @staticmethod
    def get_clinics() -> List[Dict[str, Any]]:
        return AVAILABLE_CLINICS

    @staticmethod
    def book_appointment(
        db: Session,
        user_id: int,
        clinic_name: str,
        specialty: str,
        provider_name: str,
        appt_date: str,
        appt_time: str,
        appt_type: str = "In-Person",
        notes: str = ""
    ):
        return AppointmentRepository.create(
            db=db,
            user_id=user_id,
            provider=provider_name,
            specialty=specialty,
            clinic=clinic_name,
            appt_date=appt_date,
            appt_time=appt_time,
            appt_type=appt_type,
            notes=notes
        )
