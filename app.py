"""
HealthAware AI - Home Dashboard & Application Entrypoint
A professional, dark-themed, evidence-grounded healthcare awareness platform.
Strictly Python + Streamlit. NO JAVASCRIPT.
"""

import streamlit as st
from datetime import date
from database.connection import get_db_session, init_db
from database.repositories import (
    UserRepository, HealthModuleRepository, QuizRepository,
    MedicationRepository, AppointmentRepository, MythFactRepository
)
from auth.authentication import AuthService, get_current_user, set_current_user
from components.common import render_header, render_disclaimer, apply_theme
from components.sidebar import render_sidebar
from data.seed_data.seed import seed_database

# ──────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HealthAware AI — Healthcare Awareness & Wellness",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────────────────────────────────────
# BOOTSTRAP: Init DB, seed, theme, sidebar
# ──────────────────────────────────────────────────────────────────────────────
if "db_initialized" not in st.session_state:
    try:
        seed_database()
    except Exception:
        init_db()
    st.session_state["db_initialized"] = True

apply_theme()
render_sidebar()

user = get_current_user()
if user:
    st.switch_page("pages/1_💬_AI_Health_Chat.py")

# ──────────────────────────────────────────────────────────────────────────────
# HERO HEADER
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="page-hero" style="background: linear-gradient(135deg,
            rgba(14,165,233,0.14) 0%, rgba(20,184,166,0.10) 40%,
            rgba(16,185,129,0.07) 100%); text-align: center; padding: 48px 40px;">
        <div style="font-size: 3rem; margin-bottom: 12px;">🩺</div>
        <div class="hero-title" style="font-size: 2.8rem;">
            <span class="grad-text">HealthAware AI</span>
        </div>
        <div class="hero-subtitle" style="text-align: center; margin: 10px auto 0;
                                          max-width: 600px; font-size: 1.1rem;">
            Your intelligent educational companion for preventive health, medical
            awareness, and daily wellness — powered by AI and verified knowledge.
        </div>
        <div style="margin-top: 20px; display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;">
            <span class="badge-teal">🔬 RAG-Powered Responses</span>
            &nbsp;
            <span class="badge-primary">🛡️ Safety-First Architecture</span>
            &nbsp;
            <span class="badge-green">📚 Verified Medical Sources</span>
            &nbsp;
            <span class="badge-violet">🌐 Multi-Language Support</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

render_disclaimer()

