"""
Unit and Integration Tests for Medication Adherence & Schedules
"""

import pytest
from database.connection import get_db_session, init_db
from database.repositories import MedicationRepository


@pytest.fixture(autouse=True)
def setup_db():
    init_db()


def test_medication_crud_and_adherence():
    with get_db_session() as db:
        user_id = 999  # Isolated test user id
        med = MedicationRepository.add(
            db=db,
            user_id=user_id,
            name="Atorvastatin",
            dosage="20mg",
            frequency="Once daily",
            times=["21:00"],
            instructions="Take at bedtime",
            refill_date="2026-12-01"
        )
        assert med.id is not None
        assert med.name == "Atorvastatin"

        # Log doses
        MedicationRepository.log_status(db, med.id, user_id, "2026-09-08", "21:00", "taken")
        MedicationRepository.log_status(db, med.id, user_id, "2026-09-09", "21:00", "taken")

        rate = MedicationRepository.get_adherence_rate(db, user_id, days=7)
        assert rate == 100.0

        # Delete
        deleted = MedicationRepository.delete(db, med.id, user_id)
        assert deleted is True
