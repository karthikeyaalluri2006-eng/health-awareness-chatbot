"""
HealthAware AI - Intelligent Offline Healthcare Knowledge Engine
A topic-aware, context-driven LLM replacement that delivers real, useful,
well-structured healthcare educational responses without any external API.
Supports OpenAI and Ollama when API keys are configured.
"""

import os
import re
from typing import Optional
import requests
from dotenv import load_dotenv
from rag.prompts import HEALTH_SYSTEM_PROMPT

load_dotenv()


class LLMProvider:
    """Abstract base class for all LLM providers."""
    def generate_response(
        self,
        prompt: str,
        system_prompt: str = HEALTH_SYSTEM_PROMPT,
        temperature: float = 0.3,
        max_tokens: int = 900
    ) -> str:
        raise NotImplementedError


# ==============================================================================
# HEALTHCARE KNOWLEDGE BASE — topic-aware response library
# ==============================================================================
HEALTH_KNOWLEDGE = {
    # ── DIABETES ──────────────────────────────────────────────────────────────
    "diabetes": {
        "keywords": ["diabetes", "diabetic", "blood sugar", "glucose", "insulin", "hba1c", "type 2", "type 1", "hyperglycemia", "prediabetes", "diabetes symptom", "diabetic symptom", "signs of diabetes", "symptoms of diabetes"],
        "response": """
## 🩸 Diabetes — What You Need to Know

Diabetes is a chronic condition where the body cannot properly regulate blood glucose (sugar) levels, either because the pancreas doesn't produce enough insulin or because cells don't respond to it effectively.

### 📌 Key Types
| Type | Cause | Notes |
|------|-------|-------|
| **Type 1** | Immune system destroys insulin-producing cells | Often diagnosed in children/teens |
| **Type 2** | Cells become insulin-resistant | Most common (90%+); strongly lifestyle-linked |
| **Prediabetes** | Blood sugar higher than normal but not yet diabetic | Reversible with lifestyle changes |
| **Gestational** | Develops during pregnancy | Usually resolves after delivery |

### ⚠️ Common Warning Signs (The "3 P's" + more)
- 🚰 **Polyuria** — Frequent urination, especially at night
- 💧 **Polydipsia** — Excessive thirst you can't quench
- 🍽️ **Polyphagia** — Unusual or extreme hunger even after eating
- 😴 Persistent unexplained fatigue
- 👁️ Blurry vision
- 🩹 Slow-healing cuts or wounds
- 🦶 Tingling or numbness in hands/feet

### 🔬 Diagnostic Benchmarks (ADA Guidelines)
| Marker | Normal | Prediabetes | Diabetes |
|--------|--------|-------------|---------|
| **Fasting Glucose** | < 100 mg/dL | 100–125 mg/dL | ≥ 126 mg/dL |
| **HbA1c** | < 5.7% | 5.7%–6.4% | ≥ 6.5% |
| **Random Glucose** | — | — | ≥ 200 mg/dL with symptoms |

### 💪 Prevention & Management Strategies
- **Healthy diet** — Focus on whole grains, vegetables, lean proteins; limit refined sugars and processed carbs
- **Regular exercise** — Aim for 150 min/week of moderate aerobic activity (walking, cycling)
- **Weight management** — Even a 5–7% reduction in body weight can reduce Type 2 diabetes risk by ~58%
- **Regular monitoring** — Routine HbA1c and fasting glucose checks as recommended by your doctor
- **Medication adherence** — If prescribed, take medications consistently

### 🏥 When to See a Doctor
Schedule an appointment if you experience any of the warning signs above, especially if you have risk factors such as family history of diabetes, obesity, or are over 45 years old.

> **⚕️ Educational Notice:** This information is for awareness only. Only a licensed physician can diagnose diabetes and create a personalized treatment plan.
""",
    },

    # ── HYPERTENSION / BLOOD PRESSURE ─────────────────────────────────────
    "hypertension": {
        "keywords": ["hypertension", "blood pressure", "high bp", "systolic", "diastolic", "mmhg", "heart attack", "stroke risk"],
        "response": """
## ❤️ High Blood Pressure (Hypertension) — Complete Guide

High blood pressure (hypertension) is often called the **"silent killer"** because it typically has no symptoms, yet silently damages your arteries, heart, kidneys, and brain over time.

### 📊 Blood Pressure Classification (AHA Guidelines)
| Category | Systolic | | Diastolic |
|----------|----------|---|-----------|
| **Normal** | < 120 mmHg | AND | < 80 mmHg |
| **Elevated** | 120–129 mmHg | AND | < 80 mmHg |
| **Stage 1 Hypertension** | 130–139 mmHg | OR | 80–89 mmHg |
| **Stage 2 Hypertension** | ≥ 140 mmHg | OR | ≥ 90 mmHg |
| **Hypertensive Crisis** | > 180 mmHg | AND/OR | > 120 mmHg — **SEEK EMERGENCY CARE** |

### ⚠️ Risk Factors
- Family history of heart disease or hypertension
- Age (risk increases after 45 for men, 65 for women)
- Obesity or overweight
- High salt/sodium diet
- Physical inactivity
- Heavy alcohol consumption
- Smoking or tobacco use
- Chronic kidney disease or diabetes

### 💡 Symptoms (usually absent — why monitoring matters)
- Severe headache (during hypertensive crisis)
- Shortness of breath
- Nosebleeds
- Visual changes (rare, in severe cases)

### 🌿 Natural Prevention & Control Strategies
1. **DASH Diet** — Reduce sodium to < 2,300 mg/day; eat fruits, vegetables, low-fat dairy
2. **Exercise** — 30 minutes of moderate aerobic exercise most days
3. **Weight loss** — Losing even 5 kg can significantly lower blood pressure
4. **Limit alcohol** — No more than 1–2 standard drinks/day
5. **Quit smoking** — Smoking raises blood pressure and multiplies cardiovascular risk
6. **Stress management** — Meditation, yoga, deep breathing exercises
7. **Adequate sleep** — 7–9 hours per night

### 🏥 When to Consult a Doctor
- Blood pressure consistently ≥ 130/80 mmHg on multiple readings
- Family history of early heart disease
- Already diagnosed with kidney disease or diabetes

> **⚕️ Educational Notice:** Do not self-medicate or adjust prescribed blood pressure medications without medical guidance.
""",
    },

    # ── HEART DISEASE ─────────────────────────────────────────────────────
    "heart": {
        "keywords": ["heart disease", "heart attack", "cardiac", "cholesterol", "ldl", "hdl", "cardiovascular", "angina", "coronary", "heart failure", "prevent heart"],
        "response": """
## 🫀 Heart Health & Cardiovascular Disease Prevention

Heart disease is the leading cause of death globally, but up to **80% of cases are preventable** through lifestyle changes and awareness.

### 🔍 Understanding Cholesterol
| Type | Role | Target Level |
|------|------|-------------|
| **LDL** (Bad Cholesterol) | Builds plaque in arteries | < 100 mg/dL (optimal) |
| **HDL** (Good Cholesterol) | Removes LDL from bloodstream | > 60 mg/dL (protective) |
| **Total Cholesterol** | Overall measurement | < 200 mg/dL (desirable) |
| **Triglycerides** | Blood fats linked to heart risk | < 150 mg/dL |

### 🚨 Heart Attack Warning Signs (Act Immediately — Call 112/911)
- **Chest pain or pressure** — feels like squeezing, fullness, or tightness
- **Pain radiating** to arm, neck, jaw, shoulder, or back
- **Shortness of breath** — may occur with or without chest discomfort
- **Cold sweats, nausea, or light-headedness**
- **Sudden unusual fatigue** (especially in women)

> 🆘 **If you or someone near you has these symptoms, call emergency services immediately. Every minute matters.**

### 💪 Heart Disease Prevention Strategies
1. **Heart-Healthy Diet (Mediterranean/DASH)**
   - Increase: Fruits, vegetables, whole grains, legumes, nuts, olive oil, fatty fish (omega-3)
   - Reduce: Saturated fats, trans fats, salt, processed meats, refined sugars

2. **Physical Activity**
   - ≥ 150 min/week of moderate exercise (brisk walking, swimming, cycling)
   - Include strength training 2 days/week

3. **Quit Smoking** — Smoking doubles the risk of heart disease

4. **Control Blood Pressure & Cholesterol** — Regular medical checks; medication if prescribed

5. **Manage Diabetes** — Uncontrolled blood sugar accelerates arterial damage

6. **Maintain Healthy Weight** — BMI 18.5–24.9 minimizes heart strain

7. **Limit Alcohol** — No more than 1 drink/day for women, 2 for men

8. **Manage Stress** — Chronic stress elevates cortisol, raising blood pressure

### 📅 Recommended Screenings (Adults)
- **Blood pressure** — Every 1–2 years (more often if elevated)
- **Cholesterol panel** — Every 4–6 years; annually if at risk
- **Blood glucose/HbA1c** — Every 3 years from age 35–70
- **BMI assessment** — At every annual check-up

> **⚕️ Educational Notice:** Chest pain, especially with exertion, is a medical emergency. Always consult a cardiologist for personalized risk assessment.
""",
    },

    # ── SYMPTOMS / COMMON SYMPTOMS ────────────────────────────────────────
    "symptoms": {
        "keywords": ["symptom", "symptoms", "feeling sick", "not feeling well", "fever", "headache", "cough", "fatigue", "tired", "pain"],
        "response": """
## 🩺 Understanding Common Health Symptoms

Symptoms are your body's way of signaling that something needs attention. Recognizing what's normal vs. concerning is an important part of healthcare awareness.

### 🌡️ Common Symptoms & What They May Indicate

**Fever (Temperature ≥ 100.4°F / 38°C)**
- Usually caused by infection (bacterial or viral)
- Self-care: Rest, fluids, OTC fever reducers if comfortable
- See a doctor if: Fever > 103°F (39.4°C), lasts > 3 days, or is accompanied by stiff neck, severe headache, or difficulty breathing

**Persistent Fatigue**
- Possible causes: Anemia, thyroid disorders, diabetes, depression, sleep apnea, vitamin deficiencies
- Track: Duration, severity, whether rest helps
- See a doctor if: Lasting > 2 weeks without clear cause

**Cough**
- Acute (< 3 weeks): Usually viral — cold, flu, COVID
- Chronic (> 8 weeks): May indicate asthma, GERD, COPD, or rarely lung conditions
- See a doctor if: Coughing blood, chest pain with cough, shortness of breath

**Headache**
- Tension-type: Pressure around forehead — stress, dehydration
- Migraine: Throbbing, often one-sided, with nausea/light sensitivity
- See a doctor urgently if: Sudden severe "thunderclap" headache, headache with fever and stiff neck, or after head injury

### 🚨 Red-Flag Symptoms (Seek Emergency Care Immediately)
- Sudden severe chest pain or pressure
- Difficulty breathing at rest
- Sudden weakness on one side of body (possible stroke)
- Confusion or loss of consciousness
- Coughing or vomiting blood
- Severe abdominal pain

### 📋 Tracking Your Symptoms
When seeing a doctor, note:
1. **When** did it start?
2. **How severe** on a 1-10 scale?
3. **What makes it better or worse?**
4. **Any associated symptoms?**
5. **Recent exposures** (sick contacts, travel, new medications)?

> **⚕️ Educational Notice:** This overview is for general awareness. Symptoms alone cannot confirm a diagnosis — only a licensed physician with proper examination and tests can do that.
""",
    },

    # ── MENTAL HEALTH ─────────────────────────────────────────────────────
    "mental_health": {
        "keywords": ["mental health", "anxiety", "depression", "stress", "panic attack", "mood", "mental wellness", "psychology", "bipolar", "ptsd", "ocd", "schizophrenia", "suicid"],
        "response": """
## 🧠 Mental Health Awareness

Mental health is just as vital as physical health. Approximately **1 in 4 people** worldwide experience a mental health condition at some point in their lives. Awareness, early support, and compassionate care make a significant difference.

### 💙 Common Mental Health Conditions

**Anxiety Disorders**
- Characterized by persistent, excessive worry or fear
- Types: Generalized Anxiety Disorder (GAD), Panic Disorder, Social Anxiety, Phobias
- Symptoms: Rapid heartbeat, sweating, restlessness, difficulty concentrating, sleep problems

**Depression (Major Depressive Disorder)**
- More than "feeling sad" — a persistent low mood affecting daily functioning
- Symptoms: Loss of interest in activities, fatigue, changes in appetite/sleep, feelings of worthlessness, difficulty concentrating
- Important: Depression is a medical condition, NOT a personal weakness

**Stress**
- Acute stress: Short-term response to specific triggers — normal and manageable
- Chronic stress: Prolonged stress that raises cortisol, affecting heart, immunity, and mental clarity

### 🌿 Evidence-Based Coping Strategies
1. **Physical Activity** — 30 min of exercise releases endorphins, reducing anxiety and depression symptoms
2. **Sleep Hygiene** — Consistent 7–9 hours; sleep deprivation worsens mood disorders
3. **Mindfulness & Breathing** — Deep breathing (4-7-8 technique), meditation apps, body scans
4. **Social Connection** — Talk to trusted friends, family, or support groups
5. **Professional Support** — Therapy (CBT is highly evidence-based), counseling, or psychiatry
6. **Limit Alcohol & Caffeine** — Both can worsen anxiety and disrupt sleep
7. **Journaling** — Writing thoughts helps process emotions and identify patterns

### 📞 24/7 Crisis Helplines (India)
| Service | Contact |
|---------|---------|
| **iCall (TISS)** | 9152987821 |
| **Vandrevala Foundation** | 1860-2662-345 |
| **NIMHANS** | 080-46110007 |
| **Snehi** | 044-24640050 |

> **💙 You are not alone.** Seeking help is a sign of strength, not weakness. If you are having thoughts of self-harm, please reach out to a crisis helpline or emergency services immediately.
""",
    },

    # ── NUTRITION / DIET ──────────────────────────────────────────────────
    "nutrition": {
        "keywords": ["nutrition", "diet", "eating", "food", "weight", "obesity", "bmi", "calorie", "protein", "carbohydrate", "vitamin", "mineral", "healthy eating", "nutrient"],
        "response": """
## 🥗 Nutrition & Healthy Eating Awareness

Good nutrition is the foundation of long-term health. What you eat affects your energy, immunity, mental health, and risk of chronic disease.

### 🌈 Principles of a Balanced Diet (WHO & ICMR Guidelines)

**Key Food Groups to Include Daily:**
- 🌾 **Whole Grains** — Brown rice, oats, whole wheat bread, millets (complex carbs + fiber)
- 🥦 **Vegetables** — Aim for 5+ servings; variety of colors for different micronutrients
- 🍎 **Fruits** — 2–3 servings/day; choose whole fruit over juice
- 🥩 **Lean Proteins** — Dal, legumes, eggs, fish, chicken, paneer, tofu
- 🥛 **Dairy/Alternatives** — Low-fat milk, curd, fortified plant-based options
- 🥑 **Healthy Fats** — Olive oil, nuts, seeds, avocado; limit saturated & trans fats

**What to Limit:**
- 🧂 **Salt** — < 5g/day (WHO) — reduces hypertension risk
- 🍬 **Free sugars** — < 10% of total energy intake
- 🍟 **Processed/ultra-processed foods** — High in sodium, unhealthy fats, additives
- 🥤 **Sugary beverages** — Replace with water, buttermilk, or herbal teas

### 💧 Hydration
- **Adults**: 2–3 litres of water per day
- More needed during exercise, hot weather, or illness
- Urine color guide: Pale yellow = well hydrated; dark yellow = drink more

### 📊 Understanding BMI (Body Mass Index)
| BMI Range | Category |
|-----------|---------|
| < 18.5 | Underweight |
| 18.5–24.9 | Normal weight |
| 25.0–29.9 | Overweight |
| ≥ 30.0 | Obese |

### 🍽️ Practical Healthy Eating Tips
1. **Eat mindfully** — Slow down, chew well, avoid screens while eating
2. **Portion control** — Use smaller plates; fill half the plate with vegetables
3. **Don't skip breakfast** — Kick-starts metabolism; choose protein-rich options
4. **Plan meals** — Reduces impulsive unhealthy choices
5. **Healthy snacks** — Nuts, fruit, hummus with vegetables instead of chips/cookies

> **⚕️ Educational Notice:** For personalized dietary advice, especially if you have diabetes, kidney disease, or other medical conditions, consult a registered dietitian or your physician.
""",
    },

    # ── VACCINATION / IMMUNIZATION ────────────────────────────────────────
    "vaccination": {
        "keywords": ["vaccine", "vaccination", "immunization", "flu shot", "booster", "mmr", "hepatitis", "covid vaccine", "tetanus", "immunize"],
        "response": """
## 💉 Vaccines & Immunization Awareness

Vaccines are one of the most powerful tools in preventive medicine, having eradicated or drastically reduced diseases like smallpox, polio, measles, and more.

### 🛡️ How Vaccines Work
Vaccines train your immune system to recognize and fight specific pathogens (bacteria/viruses) without causing the disease itself. When vaccinated, your body creates **memory cells** so that if exposed to the real pathogen, it can mount a rapid, effective defense.

### 📅 Recommended Adult Vaccines (India — General Guidance)
| Vaccine | Protection | Schedule |
|---------|-----------|---------|
| **Influenza (Flu)** | Seasonal influenza | Annually (especially for elderly, immunocompromised) |
| **COVID-19** | SARS-CoV-2 | Primary series + boosters as recommended |
| **Tetanus-Diphtheria (Td)** | Tetanus, diphtheria | Every 10 years |
| **Hepatitis B** | Hepatitis B virus | 3-dose series (if not vaccinated as child) |
| **Pneumococcal** | Pneumonia | Recommended for 65+, high-risk adults |
| **Typhoid** | Typhoid fever | Every 3 years (in endemic areas) |
| **MMR** | Measles, mumps, rubella | If not immune |

### ✅ Vaccine Safety — Key Facts
- All approved vaccines undergo rigorous multi-phase clinical trials
- Serious adverse reactions are extremely rare; benefits vastly outweigh risks
- "Herd immunity" protects vulnerable people who cannot be vaccinated
- Natural infection is NOT safer than vaccination — it carries far higher complication risks

### ⚠️ Common Side Effects (Normal Immune Response)
- Arm soreness at injection site
- Low-grade fever for 1–2 days
- Mild fatigue or headache
These side effects indicate your immune system is building protection.

### 👶 Childhood Immunization Schedule (India — Universal Immunization Programme)
- BCG (at birth), OPV, DPT, Hepatitis B, Hib, Rotavirus, PCV, Measles/MR, JE, HPV (girls)
- Follow the National Immunization Schedule; consult your paediatrician

> **⚕️ Educational Notice:** Consult your doctor before vaccination if you have severe allergies, are immunocompromised, or are pregnant. Your physician will advise on appropriate timing and any contraindications.
""",
    },

    # ── CHOLESTEROL ───────────────────────────────────────────────────────
    "cholesterol": {
        "keywords": ["cholesterol", "ldl", "hdl", "triglyceride", "lipid", "dyslipidemia", "statin", "cholesterol level", "good cholesterol", "bad cholesterol", "healthy cholesterol", "cholesterol reading", "lipid panel", "lipid profile"],
        "response": """
## 🧬 Cholesterol — Understanding Your Lipid Profile

Cholesterol is a waxy, fat-like substance found in every cell of your body. While your body *needs* cholesterol to build cells and make hormones, too much of the wrong type raises heart disease risk.

### 📊 Cholesterol Values Guide
| Measurement | Optimal | Borderline | High Risk |
|-------------|---------|------------|-----------|
| **Total Cholesterol** | < 200 mg/dL | 200–239 mg/dL | ≥ 240 mg/dL |
| **LDL ("Bad")** | < 100 mg/dL | 100–159 mg/dL | ≥ 160 mg/dL |
| **HDL ("Good")** | ≥ 60 mg/dL (protective) | 40–59 mg/dL | < 40 mg/dL |
| **Triglycerides** | < 150 mg/dL | 150–199 mg/dL | ≥ 200 mg/dL |

### 🥗 Diet Strategies to Improve Cholesterol
- **Increase soluble fiber** — Oats, barley, beans, lentils, apples, citrus fruits
- **Eat healthy fats** — Olive oil, avocado, nuts, fatty fish (omega-3: salmon, mackerel, sardines)
- **Reduce saturated fat** — Limit red meat, full-fat dairy, coconut oil, ghee
- **Eliminate trans fats** — Avoid partially hydrogenated oils in packaged foods
- **Plant sterols/stanols** — Found in fortified foods; block cholesterol absorption

### 💪 Lifestyle Changes
- 30+ minutes of aerobic exercise daily raises HDL
- Quit smoking — raises HDL and reduces LDL oxidation
- Maintain healthy weight — 10% weight reduction can lower LDL by 10–20%
- Limit alcohol — excessive drinking raises triglycerides

### 💊 When Medication is Needed
Statins (e.g., atorvastatin, rosuvastatin) are highly effective and widely prescribed when lifestyle changes alone are insufficient or when cardiovascular risk is high. Always take as prescribed and do not stop without consulting your doctor.

> **⚕️ Educational Notice:** A fasting lipid panel test is needed for accurate cholesterol measurement. Testing is recommended every 5 years from age 20, more often if you have risk factors.
""",
    },

    # ── FLU / COLD ────────────────────────────────────────────────────────
    "flu": {
        "keywords": ["flu", "influenza", "cold", "common cold", "cough", "runny nose", "sore throat", "fever flu", "flu vs cold", "virus"],
        "response": """
## 🤧 Flu vs. Common Cold — What's the Difference?

Both are respiratory illnesses caused by viruses, but they differ significantly in severity, onset, and complications.

### ⚖️ Comparison Table
| Feature | Common Cold | Influenza (Flu) |
|---------|------------|-----------------|
| **Onset** | Gradual (1–2 days) | Sudden (hours) |
| **Fever** | Rare, mild if present | Common, often 100–104°F (38–40°C) |
| **Headache** | Uncommon | Very common |
| **Body aches** | Mild | Severe, often described as "hit by a truck" |
| **Fatigue** | Mild | Intense, can last weeks |
| **Runny nose** | Very common | Sometimes |
| **Sore throat** | Very common | Sometimes |
| **Chest discomfort** | Mild | Common; can be severe |
| **Complications** | Rare | Pneumonia, hospitalization possible |
| **Duration** | 7–10 days | 1–2 weeks; fatigue longer |

### 💊 Treatment
**Common Cold:**
- No cure — supportive care only
- Rest, fluids, saline nasal rinse, OTC decongestants/antihistamines for symptoms
- Antibiotics are NOT effective (colds are viral)

**Influenza:**
- Antiviral medications (Oseltamivir/Tamiflu) can reduce duration if taken within 48 hours of onset
- Most people recover with rest and fluids
- High-risk groups (elderly, pregnant, immunocompromised) should see a doctor promptly

### 🛡️ Prevention
- **Annual flu vaccine** — Most effective prevention; reformulated each year for circulating strains
- **Hand hygiene** — Wash hands frequently for ≥ 20 seconds
- **Avoid close contact** with sick individuals
- **Don't touch your face** — Viruses enter through eyes, nose, and mouth
- **Stay home when sick** — Prevents spreading to others

### 🚨 When to Seek Medical Attention
- Difficulty breathing or shortness of breath
- Persistent chest pain or pressure
- Confusion or altered consciousness
- Severe or worsening symptoms after initial improvement

> **⚕️ Educational Notice:** Antibiotics do not treat colds or flu. Misuse leads to antibiotic resistance. Only use antibiotics when prescribed by a physician for bacterial infections.
""",
    },

    # ── SLEEP ─────────────────────────────────────────────────────────────
    "sleep": {
        "keywords": ["sleep", "insomnia", "sleep disorder", "sleep apnea", "tired", "fatigue", "rest", "sleep quality", "sleep hygiene"],
        "response": """
## 😴 Sleep Health & Sleep Hygiene

Quality sleep is essential for physical health, mental clarity, immunity, metabolism, and emotional regulation. Chronic sleep deprivation is linked to diabetes, heart disease, obesity, and depression.

### ⏰ How Much Sleep Do You Need?
| Age Group | Recommended Sleep |
|-----------|------------------|
| **Infants (4–12 months)** | 12–16 hours |
| **Toddlers (1–2 years)** | 11–14 hours |
| **School-age (6–12 years)** | 9–12 hours |
| **Teenagers (13–18 years)** | 8–10 hours |
| **Adults (18–64 years)** | **7–9 hours** |
| **Older Adults (65+)** | 7–8 hours |

### ⚠️ Signs of Poor Sleep / Sleep Deprivation
- Difficulty concentrating or making decisions
- Irritability, mood swings
- Frequent yawning, heavy eyelids during the day
- Dependence on caffeine to function
- Microsleeps (brief unintended sleep episodes)
- Weakened immune system (getting sick often)

### 🌙 Sleep Hygiene — Evidence-Based Tips
1. **Consistent schedule** — Same sleep/wake time every day (including weekends)
2. **Cool, dark, quiet room** — 65–68°F (18–20°C) is optimal sleep temperature
3. **Blue light restriction** — No screens (phone, TV) for 60–90 minutes before bed
4. **No caffeine after 2 PM** — Caffeine has a 5–6 hour half-life
5. **Wind-down routine** — Reading, light stretching, meditation, warm shower/bath
6. **Reserve bed for sleep** — Avoid working or watching TV in bed
7. **No large meals close to bedtime** — Aim to finish eating 2–3 hours before sleep
8. **Exercise regularly** — But not within 3 hours of bedtime

### 🏥 Common Sleep Disorders
- **Insomnia** — Difficulty falling or staying asleep
- **Sleep Apnea** — Repeated breathing interruptions; snoring, gasping; linked to hypertension and heart disease
- **Restless Leg Syndrome** — Uncomfortable urge to move legs, worse at night
- **Narcolepsy** — Excessive daytime sleepiness with sudden sleep attacks

> **⚕️ Educational Notice:** If you consistently struggle with sleep despite good sleep hygiene, consult a sleep specialist. Sleep disorders are highly treatable conditions.
""",
    },

    # ── EXERCISE / PHYSICAL ACTIVITY ──────────────────────────────────────
    "exercise": {
        "keywords": ["exercise", "workout", "physical activity", "fitness", "gym", "running", "yoga", "sedentary", "cardio", "strength training"],
        "response": """
## 🏃 Physical Activity & Exercise for Health

Regular physical activity is one of the most powerful preventive health tools available — reducing risk of heart disease, diabetes, certain cancers, depression, and premature death.

### 🎯 WHO Physical Activity Recommendations (Adults 18–64)
| Activity Type | Recommendation |
|--------------|----------------|
| **Moderate aerobic** | ≥ 150–300 min/week (brisk walk, cycling, swimming) |
| **Vigorous aerobic** | ≥ 75–150 min/week (running, HIIT, fast cycling) |
| **Muscle strengthening** | ≥ 2 days/week (all major muscle groups) |
| **Sedentary behavior** | Limit prolonged sitting — break it up frequently |

### 💪 Benefits of Regular Exercise
- ❤️ **Heart health** — Lowers blood pressure, LDL; raises HDL
- 🩸 **Blood sugar control** — Muscles use glucose without insulin during exercise
- 🧠 **Mental health** — Releases endorphins, serotonin; reduces anxiety and depression
- ⚖️ **Weight management** — Burns calories; maintains lean muscle mass
- 🦴 **Bone & joint health** — Weight-bearing exercise prevents osteoporosis
- 🛡️ **Immune support** — Moderate exercise enhances immune surveillance
- 😴 **Sleep quality** — Regular exercisers fall asleep faster and sleep more deeply
- ⏳ **Longevity** — Even 11 min/day of moderate activity reduces mortality risk by 23%

### 🚶 Starting an Exercise Routine (Beginner-Friendly)
1. **Start small** — Even 10-minute walks count and can be built upon
2. **Find activities you enjoy** — Dance, cycling, swimming, cricket — consistency matters most
3. **Progress gradually** — Increase duration and intensity by 10% per week max
4. **Warm-up & cool-down** — 5 minutes each prevents injury
5. **Listen to your body** — Pain (not muscle soreness) means stop and rest

### ⚠️ When to Consult Before Exercising
- If you have uncontrolled heart disease, severe joint problems, or are newly pregnant
- If you've been sedentary for years and are over 45 — get a medical clearance first

> **⚕️ Educational Notice:** Exercise recommendations are general guidelines. People with chronic conditions should work with their healthcare team to develop a personalized and safe fitness plan.
""",
    },

    # ── GENERAL / DEFAULT ─────────────────────────────────────────────────
    "general": {
        "keywords": [],
        "response": None,  # generated dynamically
    },
}


