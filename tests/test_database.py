"""
Unit and Integration Tests for Database Models and Repositories
"""

import pytest
from database.connection import get_db_session, init_db
from database.repositories import (
    HealthcareServiceRepository, InsuranceFAQRepository,
    MythFactRepository, AuditLogRepository
)
from services.healthcare_directory_service import HealthcareDirectoryService


@pytest.fixture(autouse=True)
def setup_db():
    init_db()


def test_healthcare_directory_repository():
    with get_db_session() as db:
        services = HealthcareServiceRepository.get_all(db)
        assert len(services) > 0
        hospitals = [s for s in services if s.category == "hospital"]
        assert len(hospitals) > 0


def test_healthcare_directory_map_links_use_browser_safe_search_url():
    with get_db_session() as db:
        services = HealthcareDirectoryService.get_services(db)
        hospital = next(s for s in services if s["name"] == "City General Hospital & Emergency Center")

        assert hospital["map_url"].startswith("https://www.google.com/maps/search/?api=1&query=")
        assert "City+General+Hospital+%26+Emergency+Center" in hospital["map_url"]


def test_insurance_faqs_repository():
    with get_db_session() as db:
        faqs = InsuranceFAQRepository.get_all(db)
        assert len(faqs) > 0
        terms = [f.term.lower() for f in faqs]
        assert "deductible" in terms
        assert "copayment (copay)" in terms


def test_myth_fact_repository():
    with get_db_session() as db:
        myths = MythFactRepository.get_all(db)
        assert len(myths) > 0
        sugar_myth = [m for m in myths if "sugar" in m.myth.lower()]
        assert len(sugar_myth) > 0


def test_audit_logging():
    with get_db_session() as db:
        log = AuditLogRepository.log(
            db=db,
            action="SYSTEM_TEST",
            user_id=1,
            resource="test_suite",
            details="Automated test audit check"
        )
        assert log.id is not None
        recent = AuditLogRepository.get_recent(db, limit=5)
        assert any(l.action == "SYSTEM_TEST" for l in recent)