# ──────────────────────────────────────────────────────────────────────────────
# AUTHENTICATION SECTION (shown when not logged in)
# ──────────────────────────────────────────────────────────────────────────────
if not user:
    st.markdown(
        """
        <div style="text-align: center; margin: 8px 0 20px;">
            <div style="font-size: 1.05rem; color: #64748b;">
                🔑 Sign in to unlock full personalization, medication tracking, and chat history
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    auth_col1, auth_col2, auth_col3 = st.columns([1, 2, 1])
    with auth_col2:
        auth_tab1, auth_tab2 = st.tabs(["🔑 Sign In", "📝 Create Account"])

        with auth_tab1:
            st.markdown(
                """
                <div style="background: rgba(14,165,233,0.06); border: 1px solid rgba(14,165,233,0.15);
                            border-radius: 10px; padding: 12px 14px; margin-bottom: 14px;
                            font-size: 0.83rem; color: #7dd3fc;">
                    <strong>Demo Credentials:</strong><br>
                    • User: <code>demo</code> / <code>123</code><br>
                    • Admin: <code>admin</code> / <code>Admin@123</code>
                </div>
                """,
                unsafe_allow_html=True
            )
            with st.form("login_form", clear_on_submit=False):
                login_id = st.text_input(
                    "Username or Email",
                    placeholder="demouser",
                    key="login_id_input"
                )
                login_pwd = st.text_input(
                    "Password",
                    type="password",
                    placeholder="••••••••",
                    key="login_pwd_input"
                )
                submit_login = st.form_submit_button(
                    "🔑 Sign In to HealthAware AI",
                    use_container_width=True
                )
                if submit_login:
                    if not login_id or not login_pwd:
                        st.error("Please enter both username/email and password.")
                    else:
                        success, msg, u_data = AuthService.login_user(login_id, login_pwd)
                        if success:
                            set_current_user(u_data)
                            st.success(f"✅ Welcome back, {u_data.get('full_name') or u_data.get('username')}!")
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")

        with auth_tab2:
            with st.form("register_form", clear_on_submit=False):
                reg_name = st.text_input("Full Name", placeholder="Alex Morgan", key="reg_name_input")
                reg_username = st.text_input("Choose Username", placeholder="alex_m", key="reg_username_input")
                reg_email = st.text_input("Email Address", placeholder="alex@example.com", key="reg_email_input")
                reg_pwd = st.text_input(
                    "Password (min 6 characters)",
                    type="password",
                    key="reg_pwd_input"
                )
                submit_reg = st.form_submit_button(
                    "✅ Create My Account",
                    use_container_width=True
                )
                if submit_reg:
                    if not all([reg_name, reg_username, reg_email, reg_pwd]):
                        st.error("Please fill in all fields to register.")
                    else:
                        success, msg, u_data = AuthService.register_user(
                            reg_username, reg_email, reg_pwd, reg_name
                        )
                        if success:
                            set_current_user(u_data)
                            st.success(f"🎉 Account created! Welcome, {reg_name}!")
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")

    st.divider()

# ──────────────────────────────────────────────────────────────────────────────
# HEALTH METRICS OVERVIEW
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(
    "<div style='font-size:0.72rem; font-weight:700; color:#64748b; "
    "text-transform:uppercase; letter-spacing:0.1em; margin-bottom:14px;'>"
    "📊 Your Healthcare Overview</div>",
    unsafe_allow_html=True
)

with get_db_session() as db:
    user_id = user["id"] if user else None
    completed_modules = HealthModuleRepository.get_user_completion_count(db, user_id) if user_id else 0
    total_modules     = len(HealthModuleRepository.get_all(db))
    upcoming_appt     = AppointmentRepository.get_upcoming(db, user_id) if user_id else None
    adherence_rate    = MedicationRepository.get_adherence_rate(db, user_id) if user_id else 100.0
    recent_quiz       = QuizRepository.get_user_recent_attempt(db, user_id) if user_id else None

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric(
        label="📚 Modules Completed",
        value=f"{completed_modules}/{total_modules}",
        delta=f"{int(completed_modules/max(total_modules,1)*100)}% done" if total_modules else "0%",
        help="Health education modules finished"
    )
with m2:
    appt_val = upcoming_appt.specialty if upcoming_appt else "None Scheduled"
    appt_delta = f"{upcoming_appt.appointment_date}" if upcoming_appt else "All Clear ✓"
    st.metric(label="📅 Next Appointment", value=appt_val, delta=appt_delta)
with m3:
    adherence_delta = "✅ Optimal" if adherence_rate >= 80 else "⚠️ Needs Attention"
    st.metric(label="💊 Med Adherence (7d)", value=f"{adherence_rate:.0f}%", delta=adherence_delta)
with m4:
    quiz_val   = f"{recent_quiz.score}/{recent_quiz.total_questions}" if recent_quiz else "Not Taken"
    quiz_delta = f"Topic: {recent_quiz.topic.title()}" if recent_quiz else "Take a Quiz"
    st.metric(label="📝 Latest Quiz Score", value=quiz_val, delta=quiz_delta)

st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# PRIMARY FEATURE: AI CHAT CTA
# ──────────────────────────────────────────────────────────────────────────────
chat_cta_col, _ = st.columns([2, 1])
with chat_cta_col:
    st.markdown(
        """
        <div class="health-card" style="background: linear-gradient(135deg,
                rgba(14,165,233,0.15) 0%, rgba(20,184,166,0.10) 100%);
                border-color: rgba(14,165,233,0.30); padding: 28px 32px;">
            <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 12px;">
                <div style="font-size: 2.5rem;">💬</div>
                <div>
                    <div style="font-size: 1.3rem; font-weight: 700; color: #f1f5f9;">
                        AI Healthcare Chat
                    </div>
                    <div style="font-size: 0.9rem; color: #7dd3fc;">
                        Powered by RAG & Verified Medical Knowledge
                    </div>
                </div>
            </div>
            <div style="color: #94a3b8; font-size: 0.9rem; line-height: 1.6; margin-bottom: 16px;">
                Ask evidence-based questions about symptoms, preventive wellness, medical myths,
                and health topics. The AI synthesizes verified healthcare documentation to provide
                educational, citation-backed answers in real-time.
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                <span class="badge-teal">✓ Emergency Detection</span>
                <span class="badge-primary">✓ Source Citations</span>
                <span class="badge-green">✓ Mental Health Crisis Support</span>
                <span class="badge-violet">✓ Multi-Language</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
