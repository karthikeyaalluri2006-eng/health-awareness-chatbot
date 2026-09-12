"""
HealthAware AI - Mental Wellness & Relaxation
Features guided breathing animations, daily emotional mood check-ins,
wellness journaling, and 24/7 crisis support lifelines.
Strictly Python + Streamlit + CSS. NO JAVASCRIPT.
"""

import streamlit as st
from datetime import date
from database.connection import get_db_session
from database.repositories import WellnessRepository
from auth.authentication import get_current_user
from safety.crisis_detection import VERIFIED_CRISIS_RESOURCES
from components.common import render_header, render_disclaimer, apply_theme
from components.sidebar import render_sidebar

st.set_page_config(page_title="Mental Wellness - HealthAware AI", page_icon="🧘", layout="wide")
apply_theme()
render_sidebar()

render_header(
    title="Mental Wellness & Mindfulness",
    subtitle="Calming breathing exercises, stress-reduction techniques, and daily mood tracking.",
    icon="🧘"
)

render_disclaimer()

user = get_current_user()
user_id = user["id"] if user else 1

tab_breathe, tab_mood, tab_crisis = st.tabs([
    "🌬️ Guided Breathing Pacer",
    "📝 Daily Mood Check-In",
    "💙 24/7 Crisis Helplines"
])

# ==============================================================================
# TAB 1: GUIDED BREATHING PACER (PURE CSS ANIMATION - ZERO JS)
# ==============================================================================
with tab_breathe:
    st.subheader("Guided 4-7-8 Deep Relaxation Breathing")
    st.caption("Follow the expanding and contracting circle to regulate your parasympathetic nervous system.")

    # Pure CSS pulsing circle animation
    BREATHING_ANIMATION_CSS = """
    <style>
    @keyframes breathe478 {
        0% { transform: scale(1); background-color: #99f6e4; }
        21% { transform: scale(1.6); background-color: #2dd4bf; } /* Inhale 4s (approx 21% of 19s cycle) */
        58% { transform: scale(1.6); background-color: #0d9488; } /* Hold 7s (approx 37%) */
        100% { transform: scale(1); background-color: #99f6e4; }  /* Exhale 8s (approx 42%) */
    }
    .breathing-circle {
        width: 140px;
        height: 140px;
        border-radius: 50%;
        margin: 40px auto;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #0f172a;
        font-weight: 700;
        font-size: 1.1rem;
        box-shadow: 0 0 25px rgba(13, 148, 136, 0.35);
        animation: breathe478 19s infinite ease-in-out;
    }
    </style>
    <div style="text-align: center; padding: 20px 0;">
        <div class="breathing-circle">Breathe</div>
        <p style="font-size: 0.95rem; color: #475569;">
            <strong>Cycle:</strong> Inhale through nose (4s) ➔ Hold breath gently (7s) ➔ Exhale slowly through mouth (8s)
        </p>
    </div>
    """
    st.markdown(BREATHING_ANIMATION_CSS, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            **Benefits of 4-7-8 Breathing:**
            - Activates the vagus nerve to slow heart rate.
            - Lowers transient arterial blood pressure.
            - Helps calm racing thoughts before sleep or stressful tasks.
            """
        )
    with col2:
        st.markdown(
            """
            **Quick Grounding Technique (5-4-3-2-1):**
            - **5 things** you can see around you.
            - **4 things** you can physically touch.
            - **3 things** you can hear right now.
            - **2 things** you can smell.
            - **1 positive thing** you can appreciate about yourself today.
            """
        )

# ==============================================================================
# TAB 2: DAILY MOOD CHECK-IN & WELLNESS LOG
# ==============================================================================
with tab_mood:
    st.subheader("Daily Wellness & Mood Check-In")

    today_str = date.today().isoformat()

    with st.form("wellness_form"):
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            mood = st.selectbox(
                "How are you feeling emotionally today?",
                ["Energized & Positive", "Calm & Content", "A Bit Stressed", "Anxious / Overwhelmed", "Low Energy / Down"]
            )
            stress = st.slider("Perceived Stress Level (1 = Serene, 5 = Very High)", 1, 5, 2)

        with m_col2:
            sleep = st.number_input("Last Night's Sleep (Hours)", min_value=1.0, max_value=16.0, value=7.5, step=0.5)
            water = st.slider("Glasses of Water Today (approx 250ml each)", 0, 16, 8)

        notes = st.text_area("Wellness Reflections / Journaling", placeholder="Write anything on your mind today...")

        submit_mood = st.form_submit_button("Save Today's Check-In", type="primary", use_container_width=True)

    if submit_mood:
        with get_db_session() as db:
            WellnessRepository.log(
                db=db,
                user_id=user_id,
                log_date=today_str,
                mood=mood,
                stress=stress,
                sleep=sleep,
                water=water,
                notes=notes
            )
        st.success("✅ Your daily wellness log has been recorded.")
        st.rerun()

    # View recent wellness history
    st.subheader("📜 Recent Wellness Logs")
    with get_db_session() as db:
        recent_logs = WellnessRepository.get_recent(db, user_id, limit=5)

    if recent_logs:
        for r in recent_logs:
            st.markdown(
                f"""
                <div class="health-card">
                    <div style="display: flex; justify-content: space-between;">
                        <strong>🗓️ {r.log_date}</strong>
                        <span class="badge-blue">Mood: {r.mood}</span>
                    </div>
                    <div style="font-size: 0.9rem; color: #334155; margin-top: 6px;">
                        😴 Sleep: <strong>{r.sleep_hours} hrs</strong> • 💧 Water: <strong>{r.water_glasses} glasses</strong> • ⚡ Stress: <strong>{r.stress_level}/5</strong>
                    </div>
                    {f'<div style="font-size: 0.85rem; color: #64748b; margin-top: 4px;">"{r.notes}"</div>' if r.notes else ''}
                </div>
                """,
                unsafe_allow_html=True
            )

# ==============================================================================
# TAB 3: 24/7 CRISIS HELPLINES & PROFESSIONAL CARE
# ==============================================================================
with tab_crisis:
    st.markdown(
        """
        <div style="background-color: #eff6ff; border: 2px solid #3b82f6; border-radius: 10px; padding: 18px; margin-bottom: 20px;">
            <h3 style="color: #1d4ed8; margin-top: 0;">💙 You Don't Have to Carry This Alone</h3>
            <p style="color: #1e3a8a; line-height: 1.5;">
                If you are feeling overwhelmed, hopeless, or having thoughts of self-harm, compassionate and confidential support is available 24 hours a day, 7 days a week.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    for r in VERIFIED_CRISIS_RESOURCES:
        st.markdown(
            f"""
            <div class="health-card">
                <h4 style="margin: 0; color: #0284c7;">{r['name']} ({r['region']})</h4>
                <div style="font-size: 1rem; font-weight: 600; color: #0f172a; margin: 6px 0;">
                    📞 {r['contact']}
                </div>
                <a href="{r['website']}" target="_blank" style="font-size: 0.85rem; color: #0d9488; text-decoration: none;">
                    Visit Official Organization Website ↗
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )
