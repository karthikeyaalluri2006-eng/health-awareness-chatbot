"""
HealthAware AI - Premium Medical Design System
Professional healthcare UI with glassmorphism, gradients, and micro-animations.
Strictly pure Streamlit and custom CSS. NO JAVASCRIPT.
"""

import streamlit as st
from services.localization_service import translate_ui

MEDICAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* ============================================================
   GLOBAL RESET & THEME VARIABLES
   ============================================================ */
:root {
    --primary:       #0ea5e9;
    --primary-dark:  #0284c7;
    --primary-glow:  rgba(14, 165, 233, 0.25);
    --teal:          #14b8a6;
    --teal-dark:     #0d9488;
    --emerald:       #10b981;
    --violet:        #8b5cf6;
    --rose:          #f43f5e;
    --amber:         #f59e0b;

    --bg-main:       #0a0f1e;
    --bg-card:       rgba(15, 23, 42, 0.85);
    --bg-glass:      rgba(255, 255, 255, 0.05);
    --bg-glass-hover:rgba(255, 255, 255, 0.09);
    --border-glass:  rgba(255, 255, 255, 0.10);
    --border-glow:   rgba(14, 165, 233, 0.40);
    --text-primary:  #f1f5f9;
    --text-secondary:#94a3b8;
    --text-muted:    #64748b;

    --radius-sm:     8px;
    --radius-md:     14px;
    --radius-lg:     20px;
    --radius-xl:     28px;

    --shadow-card:   0 4px 24px rgba(0,0,0,0.35), 0 1px 4px rgba(0,0,0,0.2);
    --shadow-glow:   0 0 30px rgba(14, 165, 233, 0.15);
    --shadow-teal:   0 0 30px rgba(20, 184, 166, 0.15);

    --transition:    all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ============================================================
   STREAMLIT CORE OVERRIDES
   ============================================================ */
.stApp {
    background: linear-gradient(135deg, #060b18 0%, #0a0f1e 40%, #0c1a2e 70%, #060b18 100%) !important;
    min-height: 100vh;
    font-family: 'Inter', 'Plus Jakarta Sans', sans-serif !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1528 0%, #0a1220 100%) !important;
    border-right: 1px solid var(--border-glass) !important;
    backdrop-filter: blur(20px);
}
section[data-testid="stSidebar"] > div {
    background: transparent !important;
}
section[data-testid="stSidebar"] > div > div {
    display: flex !important;
    flex-direction: column !important;
}
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
    order: 1 !important;
}
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
    display: none !important;
}
section[data-testid="stSidebar"] nav {
    display: none !important;
}

/* Main content */
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 1300px !important;
}

.healthaware-top-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    min-height: 58px;
    padding: 5px 0 10px;
}
.healthaware-top-mark {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 12px;
    background: linear-gradient(135deg, #0284c7, #0d9488);
    box-shadow: 0 5px 18px rgba(14, 165, 233, 0.25);
    font-size: 1.35rem;
}
.healthaware-top-name {
    color: #f1f5f9;
    font-size: 1.05rem;
    font-weight: 800;
    line-height: 1.1;
}
.healthaware-top-caption {
    color: #64748b;
    font-size: 0.72rem;
    margin-top: 3px;
}

/* Text elements */
h1, h2, h3, h4, h5, h6, p, label, span, div {
    font-family: 'Inter', 'Plus Jakarta Sans', sans-serif !important;
}
h1, h2, h3 { color: var(--text-primary) !important; }
h4, h5, h6 { color: var(--text-secondary) !important; }

/* Metric cards */
[data-testid="metric-container"] {
    background: var(--bg-glass) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: var(--radius-md) !important;
    padding: 16px 20px !important;
    backdrop-filter: blur(12px);
    transition: var(--transition);
}
[data-testid="metric-container"]:hover {
    border-color: var(--border-glow) !important;
    box-shadow: var(--shadow-glow) !important;
    transform: translateY(-2px);
}
[data-testid="stMetricLabel"] { color: var(--text-secondary) !important; font-size: 0.82rem !important; }
[data-testid="stMetricValue"] { color: var(--primary) !important; font-weight: 700 !important; }
[data-testid="stMetricDelta"] { font-size: 0.75rem !important; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--primary-dark) 0%, var(--teal-dark) 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    padding: 10px 20px !important;
    letter-spacing: 0.01em !important;
    transition: var(--transition) !important;
    box-shadow: 0 2px 12px rgba(2, 132, 199, 0.25) !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(2, 132, 199, 0.40) !important;
    filter: brightness(1.08) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* Chat input */
[data-testid="stChatInput"] {
    background: rgba(15, 23, 42, 0.9) !important;
    border: 1.5px solid var(--border-glass) !important;
    border-radius: var(--radius-lg) !important;
    color: var(--text-primary) !important;
    backdrop-filter: blur(12px);
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px var(--primary-glow) !important;
}
[data-testid="stChatInput"] textarea {
    color: var(--text-primary) !important;
    background: transparent !important;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: var(--bg-glass) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: var(--radius-md) !important;
    padding: 16px 20px !important;
    backdrop-filter: blur(8px);
    margin-bottom: 10px !important;
    animation: fadeInUp 0.3s ease-out;
}
[data-testid="stChatMessage"][data-testid*="user"] {
    border-color: rgba(14, 165, 233, 0.20) !important;
    background: rgba(14, 165, 233, 0.06) !important;
}
[data-testid="stChatMessage"][data-testid*="assistant"] {
    border-color: rgba(20, 184, 166, 0.20) !important;
    background: rgba(20, 184, 166, 0.05) !important;
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

@media (max-width: 768px) {
    .block-container {
        padding: 0.75rem 0.65rem 2.5rem !important;
    }
    .page-hero {
        padding: 24px 16px !important;
    }
    .hero-title {
        font-size: 1.75rem !important;
        line-height: 1.2 !important;
    }
    [data-testid="stChatMessage"] {
        padding: 12px 14px !important;
        border-radius: 12px !important;
    }
    [data-testid="stChatInput"] {
        margin: 0 0.25rem !important;
    }
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-glass) !important;
    border-radius: var(--radius-md) !important;
    border: 1px solid var(--border-glass) !important;
    padding: 4px !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-secondary) !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 500 !important;
    transition: var(--transition) !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--primary-dark), var(--teal-dark)) !important;
    color: white !important;
    font-weight: 600 !important;
}

