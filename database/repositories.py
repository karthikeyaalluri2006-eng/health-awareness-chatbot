"""
HealthAware AI - Database Repositories
Clean repository abstraction layer for interacting with all models.
"""

import json
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from database.models import (
    User, Conversation, Message, HealthModule, UserModuleProgress,
    QuizQuestion, QuizAttempt, RiskAssessment, MythFact,
    Medication, MedicationLog, Appointment, HealthcareService,
    InsuranceFAQ, WellnessLog, WearableData, Document, DocumentChunk, AuditLog
)


# ==============================================================================
# USER REPOSITORY
# ==============================================================================
class UserRepository:
    @staticmethod
    def create(db: Session, username: str, email: str, password_hash: str, full_name: str = "", role: str = "user", language: str = "en") -> User:
        user = User(
            username=username.lower().strip(),
            email=email.lower().strip(),
            password_hash=password_hash,
            full_name=full_name.strip(),
            role=role,
            preferred_language=language
        )
        db.add(user)
        db.flush()
        return user

    @staticmethod
    def get_by_username(db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username.lower().strip()).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email.lower().strip()).first()

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def update_preferences(db: Session, user_id: int, full_name: str = None, language: str = None) -> Optional[User]:
        user = UserRepository.get_by_id(db, user_id)
        if user:
            if full_name is not None:
                user.full_name = full_name
            if language is not None:
                user.preferred_language = language
            db.flush()
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        user = UserRepository.get_by_id(db, user_id)
        if user:
            db.delete(user)
            db.flush()
            return True
        return False


# ==============================================================================
# CHAT & CONVERSATION REPOSITORY
# ==============================================================================
class ChatRepository:
    @staticmethod
    def create_conversation(db: Session, user_id: int, title: str = "Health Consultation", language: str = "en") -> Conversation:
        conv = Conversation(user_id=user_id, title=title, language=language)
        db.add(conv)
        db.flush()
        return conv

    @staticmethod
    def get_user_conversations(db: Session, user_id: int) -> List[Conversation]:
        return db.query(Conversation).filter(Conversation.user_id == user_id).order_by(desc(Conversation.updated_at)).all()

    @staticmethod
    def get_conversation_by_id(db: Session, conv_id: int) -> Optional[Conversation]:
        return db.query(Conversation).filter(Conversation.id == conv_id).first()

    @staticmethod
    def delete_conversation(db: Session, conv_id: int) -> bool:
        conv = ChatRepository.get_conversation_by_id(db, conv_id)
        if conv:
            db.delete(conv)
            db.flush()
            return True
        return False

    @staticmethod
    def add_message(
        db: Session,
        conversation_id: int,
        role: str,
        content: str,
        sources: Optional[List[Dict[str, Any]]] = None,
        sentiment: Optional[str] = None
    ) -> Message:
        sources_str = json.dumps(sources) if sources else None
        msg = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            sources_json=sources_str,
            sentiment=sentiment
        )
        db.add(msg)
        # Update conversation timestamp
        conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if conv:
            conv.updated_at = datetime.utcnow()
            # If default title, update title using first words of user query
            if conv.title == "New Health Consultation" and role == "user":
                conv.title = content[:40] + ("..." if len(content) > 40 else "")
        db.flush()
        return msg

    @staticmethod
    def get_messages(db: Session, conversation_id: int) -> List[Message]:
        return db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at).all()

    @staticmethod
    def update_feedback(db: Session, message_id: int, feedback: int) -> bool:
        msg = db.query(Message).filter(Message.id == message_id).first()
        if msg:
            msg.feedback = feedback
            db.flush()
            return True
        return False


# ==============================================================================
# HEALTH MODULES REPOSITORY
# ==============================================================================
class HealthModuleRepository:
    @staticmethod
    def get_all(db: Session) -> List[HealthModule]:
        return db.query(HealthModule).order_by(HealthModule.id).all()

    @staticmethod
    def get_by_slug(db: Session, slug: str) -> Optional[HealthModule]:
        return db.query(HealthModule).filter(HealthModule.slug == slug).first()

    @staticmethod
    def get_user_progress(db: Session, user_id: int, module_id: int) -> Optional[UserModuleProgress]:
        return db.query(UserModuleProgress).filter(
            UserModuleProgress.user_id == user_id,
            UserModuleProgress.module_id == module_id
        ).first()

    @staticmethod
    def update_progress(db: Session, user_id: int, module_id: int, step: int, completed: bool = False) -> UserModuleProgress:
        progress = HealthModuleRepository.get_user_progress(db, user_id, module_id)
        if not progress:
            progress = UserModuleProgress(user_id=user_id, module_id=module_id, current_step=step, completed=completed)
            db.add(progress)
        else:
            progress.current_step = max(progress.current_step, step)
            if completed:
                progress.completed = True
        db.flush()
        return progress

    @staticmethod
    def get_user_completion_count(db: Session, user_id: int) -> int:
        return db.query(UserModuleProgress).filter(
            UserModuleProgress.user_id == user_id,
            UserModuleProgress.completed == True
        ).count()


