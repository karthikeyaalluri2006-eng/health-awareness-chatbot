"""
HealthAware AI - Risk Assessment UI Component
Displays educational risk scores, contributing factor breakdown,
and recommended preventive conversations with licensed doctors.
"""

import streamlit as st
from typing import List, Dict, Any


def render_risk_result_card(
    assessment_name: str,
    risk_level: str,
    score: float,
    factors: List[str],
    recommendations: List[str]
):
    """Renders educational risk evaluation card with safe, non-diagnostic wording."""
    if "Lower" in risk_level:
        badge_class = "badge-teal"
        border_color = "#10b981"
    elif "Moderate" in risk_level:
        badge_class = "badge-blue"
        border_color = "#3b82f6"
    else:
        badge_class = "badge-blue"
        border_color = "#f97316"

    st.markdown(
        f"""
        <div class="health-card" style="border-top: 5px solid {border_color};">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <h3 style="color: #0f172a; margin: 0;">{assessment_name}</h3>
                <span class="{badge_class}" style="font-size: 0.95rem; padding: 6px 14px;">{risk_level}</span>
            </div>
            <p style="font-size: 0.95rem; color: #475569; margin-bottom: 16px;">
                Educational score metric: <strong>{score}</strong>. This score assesses lifestyle and demographic indicators from standard public health models.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Contributing Factors")
        if factors:
            for f in factors:
                st.markdown(f"• {f}")
        else:
            st.info("No significant risk factors flagged based on responses provided.")

    with c2:
        st.subheader("Preventive Health Considerations")
        for rec in recommendations:
            st.markdown(f"✅ {rec}")

    st.warning(
        "⚕️ **Non-Diagnostic Notice:** This assessment is intended solely for educational awareness. "
        "It cannot diagnose medical conditions or predict future illness with certainty. "
        "Share these results with your healthcare provider to discuss personalized screening."
    )