/* Inputs & Selects */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
    background: rgba(15, 23, 42, 0.8) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    transition: var(--transition) !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 2px var(--primary-glow) !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: var(--bg-glass) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}
.streamlit-expanderContent {
    background: rgba(10, 15, 30, 0.6) !important;
    border: 1px solid var(--border-glass) !important;
    border-top: none !important;
    border-radius: 0 0 var(--radius-sm) var(--radius-sm) !important;
}

/* Divider */
hr { border-color: var(--border-glass) !important; margin: 1.5rem 0 !important; }

/* Alerts & Info */
.stAlert {
    border-radius: var(--radius-md) !important;
    border: 1px solid !important;
}
.stInfo {
    background: rgba(14, 165, 233, 0.08) !important;
    border-color: rgba(14, 165, 233, 0.25) !important;
    color: #bae6fd !important;
}
.stSuccess {
    background: rgba(16, 185, 129, 0.08) !important;
    border-color: rgba(16, 185, 129, 0.30) !important;
    color: #a7f3d0 !important;
}
.stError {
    background: rgba(244, 63, 94, 0.08) !important;
    border-color: rgba(244, 63, 94, 0.30) !important;
    color: #fda4af !important;
}
.stWarning {
    background: rgba(245, 158, 11, 0.08) !important;
    border-color: rgba(245, 158, 11, 0.30) !important;
    color: #fde68a !important;
}

/* Spinner */
.stSpinner > div { border-top-color: var(--primary) !important; }

/* Selectbox label */
.stSelectbox label, .stTextInput label, .stTextArea label,
.stNumberInput label, .stRadio label, .stCheckbox label,
.stSlider label, .stDateInput label {
    color: var(--text-secondary) !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
}

/* Dataframes / Tables */
.stDataFrame { border-radius: var(--radius-md) !important; overflow: hidden !important; }
.stDataFrame thead th {
    background: rgba(14, 165, 233, 0.12) !important;
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}
.stDataFrame tbody tr:nth-child(even) td {
    background: rgba(255, 255, 255, 0.02) !important;
}
.stDataFrame tbody tr td { color: var(--text-secondary) !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(148, 163, 184, 0.2); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(148, 163, 184, 0.4); }

/* ============================================================
   CUSTOM COMPONENT CLASSES
   ============================================================ */

/* Glassmorphism Card */
.health-card {
    background: var(--bg-glass);
    border: 1px solid var(--border-glass);
    border-radius: var(--radius-lg);
    padding: 24px;
    margin-bottom: 16px;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    box-shadow: var(--shadow-card);
    transition: var(--transition);
    position: relative;
    overflow: hidden;
}
.health-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
}
.health-card:hover {
    border-color: var(--border-glow);
    box-shadow: var(--shadow-card), var(--shadow-glow);
    transform: translateY(-2px);
}