# ==============================================================================
# QUIZ REPOSITORY
# ==============================================================================
class QuizRepository:
    @staticmethod
    def get_topics(db: Session) -> List[str]:
        results = db.query(QuizQuestion.topic).distinct().all()
        return [r[0] for r in results]

    @staticmethod
    def get_questions_by_topic(db: Session, topic: str, limit: int = 5) -> List[QuizQuestion]:
        query = db.query(QuizQuestion)
        if topic and topic.lower() != "all":
            query = query.filter(QuizQuestion.topic == topic)
        return query.order_by(func.random()).limit(limit).all()

    @staticmethod
    def save_attempt(db: Session, user_id: int, topic: str, score: int, total_questions: int, answers: dict) -> QuizAttempt:
        attempt = QuizAttempt(
            user_id=user_id,
            topic=topic,
            score=score,
            total_questions=total_questions,
            answers_json=json.dumps(answers)
        )
        db.add(attempt)
        db.flush()
        return attempt

    @staticmethod
    def get_user_recent_attempt(db: Session, user_id: int) -> Optional[QuizAttempt]:
        return db.query(QuizAttempt).filter(QuizAttempt.user_id == user_id).order_by(desc(QuizAttempt.completed_at)).first()

    @staticmethod
    def get_user_attempts(db: Session, user_id: int) -> List[QuizAttempt]:
        return db.query(QuizAttempt).filter(QuizAttempt.user_id == user_id).order_by(desc(QuizAttempt.completed_at)).all()


# ==============================================================================
# RISK ASSESSMENT REPOSITORY
# ==============================================================================
class RiskAssessmentRepository:
    @staticmethod
    def save_assessment(
        db: Session,
        user_id: int,
        assessment_type: str,
        inputs: dict,
        risk_level: str,
        score: float,
        factors: list,
        recommendations: list
    ) -> RiskAssessment:
        record = RiskAssessment(
            user_id=user_id,
            assessment_type=assessment_type,
            inputs_json=json.dumps(inputs),
            risk_level=risk_level,
            score=score,
            contributing_factors_json=json.dumps(factors),
            recommendations_json=json.dumps(recommendations)
        )
        db.add(record)
        db.flush()
        return record

    @staticmethod
    def get_user_assessments(db: Session, user_id: int) -> List[RiskAssessment]:
        return db.query(RiskAssessment).filter(RiskAssessment.user_id == user_id).order_by(desc(RiskAssessment.created_at)).all()


# ==============================================================================
# MYTH VS FACT REPOSITORY
# ==============================================================================
class MythFactRepository:
    @staticmethod
    def get_all(db: Session, category: Optional[str] = None, search: Optional[str] = None) -> List[MythFact]:
        query = db.query(MythFact)
        if category and category.lower() != "all":
            query = query.filter(MythFact.category == category)
        if search:
            search_term = f"%{search.lower()}%"
            query = query.filter(
                (func.lower(MythFact.myth).like(search_term)) |
                (func.lower(MythFact.fact).like(search_term)) |
                (func.lower(MythFact.explanation).like(search_term))
            )
        return query.all()

    @staticmethod
    def get_categories(db: Session) -> List[str]:
        results = db.query(MythFact.category).distinct().all()
        return [r[0] for r in results]

    @staticmethod
    def get_random(db: Session) -> Optional[MythFact]:
        return db.query(MythFact).order_by(func.random()).first()


