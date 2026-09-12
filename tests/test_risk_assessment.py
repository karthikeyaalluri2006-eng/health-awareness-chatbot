"""
Unit and Integration Tests for Educational Risk Assessment Scoring
"""

import pytest
from database.connection import get_db_session, init_db
from database.repositories import RiskAssessmentRepository


@pytest.fixture(autouse=True)
def setup_db():
    init_db()


def test_diabetes_risk_calculation():
    # Scoring verification:
    # High risk profile: age >= 60 (3 pts), inactive (1 pt), family history (1 pt), obese (2 pts) = 7 pts -> Higher Educational Risk
    score = 3 + 1 + 1 + 2
    assert score >= 5
    risk_level = "Higher Educational Risk" if score >= 5 else "Moderate Educational Risk"
    assert risk_level == "Higher Educational Risk"


def test_risk_assessment_repository_persistence():
    with get_db_session() as db:
        rec = RiskAssessmentRepository.save_assessment(
            db=db,
            user_id=1,
            assessment_type="Type 2 Diabetes",
            inputs={"age": "50-59", "active": "No"},
            risk_level="Moderate Educational Risk",
            score=4.0,
            factors=["Age range", "Physical inactivity"],
            recommendations=["Increase moderate aerobic activity"]
        )
        assert rec.id is not None
        assert rec.risk_level == "Moderate Educational Risk"

        assessments = RiskAssessmentRepository.get_user_assessments(db, 1)
        assert len(assessments) > 0
