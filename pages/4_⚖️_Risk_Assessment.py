"""
HealthAware AI - Educational Health Risk Assessment
Calculates non-diagnostic educational lifestyle risk indicators for Type 2 Diabetes and Hypertension.
Strictly educational - uses wording 'Lower / Moderate / Higher Educational Risk'.
Strictly Python + Streamlit. NO JAVASCRIPT.
"""

import streamlit as st
from database.connection import get_db_session
from database.repositories import RiskAssessmentRepository
from auth.authentication import get_current_user
from components.common import render_header, render_disclaimer, apply_theme
from components.sidebar import render_sidebar
from components.risk_ui import render_risk_result_card

st.set_page_config(page_title="Risk Assessment - HealthAware AI", page_icon="⚖️", layout="wide")
apply_theme()
render_sidebar()

render_header(
    title="Educational Health Risk Assessments",
    subtitle="Evaluate lifestyle and demographic risk indicators for preventable chronic conditions.",
    icon="⚖️"
)

render_disclaimer()

user = get_current_user()
user_id = user["id"] if user else 1

tab_diabetes, tab_htn, tab_history = st.tabs([
    "🩸 Type 2 Diabetes Risk",
    "❤️ Hypertension & Heart Lifestyle Risk",
    "📜 Assessment History"
])

# ==============================================================================
# 1. TYPE 2 DIABETES EDUCATIONAL RISK ASSESSMENT (ADA MODEL INSPIRATION)
# ==============================================================================
with tab_diabetes:
    st.markdown("### Type 2 Diabetes Educational Screening")
    st.caption("Based on standard public health risk indicators from the American Diabetes Association (ADA).")

    with st.form("diabetes_risk_form"):
        col1, col2 = st.columns(2)
        with col1:
            age_cat = st.selectbox(
                "Age Group",
                ["Under 40 years (0 pts)", "40 - 49 years (1 pt)", "50 - 59 years (2 pts)", "60 years or older (3 pts)"]
            )
            gender = st.selectbox("Biological Sex", ["Female", "Male", "Other / Prefer not to say"])
            active = st.radio("Are you physically active regularly (at least 150 mins/week)?", ["Yes (0 pts)", "No (1 pt)"])
            family = st.radio("Do you have a parent, brother, or sister with diabetes?", ["No (0 pts)", "Yes (1 pt)"])

        with col2:
            bp_status = st.radio("Have you ever been told by a doctor that you have high blood pressure?", ["No (0 pts)", "Yes (1 pt)"])
            bmi_cat = st.selectbox(
                "Body Mass Category (Relative to height & weight)",
                ["Normal weight range (0 pts)", "Overweight range (1 pt)", "Obese range (2 pts)", "Severely obese range (3 pts)"]
            )
            gestational = st.radio("If female, have you ever been diagnosed with gestational diabetes?", ["No / Not Applicable (0 pts)", "Yes (1 pt)"])

        calc_diabetes = st.form_submit_button("Calculate Educational Risk", type="primary", use_container_width=True)

    if calc_diabetes:
        score = 0
        factors = []
        recommendations = []

        # Age score
        if "40 - 49" in age_cat: score += 1
        elif "50 - 59" in age_cat: score += 2
        elif "60 years" in age_cat: score += 3

        # Inactivity
        if "No (1 pt)" in active:
            score += 1
            factors.append("Low regular physical activity level.")
            recommendations.append("Work toward 150 minutes of moderate aerobic activity (e.g. brisk walking) weekly.")

        # Family history
        if "Yes (1 pt)" in family:
            score += 1
            factors.append("First-degree family member diagnosed with diabetes.")
            recommendations.append("Inform your primary care doctor of your family medical history.")

        # Hypertension
        if "Yes (1 pt)" in bp_status:
            score += 1
            factors.append("History of elevated blood pressure.")
            recommendations.append("Maintain routine blood pressure and glucose monitoring.")

        # Weight category
        if "Overweight" in bmi_cat:
            score += 1
            factors.append("Elevated body mass category.")
            recommendations.append("Modest 5-7% weight reduction significantly improves insulin sensitivity.")
        elif "Obese" in bmi_cat:
            score += 2
            factors.append("Significantly elevated body mass category.")
            recommendations.append("Discuss structured medical nutrition therapy with a registered dietitian.")
        elif "Severely obese" in bmi_cat:
            score += 3
            factors.append("Substantially elevated body mass index.")
            recommendations.append("Consult with your physician regarding comprehensive metabolic health management.")

        # Gestational
        if "Yes (1 pt)" in gestational:
            score += 1
            factors.append("Personal history of gestational diabetes during pregnancy.")
            recommendations.append("Undergo annual or biennial fasting glucose / HbA1c testing.")

        # Risk Tier
        if score >= 5:
            risk_tier = "Higher Educational Risk"
        elif score >= 3:
            risk_tier = "Moderate Educational Risk"
        else:
            risk_tier = "Lower Educational Risk"

        recommendations.append("Review these educational results with your doctor during your next wellness visit.")

        render_risk_result_card(
            assessment_name="Type 2 Diabetes Risk Indicator",
            risk_level=risk_tier,
            score=score,
            factors=factors,
            recommendations=recommendations
        )

        with get_db_session() as db:
            RiskAssessmentRepository.save_assessment(
                db=db,
                user_id=user_id,
                assessment_type="Type 2 Diabetes",
                inputs={"age": age_cat, "active": active, "family": family, "bp": bp_status, "bmi": bmi_cat},
                risk_level=risk_tier,
                score=float(score),
                factors=factors,
                recommendations=recommendations
            )

