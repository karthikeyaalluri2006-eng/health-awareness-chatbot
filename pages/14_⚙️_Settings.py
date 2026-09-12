"""
HealthAware AI - Application Settings
Configure LLM providers, vector database preferences, and accessibility controls.
Strictly Python + Streamlit. NO JAVASCRIPT.
"""

import streamlit as st
import os
from components.common import render_header, render_disclaimer, apply_theme
from components.sidebar import render_sidebar
from services.llm_service import get_llm_provider

st.set_page_config(page_title="Settings - HealthAware AI", page_icon="⚙️", layout="wide")
apply_theme()
render_sidebar()

render_header(
    title="System Configuration & Preferences",
    subtitle="Manage AI inference providers, database engines, and accessibility options.",
    icon="⚙️"
)

render_disclaimer()

tab_llm, tab_db, tab_access = st.tabs([
    "🤖 LLM Provider",
    "🗄️ Database & Vector Store",
    "👁️ Accessibility"
])

# ==============================================================================
# TAB 1: LLM PROVIDER CONFIGURATION
# ==============================================================================
with tab_llm:
    st.subheader("Active Inference Provider")

    active_provider = os.getenv("LLM_PROVIDER", "offline")
    st.info(f"Currently active engine: **{active_provider.upper()}**")

    st.markdown(
        """
        - **Offline Engine (Default):** Runs 100% locally with zero external API calls or latency. Synthesizes answers directly from the verified medical RAG knowledge base.
        - **OpenAI:** Requires `LLM_API_KEY` set in your `.env` file.
        - **Ollama:** Connects to local Ollama instance running at `http://localhost:11434`.
        """
    )

    if st.button("🧪 Test LLM Engine Health"):
        try:
            llm = get_llm_provider()
            sample_resp = llm.generate_response("What are 2 healthy lifestyle habits?")
            st.success("✅ Provider operational and responding correctly.")
            st.markdown(f"**Sample Output:**\n\n{sample_resp[:300]}...")
        except Exception as e:
            st.error(f"Provider healthcheck encountered an issue: {e}")

# ==============================================================================
# TAB 2: DATABASE & VECTOR STORE
# ==============================================================================
with tab_db:
    st.subheader("Vector Database & Knowledge Storage")

    db_url = os.getenv("DATABASE_URL", "sqlite:///./data/healthaware.db")
    is_sqlite = "sqlite" in db_url

    st.markdown(f"**Database Mode:** `{'Local SQLite (Out-of-the-box)' if is_sqlite else 'PostgreSQL + pgvector'}`")
    st.caption(f"Connection URI: `{db_url}`")

    if is_sqlite:
        st.success("✅ Running in Zero-Dependency Local Mode: In-memory vector similarity active via NumPy cosine projection.")
    else:
        st.info("Connected to external PostgreSQL / pgvector instance.")

# ==============================================================================
# TAB 3: ACCESSIBILITY
# ==============================================================================
with tab_access:
    st.subheader("Visual Accessibility Preferences")

    high_contrast = st.toggle("Enable High-Contrast Border Mode", value=False)
    if high_contrast:
        st.markdown(
            """
            <style>
            .health-card { border: 2px solid #000000 !important; }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.toast("High-contrast mode enabled.")

    st.caption("Streamlit widgets automatically support browser native zoom (Ctrl +/-) and screen readers.")