/* Feature Card */
.feature-card {
    background: var(--bg-glass);
    border: 1px solid var(--border-glass);
    border-radius: var(--radius-lg);
    padding: 20px;
    margin-bottom: 12px;
    backdrop-filter: blur(12px);
    transition: var(--transition);
    position: relative;
    overflow: hidden;
}
.feature-card:hover {
    border-color: var(--border-glow);
    box-shadow: var(--shadow-glow);
    transform: translateY(-2px);
}
.feature-card .fc-icon {
    font-size: 2rem;
    margin-bottom: 10px;
    display: block;
}
.feature-card h4 {
    color: var(--text-primary) !important;
    margin: 0 0 8px 0 !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
}
.feature-card p {
    color: var(--text-secondary) !important;
    font-size: 0.855rem !important;
    line-height: 1.6 !important;
    margin: 0 !important;
}

/* Gradient text */
.grad-text {
    background: linear-gradient(135deg, var(--primary) 0%, var(--teal) 50%, var(--emerald) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 800;
}

/* Page hero header */
.page-hero {
    background: linear-gradient(135deg, rgba(14,165,233,0.12) 0%, rgba(20,184,166,0.08) 50%, rgba(16,185,129,0.06) 100%);
    border: 1px solid rgba(14, 165, 233, 0.15);
    border-radius: var(--radius-xl);
    padding: 36px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(16px);
}
.page-hero::after {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(14,165,233,0.12) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}
.page-hero .hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: var(--text-primary);
    margin: 0 0 8px 0;
    line-height: 1.15;
}
.page-hero .hero-subtitle {
    font-size: 1.05rem;
    color: var(--text-secondary);
    margin: 0;
    line-height: 1.6;
    max-width: 700px;
}

/* Disclaimer banner */
.disclaimer-banner {
    background: rgba(14, 165, 233, 0.07);
    border: 1px solid rgba(14, 165, 233, 0.20);
    border-left: 4px solid var(--primary);
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    padding: 12px 16px;
    margin-bottom: 22px;
    font-size: 0.865rem;
    color: #bae6fd;
    line-height: 1.5;
}

/* Emergency banner */
.emergency-banner-box {
    background: rgba(244, 63, 94, 0.10);
    border: 2px solid rgba(244, 63, 94, 0.60);
    border-radius: var(--radius-md);
    padding: 20px 24px;
    margin-bottom: 20px;
    animation: pulse-border 1.5s ease-in-out infinite;
}
@keyframes pulse-border {
    0%, 100% { border-color: rgba(244, 63, 94, 0.60); }
    50%       { border-color: rgba(244, 63, 94, 1.00); }
}

/* Badge pills */
.badge-primary {
    background: rgba(14, 165, 233, 0.18);
    color: #7dd3fc;
    border: 1px solid rgba(14, 165, 233, 0.30);
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    display: inline-block;
}
.badge-teal {
    background: rgba(20, 184, 166, 0.18);
    color: #5eead4;
    border: 1px solid rgba(20, 184, 166, 0.30);
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    display: inline-block;
}
.badge-green {
    background: rgba(16, 185, 129, 0.18);
    color: #6ee7b7;
    border: 1px solid rgba(16, 185, 129, 0.30);
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    display: inline-block;
}
.badge-rose {
    background: rgba(244, 63, 94, 0.15);
    color: #fda4af;
    border: 1px solid rgba(244, 63, 94, 0.30);
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    display: inline-block;
}
.badge-violet {
    background: rgba(139, 92, 246, 0.18);
    color: #c4b5fd;
    border: 1px solid rgba(139, 92, 246, 0.30);
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    display: inline-block;
}

/* Stat pill */
.stat-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--bg-glass);
    border: 1px solid var(--border-glass);
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 0.82rem;
    color: var(--text-secondary);
}

/* Source card */
.source-card {
    background: rgba(14, 165, 233, 0.05);
    border-left: 3px solid var(--primary);
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    padding: 10px 14px;
    margin-bottom: 8px;
}
.source-card .source-title {
    font-weight: 600;
    font-size: 0.88rem;
    color: var(--text-primary);
}
.source-card .source-meta {
    font-size: 0.78rem;
    color: var(--text-muted);
    margin-top: 3px;
}

/* Myth/Fact card */
.myth-card {
    background: rgba(244, 63, 94, 0.07);
    border: 1px solid rgba(244, 63, 94, 0.20);
    border-radius: var(--radius-md);
    padding: 18px 20px;
    margin-bottom: 12px;
}
.fact-card {
    background: rgba(16, 185, 129, 0.07);
    border: 1px solid rgba(16, 185, 129, 0.20);
    border-radius: var(--radius-md);
    padding: 18px 20px;
    margin-bottom: 16px;
}

/* Sidebar user card */
.sidebar-user-card {
    background: linear-gradient(135deg, rgba(14,165,233,0.12), rgba(20,184,166,0.08));
    border: 1px solid rgba(14, 165, 233, 0.25);
    border-radius: var(--radius-md);
    padding: 12px 14px;
    margin-bottom: 14px;
}

/* Risk level indicators */
.risk-low    { color: #34d399; font-weight: 700; }
.risk-medium { color: #fbbf24; font-weight: 700; }
.risk-high   { color: #f87171; font-weight: 700; }

/* Progress bar override */
.stProgress > div > div > div { background: linear-gradient(90deg, var(--primary), var(--teal)) !important; border-radius: 4px !important; }
.stProgress > div > div { background: rgba(255,255,255,0.07) !important; border-radius: 4px !important; }

/* Form submit button */
[data-testid="stForm"] .stButton > button {
    background: linear-gradient(135deg, var(--primary-dark) 0%, var(--teal-dark) 100%) !important;
    width: 100% !important;
    padding: 12px 20px !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 4px 16px rgba(2, 132, 199, 0.35) !important;
}

/* Sidebar nav links */
.sidebar-nav-link {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 9px 12px;
    border-radius: var(--radius-sm);
    color: var(--text-secondary);
    font-size: 0.875rem;
    font-weight: 500;
    transition: var(--transition);
    margin-bottom: 2px;
    text-decoration: none;
}

/* Typing dots animation */
@keyframes typingDot {
    0%, 60%, 100% { transform: translateY(0); opacity: 0.5; }
    30%            { transform: translateY(-6px); opacity: 1; }
}
.typing-dot {
    display: inline-block;
    width: 6px; height: 6px;
    background: var(--primary);
    border-radius: 50%;
    margin: 0 2px;
    animation: typingDot 1.2s ease-in-out infinite;
}
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }

/* Markdown text in dark theme */
.stMarkdown p { color: var(--text-secondary) !important; line-height: 1.7 !important; }
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 { color: var(--text-primary) !important; }
.stMarkdown strong { color: var(--text-primary) !important; font-weight: 700 !important; }
.stMarkdown li { color: var(--text-secondary) !important; line-height: 1.7 !important; }
.stMarkdown code {
    background: rgba(14, 165, 233, 0.12) !important;
    color: #7dd3fc !important;
    border-radius: 4px !important;
    padding: 1px 6px !important;
    font-size: 0.87em !important;
}

/* Sidebar selectbox & radios */
.css-1d391kg .stSelectbox label, .css-1d391kg p { color: var(--text-secondary) !important; }
</style>
"""


def apply_theme():
    """Injects core medical styling."""
    st.markdown(MEDICAL_CSS, unsafe_allow_html=True)


def render_top_bar():
    """Render the shared top brand bar and application language selector."""
    languages = {
        "en": "English",
        "te": "Telugu (తెలుగు)",
        "hi": "Hindi (हिन्दी)",
        "ta": "Tamil (தமிழ்)",
        "kn": "Kannada (ಕನ್ನಡ)",
    }
    current_language = st.session_state.get("preferred_language", "en")
    brand_col, language_col = st.columns([5, 1.35], vertical_alignment="center")
    with brand_col:
        st.markdown(
            """
            <div class="healthaware-top-brand">
                <div class="healthaware-top-mark">🩺</div>
                <div>
                    <div class="healthaware-top-name">HealthAware AI</div>
                    <div class="healthaware-top-caption">Verified health awareness</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with language_col:
        selected_language = st.selectbox(
            "Language",
            options=list(languages.keys()),
            format_func=lambda code: languages[code],
            index=list(languages.keys()).index(current_language) if current_language in languages else 0,
            key="top_language_selector",
        )
        st.session_state["preferred_language"] = selected_language


def render_header(title: str, subtitle: str, icon: str = "🩺"):
    """Renders a professional glassmorphic page hero header."""
    apply_theme()
    language = st.session_state.get("preferred_language", "en")
    title = translate_ui(title, language)
    subtitle = translate_ui(subtitle, language)
    st.markdown(
        f"""
        <div class="page-hero">
            <div class="hero-title">{icon} {title}</div>
            <div class="hero-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_disclaimer():
    """Renders standard educational healthcare disclaimer banner."""
    language = st.session_state.get("preferred_language", "en")
    notice = translate_ui("Educational Notice", language)
    st.markdown(
        f"""
        <div class="disclaimer-banner">
            🛡️ <strong>{notice}:</strong> HealthAware AI provides general health awareness and
            educational information only. It is <strong>not a licensed medical professional</strong> and does
            not provide a clinical diagnosis, prescribe medications, or replace professional healthcare consultation.
            For severe or acute symptoms, seek immediate emergency care.
        </div>
        """,
        unsafe_allow_html=True
    )