if st.button("💬 Open AI Health Chat →", key="btn_open_chat", use_container_width=False):
    st.switch_page("pages/1_💬_AI_Health_Chat.py")

st.divider()

# ──────────────────────────────────────────────────────────────────────────────
# FEATURE GRID
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(
    "<div style='font-size:0.72rem; font-weight:700; color:#64748b; "
    "text-transform:uppercase; letter-spacing:0.1em; margin-bottom:16px;'>"
    "⚡ All Features</div>",
    unsafe_allow_html=True
)

features = [
    {
        "icon": "🔍",
        "title": "Myth vs Fact",
        "desc": "Debunk viral medical misinformation with our searchable evidence-based myth-fact database.",
        "badge": "badge-rose",
        "badge_text": "Popular",
        "page": "pages/5_🔍_Myth_vs_Fact.py"
    },
    {
        "icon": "🩺",
        "title": "Symptom Checker",
        "desc": "Check symptom urgency via a guided clinical triage questionnaire. Educational only.",
        "badge": "badge-primary",
        "badge_text": "Triage Tool",
        "page": "pages/6_🩺_Symptom_Checker.py"
    },
    {
        "icon": "⚖️",
        "title": "Risk Assessment",
        "desc": "Evaluate educational lifestyle risk factors for Type 2 Diabetes and Hypertension.",
        "badge": "badge-violet",
        "badge_text": "Preventive",
        "page": "pages/4_⚖️_Risk_Assessment.py"
    },
    {
        "icon": "📚",
        "title": "Health Learning",
        "desc": "Bite-sized evidence-based health modules on nutrition, cardiology, and disease prevention.",
        "badge": "badge-green",
        "badge_text": "Education",
        "page": "pages/2_📚_Health_Learning.py"
    },
    {
        "icon": "📝",
        "title": "Health Quizzes",
        "desc": "Test your knowledge on diabetes, heart health, vaccines, and more with scored quizzes.",
        "badge": "badge-teal",
        "badge_text": "Interactive",
        "page": "pages/3_📝_Interactive_Quizzes.py"
    },
    {
        "icon": "💊",
        "title": "Medication Tracker",
        "desc": "Organize prescriptions, log daily doses, and monitor 7-day adherence rates.",
        "badge": "badge-primary",
        "badge_text": "Personal",
        "page": "pages/7_💊_Medications.py"
    },
    {
        "icon": "📅",
        "title": "Appointments",
        "desc": "Schedule and manage healthcare appointments with pre-visit preparation notes.",
        "badge": "badge-teal",
        "badge_text": "Scheduling",
        "page": "pages/8_📅_Appointments.py"
    },
    {
        "icon": "🧘",
        "title": "Mental Wellness",
        "desc": "Guided 4-7-8 box breathing, mood journaling, and 24/7 crisis lifelines.",
        "badge": "badge-violet",
        "badge_text": "Wellness",
        "page": "pages/11_🧘_Mental_Wellness.py"
    },
    {
        "icon": "🏥",
        "title": "Healthcare Directory",
        "desc": "Find hospitals, clinics, pharmacies, and emergency services near you.",
        "badge": "badge-green",
        "badge_text": "Directory",
        "page": "pages/9_🏥_Healthcare_Directory.py"
    },
]

