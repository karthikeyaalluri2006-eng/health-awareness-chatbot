"""
HealthAware AI - User Profile & Privacy Controls
Manage display preferences, emergency contacts, data export, and deletion (GDPR/HIPAA principles).
Strictly Python + Streamlit. NO JAVASCRIPT.
"""

import streamlit as st
import json
from database.connection import get_db_session
from database.repositories import UserRepository, MedicationRepository, AppointmentRepository, WellnessRepository
from auth.authentication import get_current_user, set_current_user, logout_user
from components.common import render_header, render_disclaimer, apply_theme
from components.sidebar import render_sidebar

st.set_page_config(page_title="User Profile - HealthAware AI", page_icon="👤", layout="wide")
apply_theme()
render_sidebar()

render_header(
    title="User Profile & Privacy Controls",
    subtitle="Manage account preferences, emergency contacts, and personal data portability.",
    icon="👤"
)

render_disclaimer()

user = get_current_user()

if not user:
    st.info("💡 You are currently browsing as a Guest. Please sign in on the Home Dashboard to manage personal profiles.")
    st.stop()

tab_settings, tab_privacy = st.tabs(["⚙️ Profile Preferences", "🔒 Privacy & Data Portability"])

# ==============================================================================
# TAB 1: PROFILE SETTINGS
# ==============================================================================
with tab_settings:
    st.subheader("Account Details")
    with st.form("profile_form"):
        full_name = st.text_input("Full Name", value=user.get("full_name", ""))
        email = st.text_input("Email Address", value=user.get("email", ""), disabled=True)
        username = st.text_input("Username", value=user.get("username", ""), disabled=True)

        languages = {"en": "English", "te": "Telugu", "hi": "Hindi", "ta": "Tamil", "kn": "Kannada", "bn": "Bengali", "es": "Spanish"}
        current_lang = user.get("language", "en")
        selected_lang = st.selectbox(
            "Preferred Language",
            options=list(languages.keys()),
            format_func=lambda k: languages[k],
            index=list(languages.keys()).index(current_lang) if current_lang in languages else 0
        )

        submit_profile = st.form_submit_button("Save Changes", type="primary")

    if submit_profile:
        with get_db_session() as db:
            updated_user = UserRepository.update_preferences(db, user["id"], full_name=full_name, language=selected_lang)
            if updated_user:
                user["full_name"] = updated_user.full_name
                user["language"] = updated_user.preferred_language
                set_current_user(user)
                st.session_state["preferred_language"] = selected_lang
                st.success("Profile preferences updated successfully!")
                st.rerun()

# ==============================================================================
# TAB 2: PRIVACY & DATA PORTABILITY (GDPR & HIPAA ARCHITECTURE)
# ==============================================================================
with tab_privacy:
    st.subheader("Data Export (Right to Access & Portability)")
    st.caption("Download a copy of all health entries, medication logs, and appointments stored on your account.")

    with get_db_session() as db:
        user_meds = MedicationRepository.get_user_medications(db, user["id"])
        user_appts = AppointmentRepository.get_user_appointments(db, user["id"])
        user_wellness = WellnessRepository.get_recent(db, user["id"], limit=30)

    export_payload = {
        "user": {"username": user["username"], "full_name": user["full_name"]},
        "medications": [{"name": m.name, "dosage": m.dosage, "frequency": m.frequency} for m in user_meds],
        "appointments": [{"clinic": a.clinic_name, "specialty": a.specialty, "date": a.appointment_date} for a in user_appts],
        "wellness_logs": [{"date": w.log_date, "mood": w.mood, "sleep": w.sleep_hours} for w in user_wellness]
    }

    json_str = json.dumps(export_payload, indent=2)
    st.download_button(
        label="📥 Export Health Data as JSON",
        data=json_str,
        file_name=f"healthaware_export_{user['username']}.json",
        mime="application/json",
        use_container_width=True
    )

    st.divider()

    st.subheader("Data Deletion (Right to Erasure)")
    st.warning("⚠️ Deleting your account will permanently remove your stored conversations, medication logs, and profile records.")

    if st.button("🗑️ Delete My Account & All Health Records", type="secondary"):
        with get_db_session() as db:
            UserRepository.delete_user(db, user["id"])
        logout_user()
        st.success("Your account and all associated health records have been permanently erased.")
        st.rerun()
