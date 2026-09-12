"""
HealthAware AI - Emergency Alert Component
Displays high-prominence medical emergency banners with verified regional hotlines.
"""

import streamlit as st
from safety.emergency_detection import EmergencyCheckResult, VERIFIED_EMERGENCY_HOTLINES


def render_emergency_banner(result: EmergencyCheckResult):
    """Renders prominent emergency alert card when acute symptoms are detected."""
    st.markdown(
        f"""
        <div class="emergency-banner-box">
            <h3 style="color: #b91c1c; margin-top: 0; display: flex; align-items: center; gap: 8px;">
                🚨 URGENT MEDICAL ATTENTION REQUIRED
            </h3>
            <p style="font-size: 1.05rem; font-weight: 600; line-height: 1.5; color: #7f1d1d;">
                {result.guidance}
            </p>
            <div style="margin-top: 12px; padding: 12px; background: #fee2e2; border-radius: 8px;">
                <strong>Identified Red-Flag Symptoms:</strong>
                <ul style="margin: 6px 0 0 0; padding-left: 20px;">
                    {"".join(f"<li>{flag}</li>" for flag in result.matched_flags)}
                </ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("📞 View Verified Emergency Contact Numbers", expanded=True):
        cols = st.columns(len(result.emergency_contacts) or 3)
        contacts = result.emergency_contacts or VERIFIED_EMERGENCY_HOTLINES[:3]
        for idx, contact in enumerate(contacts):
            col = cols[idx % len(cols)]
            with col:
                st.metric(label=contact["region"], value=contact["number"], help=contact["service"])


def render_crisis_banner(guidance: str, resources: list):
    """Renders supportive mental health crisis assistance card."""
    st.markdown(
        f"""
        <div style="background-color: #eff6ff; border: 2px solid #3b82f6; border-radius: 10px; padding: 18px; margin-bottom: 20px;">
            <h3 style="color: #1d4ed8; margin-top: 0;">💙 We Are Here With You — Free, Confidential Crisis Support</h3>
            <p style="font-size: 1.02rem; color: #1e3a8a; line-height: 1.5;">{guidance}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Available 24/7 Crisis Helplines:")
    for res in resources:
        st.markdown(f"• **{res['name']}** ({res['region']}): **{res['contact']}** — [Official Website]({res['website']})")