# Render 3 columns
for row_start in range(0, len(features), 3):
    row_features = features[row_start:row_start + 3]
    cols = st.columns(3)
    for col, feat in zip(cols, row_features):
        with col:
            st.markdown(
                f"""
                <div class="feature-card">
                    <span class="fc-icon">{feat['icon']}</span>
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                        <h4 style="margin: 0 !important;">{feat['title']}</h4>
                        <span class="{feat['badge']}">{feat['badge_text']}</span>
                    </div>
                    <p>{feat['desc']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button(
                f"Open {feat['title']} →",
                key=f"feat_btn_{feat['title'].replace(' ', '_')}",
                use_container_width=True
            ):
                st.switch_page(feat['page'])
    st.markdown("<div style='margin-bottom: 4px;'></div>", unsafe_allow_html=True)

st.divider()

# ──────────────────────────────────────────────────────────────────────────────
# HEALTH FACT OF THE DAY
# ──────────────────────────────────────────────────────────────────────────────
with get_db_session() as db:
    random_myth = MythFactRepository.get_random(db)

if random_myth:
    st.markdown(
        "<div style='font-size:0.72rem; font-weight:700; color:#64748b; "
        "text-transform:uppercase; letter-spacing:0.1em; margin-bottom:14px;'>"
        "💡 Health Fact of the Day</div>",
        unsafe_allow_html=True
    )
    fact_col1, fact_col2 = st.columns([1, 1])
    with fact_col1:
        st.markdown(
            f"""
            <div class="myth-card">
                <div style="font-size: 0.75rem; font-weight: 700; color: #f87171;
                            text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px;">
                    ❌ Common Myth
                </div>
                <div style="color: #fca5a5; font-size: 1rem; font-weight: 600; line-height: 1.5;">
                    "{random_myth.myth}"
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with fact_col2:
        st.markdown(
            f"""
            <div class="fact-card">
                <div style="font-size: 0.75rem; font-weight: 700; color: #34d399;
                            text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px;">
                    ✅ The Real Fact
                </div>
                <div style="color: #a7f3d0; font-size: 1rem; font-weight: 600; line-height: 1.5; margin-bottom: 10px;">
                    {random_myth.fact}
                </div>
                <div style="color: #6ee7b7; font-size: 0.85rem; line-height: 1.6;">
                    {random_myth.explanation}
                </div>
                <div style="margin-top: 10px; font-size: 0.75rem; color: #64748b;">
                    📖 Source: {random_myth.source}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    if st.button("🔍 Explore All Myths & Facts", key="btn_goto_myths"):
        st.switch_page("pages/5_🔍_Myth_vs_Fact.py")

# ──────────────────────────────────────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="margin-top: 40px; padding: 24px; text-align: center;
                background: rgba(255,255,255,0.02); border-top: 1px solid rgba(255,255,255,0.06);
                border-radius: 16px 16px 0 0;">
        <div style="font-size: 1rem; font-weight: 700; color: #0ea5e9; margin-bottom: 6px;">
            🩺 HealthAware AI — Final Year Project
        </div>
        <div style="font-size: 0.82rem; color: #64748b; line-height: 1.6;">
            Built with Python · Streamlit · RAG · SQLite · Offline AI Engine<br>
            ⚕️ This platform is for educational awareness only and does not replace professional medical advice.
        </div>
        <div style="margin-top: 12px; display: flex; justify-content: center; gap: 16px; flex-wrap: wrap;
                    font-size: 0.78rem; color: #475569;">
            <span>🔒 Privacy-First Design</span>
            <span>•</span>
            <span>📚 Evidence-Based Content</span>
            <span>•</span>
            <span>🚨 Emergency Routing Built-In</span>
            <span>•</span>
            <span>🌐 Multi-Language Support</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