def _match_topic(query: str) -> str:
    """Match user query to best knowledge base topic using keyword scoring."""
    query_lower = query.lower()
    best_topic = "general"
    best_score = 0

    for topic, data in HEALTH_KNOWLEDGE.items():
        if topic == "general":
            continue
        # Count keyword hits — longer/more specific keywords get higher weight
        score = 0
        for kw in data["keywords"]:
            if kw in query_lower:
                # Longer keywords are more specific — give bonus weight
                score += 1 + len(kw.split()) * 0.5
        if score > best_score:
            best_score = score
            best_topic = topic

    # Require a minimum score to avoid false positives
    return best_topic if best_score >= 1 else "general"


def _clean_context_text(text: str) -> str:
    """Strip out raw markdown headers, source tags, and noise from RAG chunks."""
    # Remove [Source N: ...] tags
    text = re.sub(r"\[Source \d+:[^\]]*\]", "", text)
    # Remove leading markdown headers (##, #)
    text = re.sub(r"^#{1,4}\s+.*$", "", text, flags=re.MULTILINE)
    # Remove bold markdown that wraps full lines
    text = re.sub(r"\*\*([^*]{80,})\*\*", r"\1", text)
    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _extract_key_facts(context_text: str, max_facts: int = 5) -> list:
    """Extract clean, complete sentences from RAG context as educational facts."""
    # Clean the context first
    clean = _clean_context_text(context_text)

    # Split into sentences
    sentences = re.split(r"(?<=[.!?])\s+", clean)

    facts = []
    seen = set()
    for s in sentences:
        s = s.strip()
        # Only keep informative sentences (not too short, not duplicates, not headers)
        if (len(s) > 40 and not s.startswith("#") and
                s.lower() not in seen and
                not re.match(r"^\[.*\]$", s)):
            seen.add(s.lower())
            facts.append(s)
        if len(facts) >= max_facts:
            break

    return facts


