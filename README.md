# HealthAware AI - AI Healthcare Awareness & Wellness Platform

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B.svg)](https://streamlit.io/)
[![Zero JavaScript](https://img.shields.io/badge/JavaScript-None%20(0%25)-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests: Pytest](https://img.shields.io/badge/Tests-21%20Passed-success.svg)]()

> **Educational Notice:** HealthAware AI provides general healthcare awareness and educational information. It is **not a doctor** and does **not** provide definitive medical diagnosis, prescribe medications, alter dosages, or replace professional clinical advice. For emergencies, prioritize immediate emergency medical services (911, 112, 108).

---

## 1. Project Overview

**HealthAware AI** is a complete, production-grade healthcare awareness and wellness assistant built entirely with **Python and Streamlit**. It provides conversational access to evidence-grounded medical literature using Retrieval-Augmented Generation (RAG), strict multi-layer healthcare safety guardrails, acute emergency triage detection, and interactive wellness tools.

### Key Highlights
* **Zero JavaScript Principle:** 100% created using native Streamlit widgets and custom medical-grade CSS. No React, Node.js, npm, or external JS frameworks.
* **Dual Database Architecture:** Zero-configuration **SQLite + in-memory vector cosine similarity** for instant local execution, with full support for **PostgreSQL + pgvector** in production.
* **Resilient Multi-Provider LLM Engine:** Built-in offline knowledge synthesizer (`OfflineKnowledgeLLMProvider`) works 100% offline without API keys, alongside pluggable support for OpenAI, Gemini, and local Ollama models.
* **Rigorous Safety & Emergency Pipeline:** Pre-generation input validation, emergency red-flag triage, 988 crisis hotline escalations, diagnostic claim suppression, and mandatory healthcare disclaimers.

---

## 2. Main Application Modules

| # | Page / Module | Description |
| :--- | :--- | :--- |
| 1 | **Home Dashboard** (`app.py`) | Patient metrics, upcoming appointments, daily medication schedule, and quick feature navigation. |
| 2 | **AI Health Chat** (`pages/1_💬_AI_Health_Chat.py`) | Context-aware conversational RAG with verified citations, suggested prompts, voice audio upload, and feedback buttons. |
| 3 | **Health Learning** (`pages/2_📚_Health_Learning.py`) | Bite-sized educational modules covering Diabetes, Heart Health, Immunizations, and Seasonal Respiratory Illness. |
| 4 | **Interactive Quizzes** (`pages/3_📝_Interactive_Quizzes.py`) | Topic-based multiple choice quizzes with instant scientific explanations and score tracking. |
| 5 | **Risk Assessment** (`pages/4_⚖️_Risk_Assessment.py`) | Educational lifestyle risk calculators for Type 2 Diabetes (ADA model) and Hypertension. |
| 6 | **Myth vs Fact** (`pages/5_🔍_Myth_vs_Fact.py`) | Searchable evidence database debunking medical misinformation with verified citations. |
| 7 | **Symptom Checker** (`pages/6_🩺_Symptom_Checker.py`) | Guided clinical triage questionnaire classifying symptom urgency (Emergency, Urgent, Physician, Self-Care). |
| 8 | **Medications** (`pages/7_💊_Medications.py`) | Daily prescription schedules, taken/skipped adherence logging, and refill reminders. |
| 9 | **Appointments** (`pages/8_📅_Appointments.py`) | Clinic directory, doctor specialty selection, appointment booking, and cancellation. |
| 10 | **Healthcare Directory** (`pages/9_🏥_Healthcare_Directory.py`) | Search hospitals, clinics, 24/7 pharmacies, and diagnostic labs with external navigation directions. |
| 11 | **Insurance & Billing** (`pages/10_🛡️_Insurance_Billing.py`) | Demystifies deductibles, copays, coinsurance, EOB statements, and itemized hospital bill audits. |
| 12 | **Mental Wellness** (`pages/11_🧘_Mental_Wellness.py`) | Animated 4-7-8 box breathing pacer (pure CSS), mood check-in, journaling, and 24/7 crisis lifelines. |
| 13 | **Wearable Health Hub** (`pages/12_⌚_Wearable_Health.py`) | Wearable adapters (Apple Health, Fitbit, Google Health Connect) and FHIR-compliant demo EHR records. |
| 14 | **User Profile** (`pages/13_👤_Profile.py`) | Account settings, language preferences, JSON health data export, and account deletion (GDPR/HIPAA). |
| 15 | **Settings** (`pages/14_⚙️_Settings.py`) | LLM provider toggle (Offline, OpenAI, Ollama), vector DB selection, and accessibility options. |
| 16 | **Admin Portal** (`pages/15_🔒_Admin.py`) | Multi-format document upload (PDF, DOCX, TXT, JSON, CSV), vector index catalog, and audit trails. |

---

## 3. Technology Stack

* **Programming Language:** Python 3.11+
* **Frontend / User Interface:** Streamlit (Native components + medical design tokens)
* **ORM & Database:** SQLAlchemy 2.0+, SQLite (local) / PostgreSQL + pgvector (production)
* **Data Processing & Vectors:** NumPy, Pandas, Pydantic
* **Document Ingestion:** PyPDF (PDF extraction), python-docx (DOCX extraction), CSV, JSON
* **Testing:** Pytest (Unit and integration testing)

---

## 4. Safety & Triage Architecture

Every user interaction follows a mandatory multi-stage safety pipeline:

```
USER QUERY
    │
    ▼
[INPUT VALIDATION & SANITIZATION]  (blocks prompt injection, sanitizes length, masks PII)
    │
    ▼
[EMERGENCY DETECTION]              (detects severe chest pain, breathing difficulty, stroke FAST signs)
    ├─► If acute emergency: HALT -> Show red emergency alert with hotlines (911, 112, 108)
    │
    ▼
[CRISIS LIFELINE DETECTION]        (detects self-harm and acute distress)
    ├─► If crisis: HALT -> Display 988 Suicide & Crisis Lifeline resources
    │
    ▼
[SENTIMENT ANALYSIS]               (detects anxiety and distress to modulate response tone)
    │
    ▼
[RAG KNOWLEDGE RETRIEVAL]          (hybrid dense vector similarity + keyword search)
    │
    ▼
[LLM INFERENCE ENGINE]             (Offline Knowledge Synthesizer / OpenAI / Ollama)
    │
    ▼
[OUTPUT SAFETY VALIDATION]         (softens diagnostic claims, strips prescribing, appends disclaimer)
    │
    ▼
FINAL EVIDENCE-GROUNDED ANSWER + CITATIONS
```

---

## 5. Getting Started & Installation

### Prerequisites
* Python 3.11 or newer
* Git (optional)

### 1. Clone or Open the Repository
```bash
cd chatbot
```

### 2. Set Up a Virtual Environment
```bash
# Using standard venv:
python -m venv .venv
.venv\Scripts\activate      # On Windows
source .venv/bin/activate   # On Linux/macOS
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables (Optional)
Copy `.env.example` to `.env`:
```bash
copy .env.example .env      # On Windows
cp .env.example .env        # On Linux/macOS
```
*By default, the application runs 100% locally with SQLite and the built-in offline knowledge synthesizer. No external API keys are required for full functionality.*

### 5. Launch the Application
```bash
streamlit run app.py
```
The application will automatically initialize the database, seed all modules, quizzes, clinics, and pre-index the verified clinical documents. Open `http://localhost:8501` in your browser.

---

## 6. Pre-Configured Demo Accounts

For demonstration and grading evaluation, the database includes two pre-seeded accounts:

| Role | Username | Password | Privileges |
| :--- | :--- | :--- | :--- |
| **Demo Patient** | `demouser` | `User@123` | Active prescriptions, scheduled appointments, wearable activity stream. |
| **Administrator** | `admin` | `Admin@123` | Full access to Admin Portal, document ingestion, vector catalog, audit logs. |

*(Users can also browse in Guest mode or register new personal accounts).*

---

## 7. Running the Automated Test Suite

HealthAware AI includes automated tests covering authentication, RAG chunking and retrieval, emergency detection, medication adherence, and database repositories:

```bash
pytest tests/ -v
```

Expected output:
```text
tests/test_auth.py::test_password_hashing PASSED
tests/test_auth.py::test_user_registration_and_login PASSED
tests/test_chat.py::test_chat_normal_rag_query PASSED
tests/test_chat.py::test_chat_emergency_query_triggers_alert PASSED
tests/test_database.py::test_healthcare_directory_repository PASSED
tests/test_database.py::test_insurance_faqs_repository PASSED
tests/test_database.py::test_myth_fact_repository PASSED
tests/test_database.py::test_audit_logging PASSED
tests/test_medications.py::test_medication_crud_and_adherence PASSED
tests/test_rag.py::test_text_chunking PASSED
tests/test_rag.py::test_embedding_vector_generation PASSED
tests/test_rag.py::test_knowledge_retrieval PASSED
tests/test_risk_assessment.py::test_diabetes_risk_calculation PASSED
tests/test_risk_assessment.py::test_risk_assessment_repository_persistence PASSED
tests/test_safety.py::test_emergency_detection_acute_chest_pain PASSED
tests/test_safety.py::test_emergency_detection_stroke_signs PASSED
tests/test_safety.py::test_normal_query_not_emergency PASSED
tests/test_safety.py::test_crisis_detection_self_harm PASSED
tests/test_safety.py::test_input_validation_prompt_injection PASSED
tests/test_safety.py::test_output_validation_disclaimer_enforcement PASSED
tests/test_safety.py::test_output_validation_softens_diagnosis PASSED
============================== 21 passed in 2.75s ==============================
```

---

## 8. Multi-Format Document Ingestion Guide

Administrators can upload new clinical documentation directly via the Admin Portal (`pages/15_🔒_Admin.py`):
1. Sign in as `admin` (`Admin@123`).
2. Navigate to the **Admin Portal** page.
3. Under **Document Ingestion**, upload any `.pdf`, `.docx`, `.txt`, `.json`, or `.csv` file.
4. The system automatically extracts text, chunks the content with metadata, generates vector embeddings, and updates the active knowledge base.
5. The conversational chatbot immediately retrieves from the new literature!

---

## 9. Docker Deployment

To build and run with Docker:

```bash
docker build -t healthaware-ai .
docker run -p 8501:8501 healthaware-ai
```

Access the containerized application at `http://localhost:8501`.

---

## 10. Medical Disclaimer

This software application is developed solely for health awareness and educational purposes. It is not a medical device, diagnostic tool, or clinical prescription platform. It does not replace the relationship between patients and their physicians. In the event of a medical emergency, immediately contact your local emergency response service (911 in the US/Canada, 112 in Europe/India, 108 in India).