# ==============================================================================
# MEDICATION REPOSITORY
# ==============================================================================
class MedicationRepository:
    @staticmethod
    def add(db: Session, user_id: int, name: str, dosage: str, frequency: str, times: List[str], instructions: str = "", refill_date: str = "") -> Medication:
        med = Medication(
            user_id=user_id,
            name=name.strip(),
            dosage=dosage.strip(),
            frequency=frequency,
            times_json=json.dumps(times),
            instructions=instructions.strip(),
            refill_date=refill_date
        )
        db.add(med)
        db.flush()
        return med

    @staticmethod
    def get_user_medications(db: Session, user_id: int, active_only: bool = True) -> List[Medication]:
        query = db.query(Medication).filter(Medication.user_id == user_id)
        if active_only:
            query = query.filter(Medication.is_active == True)
        return query.order_by(Medication.name).all()

    @staticmethod
    def delete(db: Session, med_id: int, user_id: int) -> bool:
        med = db.query(Medication).filter(Medication.id == med_id, Medication.user_id == user_id).first()
        if med:
            db.delete(med)
            db.flush()
            return True
        return False

    @staticmethod
    def log_status(db: Session, med_id: int, user_id: int, sched_date: str, sched_time: str, status: str) -> MedicationLog:
        log = db.query(MedicationLog).filter(
            MedicationLog.medication_id == med_id,
            MedicationLog.scheduled_date == sched_date,
            MedicationLog.scheduled_time == sched_time
        ).first()

        if log:
            log.status = status
            log.logged_at = datetime.utcnow()
        else:
            log = MedicationLog(
                medication_id=med_id,
                user_id=user_id,
                scheduled_date=sched_date,
                scheduled_time=sched_time,
                status=status
            )
            db.add(log)
        db.flush()
        return log

    @staticmethod
    def get_adherence_rate(db: Session, user_id: int, days: int = 7) -> float:
        start_date = (date.today() - timedelta(days=days)).isoformat()
        total_logs = db.query(MedicationLog).filter(
            MedicationLog.user_id == user_id,
            MedicationLog.scheduled_date >= start_date
        ).count()
        if total_logs == 0:
            return 100.0  # default when no logs yet
        taken_logs = db.query(MedicationLog).filter(
            MedicationLog.user_id == user_id,
            MedicationLog.scheduled_date >= start_date,
            MedicationLog.status == "taken"
        ).count()
        return round((taken_logs / total_logs) * 100, 1)


# ==============================================================================
# APPOINTMENT REPOSITORY
# ==============================================================================
class AppointmentRepository:
    @staticmethod
    def create(db: Session, user_id: int, provider: str, specialty: str, clinic: str, appt_date: str, appt_time: str, appt_type: str = "In-Person", notes: str = "") -> Appointment:
        appt = Appointment(
            user_id=user_id,
            provider_name=provider,
            specialty=specialty,
            clinic_name=clinic,
            appointment_date=appt_date,
            appointment_time=appt_time,
            appointment_type=appt_type,
            notes=notes
        )
        db.add(appt)
        db.flush()
        return appt

    @staticmethod
    def get_user_appointments(db: Session, user_id: int) -> List[Appointment]:
        return db.query(Appointment).filter(Appointment.user_id == user_id).order_by(Appointment.appointment_date, Appointment.appointment_time).all()

    @staticmethod
    def get_upcoming(db: Session, user_id: int) -> Optional[Appointment]:
        today_str = date.today().isoformat()
        return db.query(Appointment).filter(
            Appointment.user_id == user_id,
            Appointment.appointment_date >= today_str,
            Appointment.status == "scheduled"
        ).order_by(Appointment.appointment_date, Appointment.appointment_time).first()

    @staticmethod
    def cancel(db: Session, appt_id: int, user_id: int) -> bool:
        appt = db.query(Appointment).filter(Appointment.id == appt_id, Appointment.user_id == user_id).first()
        if appt:
            appt.status = "cancelled"
            db.flush()
            return True
        return False


# ==============================================================================
# HEALTHCARE DIRECTORY REPOSITORY
# ==============================================================================
class HealthcareServiceRepository:
    @staticmethod
    def get_all(db: Session, category: Optional[str] = None, city: Optional[str] = None, search: Optional[str] = None) -> List[HealthcareService]:
        query = db.query(HealthcareService)
        if category and category.lower() != "all":
            query = query.filter(HealthcareService.category == category)
        if city and city.lower() != "all":
            query = query.filter(HealthcareService.city == city)
        if search:
            s = f"%{search.lower()}%"
            query = query.filter(
                (func.lower(HealthcareService.name).like(s)) |
                (func.lower(HealthcareService.address).like(s))
            )
        return query.all()

    @staticmethod
    def get_cities(db: Session) -> List[str]:
        results = db.query(HealthcareService.city).distinct().all()
        return [r[0] for r in results if r[0]]


# ==============================================================================
# INSURANCE FAQ REPOSITORY
# ==============================================================================
class InsuranceFAQRepository:
    @staticmethod
    def get_all(db: Session, category: Optional[str] = None, search: Optional[str] = None) -> List[InsuranceFAQ]:
        query = db.query(InsuranceFAQ)
        if category and category.lower() != "all":
            query = query.filter(InsuranceFAQ.category == category)
        if search:
            s = f"%{search.lower()}%"
            query = query.filter(
                (func.lower(InsuranceFAQ.term).like(s)) |
                (func.lower(InsuranceFAQ.definition).like(s))
            )
        return query.all()


