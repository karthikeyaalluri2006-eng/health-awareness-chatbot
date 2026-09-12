"""
HealthAware AI - Symptom Awareness Checker
Guided clinical triage workflow evaluating symptom urgency and next steps.
Strictly educational - never provides definitive diagnosis.
Strictly Python + Streamlit. NO JAVASCRIPT.
"""

import streamlit as st
from services.symptom_service import evaluate_symptoms
from components.common import render_header, render_disclaimer, apply_theme
from components.sidebar import render_sidebar

st.set_page_config(page_title="Symptom Checker - HealthAware AI", page_icon="🩺", layout="wide")
apply_theme()
render_sidebar()

render_header(
    title="Symptom Awareness & Urgency Checker",
    subtitle="Evaluate symptom duration, severity, and associated red-flags to understand appropriate care urgency.",
    icon="🩺"
)

render_disclaimer()

with st.form("symptom_form"):
    st.subheader("1. General Information")
    c1, c2 = st.columns(2)
    with c1:
        age_group = st.selectbox(
            "Age Bracket",
            ["Adult (18 - 64 years)", "Older Adult (65+ years)", "Adolescent (12 - 17 years)", "Child (under 12)"]
        )
        primary_sym = st.text_input("What is your primary symptom?", placeholder="e.g., Persistent cough, mild fever, throbbing headache")

    with c2:
        duration = st.slider("How many days have you had this symptom?", 1, 30, 2)
        severity = st.slider("Rate current discomfort / severity (1 = Mild, 10 = Severe & Debilitating)", 1, 10, 3)

    st.subheader("2. Associated Symptoms & Red Flags")
    assoc_options = [
        "High fever (> 102°F / 39°C)",
        "Shortness of breath / Difficulty breathing",
        "Chest pain or pressure",
        "Dizziness or lightheadedness",
        "Nausea or vomiting",
        "Stiff neck with headache",
        "Unexplained rash",
        "Extreme fatigue"
    ]
    selected_assoc = st.multiselect("Select any accompanying symptoms:", options=assoc_options)

    st.subheader("3. Underlying Health History")
    chronic_options = [
        "High Blood Pressure (Hypertension)",
        "Diabetes (Type 1 or Type 2)",
        "Heart Disease",
        "Asthma / COPD",
        "Immunocompromised State",
        "None of the above"
    ]
    selected_chronic = st.multiselect("Select any diagnosed chronic conditions:", options=chronic_options)

    submit_check = st.form_submit_button("Evaluate Symptoms", type="primary", use_container_width=True)

if submit_check:
    if not primary_sym.strip():
        st.error("Please describe your primary symptom.")
    else:
        results = evaluate_symptoms(
            age_group=age_group,
            primary_symptom=primary_sym,
            duration_days=duration,
            severity=severity,
            associated_symptoms=selected_assoc,
            chronic_conditions=selected_chronic
        )

        st.markdown(
            f"""
            <div class="health-card" style="border-top: 4px solid {results['color']};">
                <h3 style="color: {results['color']}; margin-top: 0;">{results['urgency_level']}</h3>
                <p style="font-size: 1rem; font-weight: 500; color: #cbd5e1; line-height: 1.6;">
                    {results['guidance']}
                </p>
                <div style="margin-top: 12px; padding: 12px; background: rgba(255,255,255,0.04);
                            border: 1px solid rgba(255,255,255,0.07); border-radius: 8px;
                            color: #94a3b8; font-size: 0.9rem;">
                    <strong style="color: #f1f5f9;">Recommended Action:</strong> {results['recommended_action']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.expander("🔍 Symptom Summary Review", expanded=True):
            for k, v in results["summary"].items():
                st.markdown(f"• **{k}:** {v}")

        st.warning(f"⚕️ {results['disclaimer']}")