def _build_dynamic_response(query: str, context_facts: list) -> str:
    """Build a well-structured, topic-aware healthcare response with context facts."""
    topic = _match_topic(query)
    query_title = query.strip().rstrip("?").title()

    # Use pre-built topic knowledge if available
    if topic != "general" and HEALTH_KNOWLEDGE[topic]["response"]:
        return HEALTH_KNOWLEDGE[topic]["response"].strip()

    # Build a dynamic structured response from context facts
    facts_section = ""
    if context_facts:
        facts_section = (
            "### 📋 Key Educational Points\n"
            + "\n".join(f"- {fact}" for fact in context_facts[:5])
            + "\n\n"
        )
    else:
        facts_section = (
            "### 📋 General Health Guidance\n"
            "- Prevention is always better than cure — address risk factors early\n"
            "- Maintain a balanced diet rich in vegetables, whole grains, and lean proteins\n"
            "- Aim for at least 150 minutes of moderate aerobic activity per week\n"
            "- Get regular health screenings based on your age and risk profile\n"
            "- Adequate sleep (7–9 hours) is essential for physical and mental recovery\n\n"
        )

    response = f"""## 🩺 Health Awareness: {query_title}

Thank you for your question. Here is evidence-based educational guidance on this health topic.

{facts_section}
### 💡 General Preventive Health Principles
- **Stay informed** — Understanding your health conditions and risk factors empowers better decisions
- **Routine check-ups** — Regular medical screenings catch conditions early when they're most treatable
- **Healthy lifestyle** — A balanced diet, regular physical activity, adequate sleep, and stress management form the foundation of long-term wellness
- **Medication adherence** — If prescribed medications, take them consistently as directed by your physician
- **Avoid self-diagnosis** — Use educational resources like this to become informed, but always confirm concerns with a licensed medical professional

### 🏥 When to Consult a Doctor
Schedule an appointment if:
- Your symptoms persist, worsen, or significantly affect daily functioning
- You are managing a chronic condition and notice changes
- You have questions about medications, test results, or diagnostic reports
- You want personalized preventive health screening based on your age and family history

> **⚕️ Educational Disclaimer:** HealthAware AI provides health awareness and educational information only. It does not diagnose medical conditions, prescribe treatments, or replace consultation with a licensed healthcare professional. For medical emergencies, call 112 (India) or your local emergency number.
"""
    return response.strip()