# ==============================================================================
# WELLNESS & WEARABLE REPOSITORY
# ==============================================================================
class WellnessRepository:
    @staticmethod
    def log(db: Session, user_id: int, log_date: str, mood: str, stress: int, sleep: float, water: int, notes: str = "") -> WellnessLog:
        log = db.query(WellnessLog).filter(
            WellnessLog.user_id == user_id,
            WellnessLog.log_date == log_date
        ).first()

        if log:
            log.mood = mood
            log.stress_level = stress
            log.sleep_hours = sleep
            log.water_glasses = water
            log.notes = notes
        else:
            log = WellnessLog(
                user_id=user_id,
                log_date=log_date,
                mood=mood,
                stress_level=stress,
                sleep_hours=sleep,
                water_glasses=water,
                notes=notes
            )
            db.add(log)
        db.flush()
        return log

    @staticmethod
    def get_recent(db: Session, user_id: int, limit: int = 7) -> List[WellnessLog]:
        return db.query(WellnessLog).filter(WellnessLog.user_id == user_id).order_by(desc(WellnessLog.log_date)).limit(limit).all()


class WearableRepository:
    @staticmethod
    def add_record(db: Session, user_id: int, record_date: str, provider: str, steps: int, hr: int, active_mins: int, sleep_mins: int, quality: int) -> WearableData:
        rec = db.query(WearableData).filter(
            WearableData.user_id == user_id,
            WearableData.record_date == record_date
        ).first()

        if rec:
            rec.provider = provider
            rec.steps = steps
            rec.resting_heart_rate = hr
            rec.active_minutes = active_mins
            rec.sleep_minutes = sleep_mins
            rec.sleep_quality_score = quality
            rec.synced_at = datetime.utcnow()
        else:
            rec = WearableData(
                user_id=user_id,
                record_date=record_date,
                provider=provider,
                steps=steps,
                resting_heart_rate=hr,
                active_minutes=active_mins,
                sleep_minutes=sleep_mins,
                sleep_quality_score=quality
            )
            db.add(rec)
        db.flush()
        return rec

    @staticmethod
    def get_recent(db: Session, user_id: int, days: int = 7) -> List[WearableData]:
        return db.query(WearableData).filter(WearableData.user_id == user_id).order_by(desc(WearableData.record_date)).limit(days).all()


# ==============================================================================
# RAG DOCUMENT REPOSITORY
# ==============================================================================
class DocumentRepository:
    @staticmethod
    def add_document(db: Session, filename: str, file_type: str, title: str, category: str, source_citation: str = "") -> Document:
        doc = db.query(Document).filter(Document.filename == filename).first()
        if not doc:
            doc = Document(
                filename=filename,
                file_type=file_type,
                title=title,
                category=category,
                source_citation=source_citation,
                total_chunks=0
            )
            db.add(doc)
            db.flush()
        return doc

    @staticmethod
    def add_chunks(db: Session, document_id: int, chunks: List[Dict[str, Any]]) -> int:
        count = 0
        for item in chunks:
            chunk = DocumentChunk(
                document_id=document_id,
                chunk_index=item["chunk_index"],
                content=item["content"],
                metadata_json=json.dumps(item.get("metadata", {})),
                embedding_json=json.dumps(item.get("embedding", []))
            )
            db.add(chunk)
            count += 1
        doc = db.query(Document).filter(Document.id == document_id).first()
        if doc:
            doc.total_chunks = count
            doc.is_indexed = True
        db.flush()
        return count

    @staticmethod
    def get_all_chunks(db: Session) -> List[DocumentChunk]:
        return db.query(DocumentChunk).all()

    @staticmethod
    def get_all_documents(db: Session) -> List[Document]:
        return db.query(Document).order_by(desc(Document.created_at)).all()

    @staticmethod
    def delete_document(db: Session, doc_id: int) -> bool:
        doc = db.query(Document).filter(Document.id == doc_id).first()
        if doc:
            db.delete(doc)
            db.flush()
            return True
        return False


# ==============================================================================
# AUDIT LOG REPOSITORY
# ==============================================================================
class AuditLogRepository:
    @staticmethod
    def log(db: Session, action: str, user_id: Optional[int] = None, resource: str = "", ip_address: str = "127.0.0.1", status: str = "SUCCESS", details: str = "") -> AuditLog:
        entry = AuditLog(
            user_id=user_id,
            action=action,
            resource=resource,
            ip_address=ip_address,
            status=status,
            details=details[:500] if details else None
        )
        db.add(entry)
        db.flush()
        return entry

    @staticmethod
    def get_recent(db: Session, limit: int = 50) -> List[AuditLog]:
        return db.query(AuditLog).order_by(desc(AuditLog.created_at)).limit(limit).all()
