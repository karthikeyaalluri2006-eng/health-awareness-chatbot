"""
HealthAware AI - Appointment Management Module
Schedule, view, and manage appointments across participating clinics and providers.
Uses a provider abstraction; clearly indicates demonstration booking.
Strictly Python + Streamlit. NO JAVASCRIPT.
"""

import streamlit as st
from datetime import date
from database.connection import get_db_session
from database.repositories import AppointmentRepository
from auth.authentication import get_current_user
from services.appointment_service import AppointmentService
from components.common import render_header, render_disclaimer, apply_theme
from components.sidebar import render_sidebar

st.set_page_config(page_title="Appointments - HealthAware AI", page_icon="📅", layout="wide")
apply_theme()
render_sidebar()

render_header(
    title="Healthcare Appointments",
    subtitle="Coordinate consultations with primary care providers, specialists, and telehealth networks.",
    icon="📅"
)

render_disclaimer()

user = get_current_user()
user_id = user["id"] if user else 1

tab_view, tab_book = st.tabs(["📅 Your Scheduled Consultations", "➕ Book Consultation"])

# ==============================================================================
# TAB 1: VIEW SCHEDULED APPOINTMENTS
# ==============================================================================
with tab_view:
    with get_db_session() as db:
        appts = AppointmentRepository.get_user_appointments(db, user_id)

    if not appts:
        st.info("You have no scheduled appointments. Use the 'Book Consultation' tab to set one up.")
    else:
        for a in appts:
            status_color = "#10b981" if a.status == "scheduled" else "#64748b"
            st.markdown(
                f"""
                <div class="health-card" style="border-left: 5px solid {status_color};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="margin: 0; color: #0f172a;">{a.specialty} — {a.provider_name}</h4>
                        <span class="badge-blue">{a.appointment_type}</span>
                    </div>
                    <div style="font-size: 0.95rem; color: #334155; margin: 8px 0;">
                        🏥 <strong>{a.clinic_name}</strong> • 🗓️ <strong>{a.appointment_date}</strong> at <strong>{a.appointment_time}</strong>
                    </div>
                    <div style="font-size: 0.85rem; color: #64748b;">
                        Notes: {a.notes or 'Routine consultation'} • Status: <strong>{a.status.title()}</strong>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if a.status == "scheduled":
                if st.button(f"Cancel Appointment #{a.id}", key=f"cancel_appt_{a.id}"):
                    with get_db_session() as db:
                        AppointmentRepository.cancel(db, a.id, user_id)
                    st.toast("Appointment has been cancelled.", icon="ℹ️")
                    st.rerun()

# ==============================================================================
# TAB 2: BOOK NEW APPOINTMENT
# ==============================================================================
with tab_book:
    st.subheader("➕ Schedule a Consultation (Demo Network)")
    st.caption("Select a clinic and available specialty to coordinate with provider schedules.")

    clinics = AppointmentService.get_clinics()
    clinic_names = [c["clinic_name"] for c in clinics]

    with st.form("book_appt_form"):
        selected_clinic_name = st.selectbox("Select Healthcare Facility", options=clinic_names)
        clinic_info = next(c for c in clinics if c["clinic_name"] == selected_clinic_name)

        specialties = clinic_info["specialties"]
        selected_specialty = st.selectbox("Select Medical Specialty", options=specialties)

        doctors = clinic_info["doctors"].get(selected_specialty, ["Staff Physician"])
        selected_doc = st.selectbox("Select Healthcare Practitioner", options=doctors)

        col1, col2, col3 = st.columns(3)
        with col1:
            appt_date = st.date_input("Preferred Date", min_value=date.today())
        with col2:
            time_slots = ["09:00 AM", "10:30 AM", "01:30 PM", "03:00 PM", "04:30 PM"]
            appt_time = st.selectbox("Available Time Slot", options=time_slots)
        with col3:
            appt_type = st.selectbox("Visit Type", ["In-Person Clinic Visit", "Telehealth Video Consultation"])

        notes = st.text_area("Reason for Visit (Brief summary for the clinic)", placeholder="e.g., Routine annual check-up, blood pressure review")

        submit_booking = st.form_submit_button("Confirm & Book Appointment", type="primary", use_container_width=True)

    if submit_booking:
        with get_db_session() as db:
            appt = AppointmentService.book_appointment(
                db=db,
                user_id=user_id,
                clinic_name=selected_clinic_name,
                specialty=selected_specialty,
                provider_name=selected_doc,
                appt_date=appt_date.isoformat(),
                appt_time=appt_time,
                appt_type=appt_type,
                notes=notes
            )
        st.success(f"🎉 Appointment confirmed with {selected_doc} on {appt_date.isoformat()} at {appt_time}!")
        st.info("A calendar reminder has been saved to your dashboard.")