# ==============================================================================
# 2. HYPERTENSION & HEART LIFESTYLE RISK ASSESSMENT
# ==============================================================================
with tab_htn:
    st.markdown("### Hypertension & Cardiovascular Lifestyle Risk")
    st.caption("Evaluates key lifestyle factors influencing vascular tone and cardiovascular health.")

    with st.form("htn_risk_form"):
        h_col1, h_col2 = st.columns(2)
        with h_col1:
            h_salt = st.selectbox("Daily Sodium Intake", ["Moderate to Low (Cook at home)", "High (Frequent processed food/takeout)"])
            h_exercise = st.selectbox("Cardiovascular Aerobic Exercise", ["Regular (3+ times per week)", "Rare or Sedentary"])
            h_smoking = st.selectbox("Tobacco / Smoking Habits", ["Non-smoker", "Former smoker", "Active smoker"])

        with h_col2:
            h_sleep = st.selectbox("Nightly Sleep Duration", ["7 - 9 hours (Restorative)", "Less than 6 hours regularly"])
            h_stress = st.slider("Typical Daily Stress Level (1 = Low, 10 = Severe)", 1, 10, 4)
            h_family_c = st.radio("Family History of Premature Heart Disease or Stroke?", ["No", "Yes"])

        calc_htn = st.form_submit_button("Calculate Heart Lifestyle Risk", type="primary", use_container_width=True)

    if calc_htn:
        h_score = 0
        h_factors = []
        h_recs = []

        if "High" in h_salt:
            h_score += 2
            h_factors.append("High intake of dietary sodium from processed foods.")
            h_recs.append("Incorporate the DASH diet pattern: restrict sodium to under 2,300 mg/day.")

        if "Rare" in h_exercise:
            h_score += 2
            h_factors.append("Sedentary lifestyle with minimal aerobic movement.")
            h_recs.append("Engage in brisk walking, swimming, or cycling for 30 minutes, 5 days a week.")

        if "Active smoker" in h_smoking:
            h_score += 3
            h_factors.append("Active tobacco use causing endothelial vasoconstriction.")
            h_recs.append("Ask your doctor about smoking cessation support, nicotine replacement, or behavioral counseling.")

        if "Less than 6 hours" in h_sleep:
            h_score += 1
            h_factors.append("Sub-optimal sleep duration.")
            h_recs.append("Prioritize consistent sleep hygiene aiming for 7-8 hours per night.")

        if h_stress >= 7:
            h_score += 1
            h_factors.append("Elevated daily perceived stress levels.")
            h_recs.append("Explore box breathing, progressive relaxation, and stress management practices.")

        if "Yes" in h_family_c:
            h_score += 2
            h_factors.append("Family history of cardiovascular illness.")
            h_recs.append("Schedule an annual fasting lipid profile and resting blood pressure measurement.")

        if h_score >= 5:
            h_tier = "Higher Educational Risk"
        elif h_score >= 3:
            h_tier = "Moderate Educational Risk"
        else:
            h_tier = "Lower Educational Risk"

        render_risk_result_card(
            assessment_name="Cardiovascular Lifestyle Risk Indicator",
            risk_level=h_tier,
            score=h_score,
            factors=h_factors,
            recommendations=h_recs
        )

        with get_db_session() as db:
            RiskAssessmentRepository.save_assessment(
                db=db,
                user_id=user_id,
                assessment_type="Hypertension & Heart",
                inputs={"salt": h_salt, "exercise": h_exercise, "smoking": h_smoking, "stress": h_stress},
                risk_level=h_tier,
                score=float(h_score),
                factors=h_factors,
                recommendations=h_recs
            )

# ==============================================================================
# 3. PAST ASSESSMENTS HISTORY
# ==============================================================================
with tab_history:
    st.subheader("📜 Your Past Risk Assessments")
    with get_db_session() as db:
        history = RiskAssessmentRepository.get_user_assessments(db, user_id)

    if history:
        for item in history:
            st.markdown(
                f"""
                <div class="health-card">
                    <div style="display: flex; justify-content: space-between;">
                        <strong>{item.assessment_type}</strong>
                        <span>{item.risk_level} (Score: {item.score})</span>
                    </div>
                    <div style="font-size: 0.8rem; color: #64748b;">Completed on: {item.created_at.strftime('%B %d, %Y at %I:%M %p')}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("No saved assessments found yet. Complete an assessment above to track your results.")