class OfflineKnowledgeLLMProvider(LLMProvider):
    """
    Built-in intelligent healthcare knowledge engine.
    Delivers topic-aware, structured, patient-friendly educational responses
    using a rich knowledge library and RAG context synthesis.
    Works 100% offline — no internet or API keys required.
    """

    def generate_response(
        self,
        prompt: str,
        system_prompt: str = HEALTH_SYSTEM_PROMPT,
        temperature: float = 0.3,
        max_tokens: int = 900
    ) -> str:

        # Extract user query
        user_query_match = re.search(r"User Question:\s*(.*?)(?:\n|$)", prompt)
        user_query = user_query_match.group(1).strip() if user_query_match else ""

        # Try to detect topic from query directly
        topic = _match_topic(user_query) if user_query else "general"

        # If a clear topic match found — use structured knowledge response
        if topic != "general" and HEALTH_KNOWLEDGE[topic]["response"]:
            base_response = HEALTH_KNOWLEDGE[topic]["response"].strip()
            return base_response

        # Otherwise extract context facts and build dynamic response
        context_match = re.search(
            r"--- VERIFIED HEALTHCARE KNOWLEDGE CONTEXT ---\s*(.*?)\s*--- END CONTEXT ---",
            prompt, re.DOTALL
        )
        context_facts = []
        if context_match:
            raw_context = context_match.group(1)
            context_facts = _extract_key_facts(raw_context, max_facts=5)

        return _build_dynamic_response(user_query or "your health question", context_facts)


