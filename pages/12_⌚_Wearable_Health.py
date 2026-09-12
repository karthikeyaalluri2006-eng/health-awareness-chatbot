"""
HealthAware AI - Wearable Health Hub & Activity Tracker
Displays biometric activity, resting heart rate, sleep metrics, and demo EHR health summaries.
Strict Rule: Wearable data is for wellness awareness only, not clinical diagnosis.
Strictly Python + Streamlit. NO JAVASCRIPT.
"""

# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
from database.connection import get_db_session
from database.repositories import WearableRepository
from auth.authentication import get_current_user
from services.wearable_service import get_wearable_provider
from services.ehr_service import get_ehr_provider
from components.common import render_header, render_disclaimer, apply_theme
from components.sidebar import render_sidebar

st.set_page_config(page_title="Wearable Health - HealthAware AI", page_icon="⌚", layout="wide")
apply_theme()
render_sidebar()

render_header(
    title="Wearable Health & Activity Hub",
    subtitle="Connect smart wearables, review daily activity trends, and inspect interoperable health summaries.",
    icon="⌚"
)

render_disclaimer()

user = get_current_user()
user_id = user["id"] if user else 1

tab_wearable, tab_ehr = st.tabs(["⌚ Wearable Metrics", "🏥 Interoperable Health Records (EHR)"])

# ==============================================================================
# TAB 1: WEARABLE DATA SYNC & VISUALIZATION
# ==============================================================================
with tab_wearable:
    c_btn1, c_btn2 = st.columns([1, 3])
    with c_btn1:
        if st.button("🔄 Sync Latest Device Data", type="primary", use_container_width=True):
            wp = get_wearable_provider()
            new_records = wp.sync_data(user_id, days=7)
            with get_db_session() as db:
                for r in new_records:
                    WearableRepository.add_record(
                        db=db,
                        user_id=user_id,
                        record_date=r["record_date"],
                        provider=r["provider"],
                        steps=r["steps"],
                        hr=r["resting_heart_rate"],
                        active_mins=r["active_minutes"],
                        sleep_mins=r["sleep_minutes"],
                        quality=r["sleep_quality_score"]
                    )
            st.toast("Synchronized with wearable provider!", icon="⌚")
            st.rerun()

    with c_btn2:
        st.caption("Supports Apple Health, Google Health Connect, and Fitbit through simulated secure adapters.")

    # Fetch recent records from database
    with get_db_session() as db:
        records = WearableRepository.get_recent(db, user_id, days=7)

    if not records:
        st.info("No wearable data found. Click 'Sync Latest Device Data' above to populate sample activity.")
    else:
        latest = records[0]

        # Top Metric Cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="Daily Steps", value=f"{latest.steps:,}", delta="+420 vs avg" if latest.steps > 7000 else "-250")
        with col2:
            st.metric(label="Resting Heart Rate", value=f"{latest.resting_heart_rate} bpm", delta="Normal")
        with col3:
            sleep_hrs = round(latest.sleep_minutes / 60.0, 1)
            st.metric(label="Sleep Duration", value=f"{sleep_hrs} hrs", delta=f"{latest.sleep_quality_score}% Quality")
        with col4:
            st.metric(label="Active Minutes", value=f"{latest.active_minutes} mins", delta="Goal: 30m")

        st.subheader("📈 7-Day Activity & Biometrics Log")
        table_data = [
            {
                "Date": r.record_date,
                "Device": r.provider,
                "Steps": r.steps,
                "Resting HR (bpm)": r.resting_heart_rate,
                "Active Mins": r.active_minutes,
                "Sleep (Hours)": round(r.sleep_minutes / 60.0, 1),
                "Sleep Quality Score": f"{r.sleep_quality_score} / 100"
            }
            for r in records
        ]
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True)

        st.line_chart(df.set_index("Date")[["Steps"]])

# ==============================================================================
# TAB 2: MOCK EHR / FHIR INTEROPERABILITY PREVIEW
# ==============================================================================
with tab_ehr:
    st.subheader("🏥 Electronic Health Record (EHR) Summary")
    st.caption("Structured using standard HL7 FHIR resource schemas (Demonstration Patient Data).")

    ehr_provider = get_ehr_provider()
    summary = ehr_provider.get_patient_summary("PATIENT-DEMO-001")

    st.markdown(
        f"""
        <div class="health-card" style="background: #f8fafc; border-left: 4px solid #0284c7;">
            <strong>Demo Patient:</strong> {summary['patient']['name']} • <strong>Birth Date:</strong> {summary['patient']['birthDate']}
            <div style="font-size: 0.8rem; color: #64748b; margin-top: 4px;">{summary['disclaimer']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    ehr_c1, ehr_c2 = st.columns(2)
    with ehr_c1:
        st.markdown("#### ⚠️ Known Allergies")
        for a in summary["allergies"]:
            st.markdown(f"• **{a['substance']}** ({a['severity']}): {a['reaction']}")

        st.markdown("#### 💉 Immunization History")
        for imm in summary["immunizations"]:
            st.markdown(f"• **{imm['vaccine']}** — Completed on `{imm['date']}`")

    with ehr_c2:
        st.markdown("#### 🧪 Recent Laboratory Bloodwork")
        labs_df = pd.DataFrame(summary["recent_labs"])
        st.dataframe(labs_df, use_container_width=True)
