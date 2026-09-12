"""
HealthAware AI - Medication Management Service
Tracks medication schedules, logging adherence, and refill reminders.
Strict rule: Never prescribes medicines or alters doctor-prescribed doses.
"""

from datetime import date
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from database.repositories import MedicationRepository


class MedicationService:
    @staticmethod
    def get_daily_schedule(db: Session, user_id: int) -> List[Dict[str, Any]]:
        """Returns today's medication schedule with status."""
        today_str = date.today().isoformat()
        meds = MedicationRepository.get_user_medications(db, user_id, active_only=True)
        schedule = []

        for med in meds:
            times = ["08:00"]
            if med.times_json:
                import json
                try:
                    times = json.loads(med.times_json)
                except Exception:
                    times = [med.times_json]

            for t in times:
                schedule.append({
                    "medication_id": med.id,
                    "name": med.name,
                    "dosage": med.dosage,
                    "frequency": med.frequency,
                    "time": t,
                    "instructions": med.instructions or "Take as prescribed",
                    "refill_date": med.refill_date or "Not specified",
                    "today": today_str
                })

        # Sort chronologically by time
        schedule.sort(key=lambda x: x["time"])
        return schedule

    @staticmethod
    def log_status(db: Session, med_id: int, user_id: int, sched_time: str, status: str):
        today_str = date.today().isoformat()
        return MedicationRepository.log_status(
            db=db,
            med_id=med_id,
            user_id=user_id,
            sched_date=today_str,
            sched_time=sched_time,
            status=status
        )

    @staticmethod
    def get_adherence_stats(db: Session, user_id: int) -> Dict[str, Any]:
        rate = MedicationRepository.get_adherence_rate(db, user_id, days=7)
        return {
            "adherence_percentage": rate,
            "status_label": "Excellent" if rate >= 90 else "Good" if rate >= 75 else "Needs Improvement"
        }
