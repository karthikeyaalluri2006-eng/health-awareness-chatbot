"""
HealthAware AI - Medication Management & Adherence Tracker
Tracks daily prescription schedules, logs doses, and monitors adherence rates.
Strict Rule: Never prescribes medication or alters doctor-prescribed doses.
Strictly Python + Streamlit. NO JAVASCRIPT.
"""

import streamlit as st
import json
from database.connection import get_db_session
from database.repositories import MedicationRepository
from auth.authentication import get_current_user
from services.medication_service import MedicationService
from components.common import render_header, render_disclaimer, apply_theme
from components.sidebar import render_sidebar

st.set_page_config(page_title="Medications - HealthAware AI", page_icon="💊", layout="wide")
apply_theme()
render_sidebar()

render_header(
    title="Medication Schedule & Adherence",
    subtitle="Keep track of doctor-prescribed regimens, daily dosage logs, and upcoming refills.",
    icon="💊"
)

render_disclaimer()

user = get_current_user()
user_id = user["id"] if user else 1

tab_today, tab_manage, tab_add = st.tabs(["📅 Today's Schedule", "📋 All Medications", "➕ Add Medication"])

# ==============================================================================
# TAB 1: TODAY'S SCHEDULE & ADHERENCE
# ==============================================================================
with tab_today:
    with get_db_session() as db:
        stats = MedicationService.get_adherence_stats(db, user_id)
        schedule = MedicationService.get_daily_schedule(db, user_id)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric(
            label="7-Day Medication Adherence",
            value=f"{stats['adherence_percentage']}%",
            delta=stats["status_label"]
        )
    with col2:
        st.info("💡 Logging your doses helps maintain steady therapeutic levels as directed by your physician.")

    st.subheader("Today's Doses")
    if not schedule:
        st.info("No active medications found. Add your prescribed medications in the 'Add Medication' tab.")
    else:
        for item in schedule:
            with st.container():
                c_time, c_info, c_actions = st.columns([1, 2.5, 2])
                with c_time:
                    st.markdown(f"### ⏰ {item['time']}")
                with c_info:
                    st.markdown(f"**{item['name']}** ({item['dosage']})")
                    st.caption(f"Instructions: {item['instructions']} • Refill: {item['refill_date']}")
                with c_actions:
                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        if st.button("✅ Taken", key=f"taken_{item['medication_id']}_{item['time']}"):
                            with get_db_session() as db:
                                MedicationService.log_status(db, item["medication_id"], user_id, item["time"], "taken")
                            st.toast(f"Logged {item['name']} as taken!", icon="💊")
                            st.rerun()
                    with btn_col2:
                        if st.button("⏭️ Skipped", key=f"skipped_{item['medication_id']}_{item['time']}"):
                            with get_db_session() as db:
                                MedicationService.log_status(db, item["medication_id"], user_id, item["time"], "skipped")
                            st.toast(f"Logged {item['name']} as skipped.", icon="ℹ️")
                            st.rerun()
                st.divider()

# ==============================================================================
# TAB 2: MANAGE MEDICATIONS
# ==============================================================================
with tab_manage:
    st.subheader("📋 Your Registered Prescriptions")
    with get_db_session() as db:
        meds = MedicationRepository.get_user_medications(db, user_id)

    if not meds:
        st.info("No medications on file.")
    else:
        for m in meds:
            st.markdown(
                f"""
                <div class="health-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="margin: 0; color: #0d9488;">{m.name} ({m.dosage})</h4>
                        <span class="badge-teal">{m.frequency}</span>
                    </div>
                    <p style="margin: 8px 0 4px 0; color: #334155; font-size: 0.92rem;">
                        <strong>Instructions:</strong> {m.instructions or 'Take as prescribed'}
                    </p>
                    <div style="font-size: 0.8rem; color: #64748b;">
                        Next Refill Target: <strong>{m.refill_date or 'None set'}</strong>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button(f"🗑️ Remove {m.name}", key=f"del_med_{m.id}"):
                with get_db_session() as db:
                    MedicationRepository.delete(db, m.id, user_id)
                st.toast(f"Removed {m.name}.", icon="🗑️")
                st.rerun()

# ==============================================================================
# TAB 3: ADD NEW MEDICATION
# ==============================================================================
with tab_add:
    st.subheader("➕ Register a Prescribed Medication")
    st.warning("⚠️ Never start, stop, or change medication dosages without consulting your doctor or pharmacist.")

    with st.form("add_med_form"):
        med_name = st.text_input("Medication Brand or Generic Name", placeholder="e.g., Metformin, Lisinopril")
        med_dose = st.text_input("Dosage Strength", placeholder="e.g., 500 mg, 10 mg, 1 puff")
        med_freq = st.selectbox("Frequency", ["Once daily", "Twice daily", "Three times daily", "As needed (PRN)"])
        med_time = st.time_input("Primary Reminder Time")
        med_notes = st.text_area("Physician's Instructions", placeholder="e.g., Take with evening meal, avoid grapefruit")
        med_refill = st.date_input("Target Refill Date")

        save_med = st.form_submit_button("Save Medication Schedule", type="primary", use_container_width=True)

    if save_med:
        if not med_name.strip() or not med_dose.strip():
            st.error("Please provide both Medication Name and Dosage Strength.")
        else:
            time_str = med_time.strftime("%H:%M")
            with get_db_session() as db:
                MedicationRepository.add(
                    db=db,
                    user_id=user_id,
                    name=med_name,
                    dosage=med_dose,
                    frequency=med_freq,
                    times=[time_str],
                    instructions=med_notes,
                    refill_date=med_refill.isoformat()
                )
            st.success(f"Successfully added {med_name} to your schedule!")
            st.rerun()