class OpenAILLMProvider(LLMProvider):
    """OpenAI API Provider (GPT-4o-mini, GPT-4, etc.)."""

    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.api_key = api_key
        self.model = model
        self.endpoint = "https://api.openai.com/v1/chat/completions"

    def generate_response(
        self,
        prompt: str,
        system_prompt: str = HEALTH_SYSTEM_PROMPT,
        temperature: float = 0.3,
        max_tokens: int = 900
    ) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        resp = requests.post(self.endpoint, headers=headers, json=payload, timeout=25)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


class OllamaLLMProvider(LLMProvider):
    """Local Ollama LLM Provider (llama3, mistral, gemma, etc.)."""

    def __init__(self, host: str = "http://localhost:11434", model: str = "llama3"):
        self.host = host.rstrip("/")
        self.model = model

    def generate_response(
        self,
        prompt: str,
        system_prompt: str = HEALTH_SYSTEM_PROMPT,
        temperature: float = 0.3,
        max_tokens: int = 900
    ) -> str:
        endpoint = f"{self.host}/api/generate"
        payload = {
            "model": self.model,
            "system": system_prompt,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature, "num_predict": max_tokens}
        }
        resp = requests.post(endpoint, json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json().get("response", "")


def get_llm_provider() -> LLMProvider:
    """
    Factory: reads LLM provider from environment variables.
    Falls back gracefully to the built-in OfflineKnowledgeLLMProvider.
    """
    provider_type = os.getenv("LLM_PROVIDER", "offline").lower().strip()
    api_key = os.getenv("LLM_API_KEY", "").strip()
    model = os.getenv("LLM_MODEL", "gpt-4o-mini").strip()

    if provider_type == "openai" and api_key:
        return OpenAILLMProvider(api_key=api_key, model=model)
    elif provider_type == "ollama":
        host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        return OllamaLLMProvider(host=host, model=model or "llama3")

    # Default: intelligent offline engine
    return OfflineKnowledgeLLMProvider()
