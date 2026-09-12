"""
HealthAware AI - Comprehensive Database Seeder
Seeds Health Modules, Quizzes, Myths vs Facts, Healthcare Facilities,
Insurance FAQs, Demo Patient Data, and Ingests Knowledge Documents into Vector DB.
"""

import os
import json
import csv
import re
from pathlib import Path
from database.connection import get_db_session, init_db
from database.models import (
    HealthModule, QuizQuestion, MythFact, HealthcareService,
    InsuranceFAQ, Medication, Appointment, WellnessLog, WearableData
)
from database.models import Document
from auth.authentication import AuthService
from rag.ingestion import ingest_document


def seed_database():
    """Initializes schema and populates all standard healthcare awareness data."""
    init_db()
    AuthService.init_default_accounts()

    with get_db_session() as db:
        # ======================================================================
        # 1. SEED HEALTH LEARNING MODULES
        # ======================================================================
        if db.query(HealthModule).count() == 0:
            modules_data = [
                {
                    "slug": "diabetes-awareness",
                    "title": "Diabetes Awareness & Glucose Management",
                    "category": "Endocrine Health",
                    "icon": "🩸",
                    "estimated_mins": 6,
                    "description": "Learn the physiological mechanisms of diabetes, risk factors, subtle warning signs, and evidence-based preventive lifestyle choices.",
                    "summary": "Covers Type 1, Type 2, prediabetes benchmarks, HbA1c screening, and lifestyle modifications.",
                    "content_json": json.dumps({
                        "lessons": [
                            {
                                "title": "Understanding Insulin & Glucose",
                                "text": "Insulin is a hormone produced by beta cells in the pancreas. It acts like a key, unlocking body cells so circulating glucose can enter and provide cellular energy. In Type 2 diabetes, cells become resistant to insulin, causing glucose to accumulate in the bloodstream."
                            },
                            {
                                "title": "Common Warning Signs (The 3 P's)",
                                "text": "Classic warning symptoms include Polyuria (frequent urination), Polydipsia (excessive thirst), and Polyphagia (extreme hunger), along with unexplained fatigue, blurry vision, and slow-healing wounds."
                            },
                            {
                                "title": "Diagnostic Benchmarks & Screening",
                                "text": "Fasting Plasma Glucose: Normal < 100 mg/dL, Prediabetes 100-125 mg/dL, Diabetes >= 126 mg/dL. Hemoglobin A1c (HbA1c) measures your average blood sugar over 3 months: Normal < 5.7%, Prediabetes 5.7%-6.4%, Diabetes >= 6.5%."
                            },
                            {
                                "title": "Preventive Lifestyle Strategies",
                                "text": "A balanced dietary pattern emphasizing dietary fiber (vegetables, legumes, whole grains), at least 150 minutes of weekly moderate exercise, and modest 5-7% weight loss can reduce Type 2 diabetes onset by nearly 60%."
                            }
                        ],
                        "key_takeaways": [
                            "Prediabetes can often be reversed with sustainable lifestyle adjustments.",
                            "Routine blood glucose checks are critical because early diabetes is often asymptomatic.",
                            "Consult a physician if you experience frequent urination, extreme thirst, or persistent lethargy."
                        ]
                    })
                },
                {
                    "slug": "heart-health",
                    "title": "Heart Health & Hypertension Awareness",
                    "category": "Cardiovascular",
                    "icon": "❤️",
                    "estimated_mins": 5,
                    "description": "Understand blood pressure readings, cholesterol types, heart-healthy nutrition, and acute warning signs requiring emergency care.",
                    "summary": "Covers systolic/diastolic blood pressure, LDL vs HDL, DASH diet, exercise, and cardiac red flags.",
                    "content_json": json.dumps({
                        "lessons": [
                            {
                                "title": "The Mechanics of Blood Pressure",
                                "text": "Blood pressure measures the pressure of circulating blood against arterial walls. The top number (systolic) represents pressure during heartbeats; the bottom number (diastolic) represents pressure when the heart rests between beats. Normal blood pressure is under 120/80 mmHg."
                            },
                            {
                                "title": "The 'Silent Killer' Explained",
                                "text": "High blood pressure (Hypertension) often has zero noticeable symptoms while silently stressing the coronary arteries, kidneys, and brain. Consistent annual screenings are essential."
                            },
                            {
                                "title": "Cholesterol: LDL vs HDL",
                                "text": "LDL (Low-Density Lipoprotein) contributes to plaque buildup in arteries. HDL (High-Density Lipoprotein) scavenges excess cholesterol and transports it back to the liver for clearance."
                            },
                            {
                                "title": "Immediate Red-Flag Warning Signs",
                                "text": "Severe chest pressure, pain radiating to the left arm or jaw, shortness of breath, and sudden cold sweats are medical emergencies. Call 911, 112, or 108 immediately."
                            }
                        ],
                        "key_takeaways": [
                            "Adopt the DASH diet: lower sodium (<2300mg/day) and rich in potassium, magnesium, and fiber.",
                            "Engage in 150 minutes of moderate aerobic activity weekly.",
                            "Never ignore sudden chest tightness or unexplained shortness of breath."
                        ]
                    })
                },
                {
                    "slug": "vaccination-awareness",
                    "title": "Vaccination Concepts & Adult Immunization",
                    "category": "Preventive Health",
                    "icon": "💉",
                    "estimated_mins": 5,
                    "description": "Explore how vaccines train your immune system, the importance of community immunity, and routine adult vaccine boosters.",
                    "summary": "Covers immunology basics, Tdap, annual influenza, shingles (Shingrix), and safety monitoring.",
                    "content_json": json.dumps({
                        "lessons": [
                            {
                                "title": "How Vaccines Train the Immune System",
                                "text": "Vaccines introduce a harmless antigen or mRNA instruction that prompts your immune cells to develop antibodies and memory cells without causing the full-blown illness."
                            },
                            {
                                "title": "Community (Herd) Immunity",
                                "text": "When the vast majority of a community is immune, transmission slows down drastically, protecting newborns and individuals who are immunocompromised."
                            },
                            {
                                "title": "Essential Adult Boosters",
                                "text": "Adults benefit from an Annual Flu shot, a Tdap booster every 10 years, and the two-dose Shingrix vaccine once reaching age 50 to prevent painful shingles complications."
                            }
                        ],
                        "key_takeaways": [
                            "Vaccine safety is monitored continuously through international surveillance networks.",
                            "Mild symptoms like arm soreness or low-grade fever indicate your body is actively building antibodies.",
                            "Check with your doctor or pharmacist to confirm your personalized booster schedule."
                        ]
                    })
                },
                {
                    "slug": "seasonal-illness",
                    "title": "Seasonal Respiratory Illness & Prevention",
                    "category": "Infectious Disease",
                    "icon": "🤧",
                    "estimated_mins": 4,
                    "description": "Learn the clear differences between a common cold, influenza (flu), and when symptoms warrant prompt medical care.",
                    "summary": "Covers cold vs flu comparison, hygiene practices, fever management, and red flag symptoms.",
                    "content_json": json.dumps({
                        "lessons": [
                            {
                                "title": "Cold vs. Flu: Spotting the Difference",
                                "text": "A cold develops gradually with sneezing, runny nose, and mild fatigue. Influenza strikes abruptly within hours, causing high fevers, severe muscle aches, and profound exhaustion."
                            },
                            {
                                "title": "Hygiene & Prevention Habits",
                                "text": "Handwashing with soap for 20 seconds, covering coughs with your elbow, and staying home while symptomatic prevents community spread."
                            },
                            {
                                "title": "When to Seek Urgent Care",
                                "text": "Difficulty breathing, chest pain, a fever that spikes again after going away, or inability to keep fluids down are red flags requiring a doctor's examination."
                            }
                        ],
                        "key_takeaways": [
                            "Rest and ample hydration are the cornerstone of recovery from uncomplicated viral infections.",
                            "Antibiotics do NOT treat viral colds or influenza.",
                            "Seek medical attention if breathing becomes strained or confusion develops."
                        ]
                    })
                }
            ]
            for m in modules_data:
                mod = HealthModule(**m)
                db.add(mod)
            db.flush()

        # ======================================================================
        # 2. SEED INTERACTIVE QUIZZES
        # ======================================================================
        if db.query(QuizQuestion).count() == 0:
            quizzes_data = [
                {
                    "topic": "Heart Health",
                    "question": "Which of the following blood pressure readings is considered in the normal range for adults according to AHA guidelines?",
                    "options_json": json.dumps(["Less than 120/80 mmHg", "135/85 mmHg", "145/95 mmHg", "160/100 mmHg"]),
                    "correct_answer": "Less than 120/80 mmHg",
                    "explanation": "According to the American Heart Association (AHA), normal adult blood pressure is systolic below 120 mmHg AND diastolic below 80 mmHg.",
                    "difficulty": "easy"
                },
                {
                    "topic": "Heart Health",
                    "question": "Which type of cholesterol is often referred to as 'good cholesterol' because it helps remove excess cholesterol from the blood?",
                    "options_json": json.dumps(["HDL (High-Density Lipoprotein)", "LDL (Low-Density Lipoprotein)", "VLDL", "Triglycerides"]),
                    "correct_answer": "HDL (High-Density Lipoprotein)",
                    "explanation": "HDL scavenges excess cholesterol in the bloodstream and carries it back to the liver to be broken down and excreted.",
                    "difficulty": "easy"
                },
                {
                    "topic": "Heart Health",
                    "question": "What is the recommended minimum duration of moderate-intensity aerobic exercise per week for cardiovascular health?",
                    "options_json": json.dumps(["150 minutes", "30 minutes", "60 minutes", "300 minutes"]),
                    "correct_answer": "150 minutes",
                    "explanation": "Major health organizations recommend at least 150 minutes of moderate aerobic physical activity (such as brisk walking) per week.",
                    "difficulty": "medium"
                },
                {
                    "topic": "Diabetes",
                    "question": "What is the normal fasting plasma glucose benchmark for a healthy adult?",
                    "options_json": json.dumps(["Less than 100 mg/dL", "100 - 125 mg/dL", "126 - 150 mg/dL", "Over 200 mg/dL"]),
                    "correct_answer": "Less than 100 mg/dL",
                    "explanation": "A fasting blood sugar level under 100 mg/dL is normal. 100 to 125 mg/dL indicates prediabetes, and 126 mg/dL or higher indicates diabetes.",
                    "difficulty": "easy"
                },
                {
                    "topic": "Diabetes",
                    "question": "Which test provides an estimate of average blood sugar levels over the past 2 to 3 months?",
                    "options_json": json.dumps(["Hemoglobin A1c (HbA1c)", "Oral Glucose Tolerance Test", "Fasting Ketone Test", "Lipid Panel"]),
                    "correct_answer": "Hemoglobin A1c (HbA1c)",
                    "explanation": "HbA1c measures the percentage of blood sugar attached to hemoglobin in red blood cells, reflecting a 2-3 month glucose average.",
                    "difficulty": "medium"
                },
                {
                    "topic": "Diabetes",
                    "question": "Which of the following symptoms is commonly referred to as 'polyuria' in early diabetes awareness?",
                    "options_json": json.dumps(["Frequent urination", "Excessive hunger", "Extreme fatigue", "Blurred vision"]),
                    "correct_answer": "Frequent urination",
                    "explanation": "Polyuria is the clinical term for frequent or excessive urination caused by osmotic diuresis when the kidneys filter high amounts of glucose.",
                    "difficulty": "easy"
                },
                {
                    "topic": "Preventive Care",
                    "question": "How often should an adult generally receive a Td/Tdap (tetanus/diphtheria/pertussis) booster?",
                    "options_json": json.dumps(["Every 10 years", "Every year", "Every 5 years", "Only once in a lifetime"]),
                    "correct_answer": "Every 10 years",
                    "explanation": "Adults should receive a Td or Tdap booster every 10 years to maintain protective immunity against tetanus and diphtheria.",
                    "difficulty": "medium"
                },
                {
                    "topic": "Preventive Care",
                    "question": "True or False: Antibiotics are effective for treating viral colds and seasonal influenza.",
                    "options_json": json.dumps(["False", "True"]),
                    "correct_answer": "False",
                    "explanation": "Antibiotics only kill bacteria. Viral infections like colds, influenza, and COVID-19 do not respond to antibiotics.",
                    "difficulty": "easy"
                },
                {
                    "topic": "First Aid & Triage",
                    "question": "In the stroke recognition acronym 'F.A.S.T.', what does the letter 'S' represent?",
                    "options_json": json.dumps(["Slurred Speech", "Sudden Sweating", "Severe Stomachache", "Shortness of breath"]),
                    "correct_answer": "Slurred Speech",
                    "explanation": "FAST stands for Face drooping, Arm weakness, Speech difficulty (slurred speech), and Time to call emergency services.",
                    "difficulty": "easy"
                },
                {
                    "topic": "First Aid & Triage",
                    "question": "If an adult experiences crushing chest pain, radiating arm pain, and shortness of breath, what is the best immediate action?",
                    "options_json": json.dumps(["Call emergency services (e.g. 911/112) immediately", "Wait 24 hours to see if it passes", "Take a hot bath and rest", "Drink a glass of water and drive to a pharmacy"]),
                    "correct_answer": "Call emergency services (e.g. 911/112) immediately",
                    "explanation": "These are classic red-flag symptoms of an acute myocardial infarction (heart attack) requiring immediate emergency medical dispatch.",
                    "difficulty": "easy"
                }
            ]
            for q in quizzes_data:
                item = QuizQuestion(**q)
                db.add(item)
            db.flush()

        # ======================================================================
        # 3. SEED MYTH VS FACT DATABASE
        # ======================================================================
        if db.query(MythFact).count() == 0:
            myths_data = [
                {
                    "myth": "Eating sugar directly causes Type 2 diabetes.",
                    "fact": "Type 2 diabetes is caused by insulin resistance, complex genetics, and lifestyle factors, not by consuming sugar alone.",
                    "explanation": "While consuming excessive sugar-sweetened beverages contributes to caloric surplus and obesity (which increases diabetes risk), sugar itself does not directly trigger diabetes without other metabolic and genetic factors.",
                    "source": "American Diabetes Association (ADA)",
                    "category": "Nutrition",
                    "keywords": "sugar, diabetes, insulin, diet"
                },
                {
                    "myth": "If you feel fine, you don't have high blood pressure.",
                    "fact": "Hypertension is widely known as the 'silent killer' because it usually produces no noticeable symptoms until severe organ damage occurs.",
                    "explanation": "Most people with hypertension have no headaches, dizziness, or visible signs. The only definitive way to know your blood pressure is through routine clinical measurement.",
                    "source": "American Heart Association (AHA)",
                    "category": "Heart Health",
                    "keywords": "hypertension, blood pressure, silent killer"
                },
                {
                    "myth": "Vaccines give you the actual disease they are designed to prevent.",
                    "fact": "Approved vaccines contain inactivated, weakened, or recombinant components that cannot cause the illness in healthy individuals.",
                    "explanation": "Mild side effects like a low-grade fever or arm soreness are signs of the immune system actively generating antibodies, not an active infection.",
                    "source": "Centers for Disease Control and Prevention (CDC)",
                    "category": "Vaccines",
                    "keywords": "vaccines, immunity, flu shot"
                },
                {
                    "myth": "Antibiotics will quickly cure a severe chest cold or flu.",
                    "fact": "Antibiotics kill bacteria, whereas colds, flu, and bronchitis are predominantly caused by viruses.",
                    "explanation": "Taking antibiotics for viral respiratory infections provides no therapeutic benefit, can cause side effects like gastrointestinal upset, and accelerates antibiotic resistance.",
                    "source": "World Health Organization (WHO)",
                    "category": "Medications",
                    "keywords": "antibiotics, virus, bacteria, cold, flu"
                },
                {
                    "myth": "You only need to worry about heart health when you are past age 50.",
                    "fact": "Atherosclerosis and arterial plaque accumulation begin in early adulthood and build silently over decades.",
                    "explanation": "Cardiovascular risk is cumulative. Developing heart-healthy dietary habits, regular physical activity, and normal cholesterol levels in your 20s and 30s dramatically reduces cardiac events later in life.",
                    "source": "European Society of Cardiology (ESC)",
                    "category": "Heart Health",
                    "keywords": "heart, age, cholesterol, prevention"
                },
                {
                    "myth": "Natural supplements are always safe because they are plant-based.",
                    "fact": "Herbal supplements can have potent biochemical effects and dangerous interactions with prescription medications.",
                    "explanation": "For instance, St. John's Wort alters the metabolism of dozens of prescription drugs, and high doses of certain vitamins can cause liver or kidney toxicity. Always discuss supplements with your physician.",
                    "source": "National Institutes of Health (NIH - NCCAM)",
                    "category": "Nutrition",
                    "keywords": "supplements, herbs, natural, interactions"
                }
            ]
            for mf in myths_data:
                db.add(MythFact(**mf))
            db.flush()

        # ======================================================================
        # 4. SEED HEALTHCARE SERVICES DIRECTORY
        # ======================================================================
        if db.query(HealthcareService).count() == 0:
            services_data = [
                {
                    "name": "City General Hospital & Emergency Center",
                    "category": "hospital",
                    "address": "100 Medical Center Way",
                    "city": "Metropolis",
                    "state": "NY",
                    "postal_code": "10001",
                    "phone": "+1 (555) 019-2831",
                    "emergency_available": True,
                    "open_hours": "24/7",
                    "latitude": 40.7128,
                    "longitude": -74.0060,
                    "services_json": json.dumps(["Level 1 Trauma", "Emergency Cardiology", "ICU", "Pediatrics"])
                },
                {
                    "name": "Metro Urgent Care & Walk-in Clinic",
                    "category": "clinic",
                    "address": "450 Broadway Suite 2B",
                    "city": "Metropolis",
                    "state": "NY",
                    "postal_code": "10002",
                    "phone": "+1 (555) 014-9820",
                    "emergency_available": False,
                    "open_hours": "Mon-Sun: 8:00 AM - 10:00 PM",
                    "latitude": 40.7200,
                    "longitude": -74.0020,
                    "services_json": json.dumps(["Minor Injuries", "Rapid Flu/COVID Tests", "X-Ray", "Vaccinations"])
                },
                {
                    "name": "CareFirst 24-Hour Community Pharmacy",
                    "category": "pharmacy",
                    "address": "780 Lexington Avenue",
                    "city": "Metropolis",
                    "state": "NY",
                    "postal_code": "10021",
                    "phone": "+1 (555) 018-3412",
                    "emergency_available": False,
                    "open_hours": "24/7",
                    "latitude": 40.7650,
                    "longitude": -73.9680,
                    "services_json": json.dumps(["Prescription Dispensing", "Over-the-counter Drugs", "Immunizations"])
                },
                {
                    "name": "Apex Diagnostic & Pathology Laboratories",
                    "category": "laboratory",
                    "address": "210 Health Park Boulevard",
                    "city": "Metropolis",
                    "state": "NY",
                    "postal_code": "10016",
                    "phone": "+1 (555) 012-7788",
                    "emergency_available": False,
                    "open_hours": "Mon-Sat: 7:00 AM - 6:00 PM",
                    "latitude": 40.7450,
                    "longitude": -73.9780,
                    "services_json": json.dumps(["Fasting Glucose", "Lipid Profile", "Complete Blood Count", "HbA1c"])
                },
                {
                    "name": "Apollo Multi-Specialty Clinic",
                    "category": "clinic",
                    "address": "Jubilee Hills Road No. 36",
                    "city": "Hyderabad",
                    "state": "Telangana",
                    "postal_code": "500033",
                    "phone": "+91 40 2360 7777",
                    "emergency_available": True,
                    "open_hours": "24/7",
                    "latitude": 17.4325,
                    "longitude": 78.4071,
                    "services_json": json.dumps(["Cardiology", "Diabetology", "Emergency", "Pathology"])
                },
                {
                    "name": "MedPlus 24/7 Pharmacy & Wellness",
                    "category": "pharmacy",
                    "address": "Banjara Hills Road No. 12",
                    "city": "Hyderabad",
                    "state": "Telangana",
                    "postal_code": "500034",
                    "phone": "+91 40 6700 8800",
                    "emergency_available": False,
                    "open_hours": "24/7",
                    "latitude": 17.4156,
                    "longitude": 78.4483,
                    "services_json": json.dumps(["Medicines", "Medical Devices", "Home Delivery"])
                }
            ]
            for s in services_data:
                db.add(HealthcareService(**s))
            db.flush()

        # ======================================================================
        # 5. SEED INSURANCE FAQS
        # ======================================================================
        if db.query(InsuranceFAQ).count() == 0:
            insurance_data = [
                {
                    "term": "Deductible",
                    "definition": "The fixed dollar amount you must pay out-of-pocket for covered medical services before your insurance plan begins paying.",
                    "example": "If your annual deductible is $1,500, you pay 100% of your medical bills up to $1,500 before your insurance co-insurance kicks in.",
                    "category": "Cost Sharing"
                },
                {
                    "term": "Copayment (Copay)",
                    "definition": "A fixed flat fee you pay at the time of receiving a specific healthcare service or prescription medication.",
                    "example": "You might pay a $25 copay for a primary care doctor visit and a $10 copay for generic medications.",
                    "category": "Cost Sharing"
                },
                {
                    "term": "Coinsurance",
                    "definition": "The percentage of healthcare costs you pay after reaching your deductible, with your insurer paying the remaining percentage.",
                    "example": "In an 80/20 plan, once your deductible is satisfied, your insurer pays 80% of a covered procedure and you pay 20%.",
                    "category": "Cost Sharing"
                },
                {
                    "term": "Out-of-Pocket Maximum",
                    "definition": "The maximum amount you have to pay for covered services in a policy year. After reaching this cap, your insurance covers 100% of eligible costs.",
                    "example": "If your out-of-pocket maximum is $6,000, once your deductibles, copays, and coinsurance total $6,000, your plan pays all remaining covered medical expenses that year.",
                    "category": "Coverage Limits"
                },
                {
                    "term": "In-Network vs. Out-of-Network",
                    "definition": "In-network providers have negotiated discounted contracts with your insurance company. Out-of-network providers do not, leading to higher or uncovered expenses.",
                    "example": "Seeing an in-network lab may cost $30, while an out-of-network lab could cost $250 and may not apply toward your in-network deductible.",
                    "category": "Network Rules"
                },
                {
                    "term": "Explanation of Benefits (EOB)",
                    "definition": "A statement sent by your health insurer explaining what services were billed by your doctor, what portion was paid by insurance, and what you may owe.",
                    "example": "An EOB is NOT a medical bill. Wait for the medical provider's statement before making payments.",
                    "category": "Billing Concepts"
                }
            ]
            for inf in insurance_data:
                db.add(InsuranceFAQ(**inf))
            db.flush()

        # ======================================================================
        # 6. SEED DEMO USER HEALTHCARE DATA
        # ======================================================================
        from database.repositories import UserRepository
        demo_user = UserRepository.get_by_username(db, "demouser")
        if demo_user:
            # Seed demo medications
            if db.query(Medication).filter(Medication.user_id == demo_user.id).count() == 0:
                db.add(Medication(
                    user_id=demo_user.id,
                    name="Metformin",
                    dosage="500 mg",
                    frequency="Twice daily",
                    times_json=json.dumps(["08:00", "20:00"]),
                    instructions="Take with meals to minimize stomach upset.",
                    refill_date="2026-10-15"
                ))
                db.add(Medication(
                    user_id=demo_user.id,
                    name="Atorvastatin",
                    dosage="20 mg",
                    frequency="Once daily",
                    times_json=json.dumps(["21:00"]),
                    instructions="Take at bedtime as directed by doctor.",
                    refill_date="2026-11-01"
                ))
                db.flush()

            # Seed demo appointment
            if db.query(Appointment).filter(Appointment.user_id == demo_user.id).count() == 0:
                db.add(Appointment(
                    user_id=demo_user.id,
                    provider_name="Dr. Sarah Jenkins, MD",
                    specialty="General Medicine",
                    clinic_name="City Health Care Center",
                    appointment_date="2026-09-18",
                    appointment_time="10:30",
                    appointment_type="In-Person",
                    notes="Annual routine preventive wellness examination."
                ))
                db.flush()

            # Seed demo wearable record
            if db.query(WearableData).filter(WearableData.user_id == demo_user.id).count() == 0:
                from services.wearable_service import get_wearable_provider
                wp = get_wearable_provider()
                wear_records = wp.sync_data(demo_user.id, days=7)
                for r in wear_records:
                    db.add(WearableData(
                        user_id=demo_user.id,
                        record_date=r["record_date"],
                        provider=r["provider"],
                        steps=r["steps"],
                        resting_heart_rate=r["resting_heart_rate"],
                        active_minutes=r["active_minutes"],
                        sleep_minutes=r["sleep_minutes"],
                        sleep_quality_score=r["sleep_quality_score"]
                    ))
                db.flush()

        # ======================================================================
        # 7. INGEST STANDARD RAG DOCUMENTS
        # ======================================================================
        docs_dir = Path(__file__).resolve().parent.parent / "documents"
        if docs_dir.exists():
            allowed_exts = {".txt", ".csv", ".tsv", ".json"}
            for doc_file in sorted(docs_dir.iterdir()):
                if doc_file.suffix.lower() not in allowed_exts:
                    continue
                try:
                    if db.query(Document).filter(Document.filename == doc_file.name).first():
                        continue
                    with open(doc_file, "rb") as f:
                        file_bytes = f.read()
                    ingest_document(
                        db=db,
                        filename=doc_file.name,
                        file_bytes=file_bytes,
                        title=doc_file.stem.replace("_", " ").title(),
                        category="Clinical Guidelines"
                    )
                except Exception as e:
                    print(f"Error ingesting {doc_file.name}: {e}")

            dataset_files = [
                docs_dir / "who_disease_awareness.csv",
                docs_dir / "disease_awareness_index.tsv",
                Path(__file__).resolve().parent.parent.parent / "verified_disease_knowledge_dataset.csv",
            ]
            for dataset_file in dataset_files:
                if not dataset_file.exists():
                    continue
                try:
                    delimiter = "," if dataset_file.suffix.lower() == ".csv" else "\t"
                    with dataset_file.open("r", encoding="utf-8", newline="") as handle:
                        reader = csv.DictReader(handle, delimiter=delimiter)
                        for row in reader:
                            if not row:
                                continue
                            disease = (row.get("disease") or row.get("Disease") or "").strip()
                            if not disease:
                                continue
                            slug = re.sub(r"[^a-z0-9]+", "_", disease.lower()).strip("_")
                            is_verified_dataset = dataset_file.name == "verified_disease_knowledge_dataset.csv"
                            filename = f"verified_dataset_{slug}.txt" if is_verified_dataset else f"disease_{slug}.txt"
                            if db.query(Document).filter(Document.filename == filename).first():
                                continue
                            content = (
                                f"Disease: {disease}\n"
                                f"Category: {row.get('category') or row.get('Category') or 'General health'}\n"
                                f"Cause: {row.get('cause') or row.get('Cause') or 'See authoritative source'}\n"
                                f"Transmission: {row.get('transmission') or row.get('Transmission') or 'Varies by condition; see authoritative source'}\n"
                                f"Common symptoms: {row.get('common_symptoms') or row.get('Common symptoms') or 'See authoritative source; symptoms are not sufficient for diagnosis'}\n"
                                f"Prevention: {row.get('prevention') or row.get('Prevention') or 'Varies by condition; see authoritative source'}\n"
                                f"Medical note: {row.get('medical_note') or row.get('Medical note') or 'Health-awareness information only. This index is for retrieval/navigation, not diagnosis or prescribing.'}\n"
                                f"Source: {row.get('source') or row.get('Source') or 'Authoritative health source'}\n"
                                f"Source URL: {row.get('source_url') or row.get('Source URL') or ''}\n"
                            ).encode("utf-8")
                            ingest_document(
                                db=db,
                                filename=filename,
                                file_bytes=content,
                                title=f"Verified Dataset - {disease} Awareness" if is_verified_dataset else f"{disease} Awareness",
                                category=row.get('category') or row.get('Category') or 'General health',
                                source_citation=f"{row.get('source') or row.get('Source') or 'Authoritative health source'} - {row.get('source_url') or row.get('Source URL') or ''}"
                            )
                except Exception as e:
                    print(f"Error ingesting disease dataset {dataset_name}: {e}")

    print("[SUCCESS] HealthAware AI database successfully initialized and seeded.")


if __name__ == "__main__":
    seed_database()
