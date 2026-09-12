"""
HealthAware AI - Database Models (SQLAlchemy ORM)
Covers Users, Chat History, RAG Documents, Quizzes, Risk Assessments,
Medications, Appointments, Directory, Wellness Logs, Wearables, and Audit Logs.
"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey, Index
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    role = Column(String(20), default="user", nullable=False)  # 'user' or 'admin'
    preferred_language = Column(String(10), default="en", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    quiz_attempts = relationship("QuizAttempt", back_populates="user", cascade="all, delete-orphan")
    risk_assessments = relationship("RiskAssessment", back_populates="user", cascade="all, delete-orphan")
    medications = relationship("Medication", back_populates="user", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="user", cascade="all, delete-orphan")
    wellness_logs = relationship("WellnessLog", back_populates="user", cascade="all, delete-orphan")
    wearable_records = relationship("WearableData", back_populates="user", cascade="all, delete-orphan")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(150), default="New Health Consultation", nullable=False)
    language = Column(String(10), default="en", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan", order_by="Message.created_at")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(20), nullable=False)  # 'user', 'assistant', 'system'
    content = Column(Text, nullable=False)
    sources_json = Column(Text, nullable=True)  # JSON serialized list of RAG sources
    sentiment = Column(String(50), nullable=True)  # e.g., 'calm', 'anxious', 'distressed'
    feedback = Column(Integer, nullable=True)  # 1 for positive, -1 for negative
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    conversation = relationship("Conversation", back_populates="messages")


class HealthModule(Base):
    __tablename__ = "health_modules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(60), unique=True, nullable=False, index=True)
    title = Column(String(150), nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    icon = Column(String(30), default="🩺")
    estimated_mins = Column(Integer, default=5)
    content_json = Column(Text, nullable=False)  # JSON structure of lessons & takeaways
    created_at = Column(DateTime, default=datetime.utcnow)


class UserModuleProgress(Base):
    __tablename__ = "user_module_progress"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    module_id = Column(Integer, ForeignKey("health_modules.id", ondelete="CASCADE"), nullable=False)
    completed = Column(Boolean, default=False)
    current_step = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    topic = Column(String(50), nullable=False, index=True)  # 'heart', 'diabetes', 'prevention', etc.
    question = Column(Text, nullable=False)
    options_json = Column(Text, nullable=False)  # JSON array of options
    correct_answer = Column(String(100), nullable=False)
    explanation = Column(Text, nullable=False)
    difficulty = Column(String(20), default="medium")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    topic = Column(String(50), nullable=False)
    score = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)
    answers_json = Column(Text, nullable=True)
    completed_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="quiz_attempts")


class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    assessment_type = Column(String(50), nullable=False)  # 'diabetes_type2', 'hypertension', 'cardio'
    inputs_json = Column(Text, nullable=False)
    risk_level = Column(String(50), nullable=False)  # 'Lower Educational Risk', 'Moderate...', 'Higher...'
    score = Column(Float, nullable=False)
    contributing_factors_json = Column(Text, nullable=True)
    recommendations_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="risk_assessments")


class MythFact(Base):
    __tablename__ = "myths_facts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    myth = Column(Text, nullable=False)
    fact = Column(Text, nullable=False)
    explanation = Column(Text, nullable=False)
    source = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False, index=True)
    keywords = Column(String(255), nullable=True)
    language = Column(String(10), default="en")
    created_at = Column(DateTime, default=datetime.utcnow)


class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    dosage = Column(String(50), nullable=False)  # e.g., '500mg'
    frequency = Column(String(50), nullable=False)  # e.g., 'Once daily', 'Twice daily'
    times_json = Column(String(100), nullable=False)  # JSON array e.g., ['08:00', '20:00']
    instructions = Column(String(255), nullable=True)  # e.g., 'Take with food'
    refill_date = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="medications")
    logs = relationship("MedicationLog", back_populates="medication", cascade="all, delete-orphan")


class MedicationLog(Base):
    __tablename__ = "medication_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    medication_id = Column(Integer, ForeignKey("medications.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    scheduled_date = Column(String(20), nullable=False)  # YYYY-MM-DD
    scheduled_time = Column(String(10), nullable=False)  # HH:MM
    status = Column(String(20), nullable=False)  # 'taken', 'skipped', 'pending'
    logged_at = Column(DateTime, default=datetime.utcnow)

    medication = relationship("Medication", back_populates="logs")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    provider_name = Column(String(100), nullable=False)
    specialty = Column(String(60), nullable=False)
    clinic_name = Column(String(150), nullable=False)
    appointment_date = Column(String(20), nullable=False)  # YYYY-MM-DD
    appointment_time = Column(String(10), nullable=False)  # HH:MM
    appointment_type = Column(String(30), default="In-Person")  # 'In-Person' or 'Telehealth'
    status = Column(String(20), default="scheduled")  # 'scheduled', 'completed', 'cancelled'
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="appointments")


class HealthcareService(Base):
    __tablename__ = "healthcare_services"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)  # 'hospital', 'clinic', 'pharmacy', 'laboratory', 'specialist'
    address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False, index=True)
    state = Column(String(50), nullable=True)
    postal_code = Column(String(20), nullable=True)
    phone = Column(String(50), nullable=False)
    emergency_available = Column(Boolean, default=False)
    open_hours = Column(String(100), default="24/7")
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    services_json = Column(Text, nullable=True)


class InsuranceFAQ(Base):
    __tablename__ = "insurance_faqs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    term = Column(String(100), nullable=False, index=True)
    definition = Column(Text, nullable=False)
    example = Column(Text, nullable=True)
    category = Column(String(50), default="General")
    created_at = Column(DateTime, default=datetime.utcnow)


class WellnessLog(Base):
    __tablename__ = "wellness_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    log_date = Column(String(20), nullable=False, index=True)  # YYYY-MM-DD
    mood = Column(String(30), nullable=False)  # 'great', 'good', 'okay', 'anxious', 'down'
    stress_level = Column(Integer, default=3)  # 1 to 5
    sleep_hours = Column(Float, default=7.0)
    water_glasses = Column(Integer, default=8)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="wellness_logs")


class WearableData(Base):
    __tablename__ = "wearable_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    record_date = Column(String(20), nullable=False, index=True)  # YYYY-MM-DD
    provider = Column(String(50), default="Mock Wearable")
    steps = Column(Integer, default=0)
    resting_heart_rate = Column(Integer, default=70)
    active_minutes = Column(Integer, default=30)
    sleep_minutes = Column(Integer, default=420)
    sleep_quality_score = Column(Integer, default=80)
    synced_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="wearable_records")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(200), nullable=False, unique=True)
    file_type = Column(String(20), nullable=False)  # 'pdf', 'txt', 'docx', 'json', 'csv'
    title = Column(String(200), nullable=False)
    category = Column(String(50), nullable=False)
    source_citation = Column(String(255), nullable=True)
    total_chunks = Column(Integer, default=0)
    is_indexed = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    metadata_json = Column(Text, nullable=True)  # document title, category, source, chunk page
    embedding_json = Column(Text, nullable=True)  # serialized float vector array for SQLite fallback
    created_at = Column(DateTime, default=datetime.utcnow)

    document = relationship("Document", back_populates="chunks")

    __table_args__ = (
        Index("idx_doc_chunk", "document_id", "chunk_index"),
    )


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=True, index=True)
    action = Column(String(50), nullable=False)  # 'LOGIN', 'LOGOUT', 'CHAT_QUERY', 'EMERGENCY_TRIGGERED', etc.
    resource = Column(String(100), nullable=True)
    ip_address = Column(String(50), nullable=True)
    status = Column(String(20), default="SUCCESS")
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
