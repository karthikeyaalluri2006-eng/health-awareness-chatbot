"""
HealthAware AI - Myth vs Fact Repository
Searchable database debunking health misinformation with clinical evidence and citations.
Strictly Python + Streamlit. NO JAVASCRIPT.
"""

import streamlit as st
from database.connection import get_db_session
from database.repositories import MythFactRepository
from components.common import render_header, render_disclaimer, apply_theme
from components.sidebar import render_sidebar

st.set_page_config(page_title="Myth vs Fact - HealthAware AI", page_icon="🔍", layout="wide")
apply_theme()
render_sidebar()

render_header(
    title="Medical Myth vs. Fact",
    subtitle="Separate science-backed medical reality from viral misinformation and common misconceptions.",
    icon="🔍"
)

render_disclaimer()

with get_db_session() as db:
    categories = ["All"] + MythFactRepository.get_categories(db)

col1, col2, col3 = st.columns([1.5, 1, 1])
with col1:
    search_term = st.text_input("🔎 Search by keyword (e.g. 'sugar', 'blood pressure', 'flu')", "")
with col2:
    selected_cat = st.selectbox("Filter by Category", options=categories, index=0)
with col3:
    st.write("")
    st.write("")
    random_btn = st.button("🎲 Show Random Myth", use_container_width=True)

with get_db_session() as db:
    if random_btn:
        r_myth = MythFactRepository.get_random(db)
        myths = [r_myth] if r_myth else []
    else:
        myths = MythFactRepository.get_all(db, category=selected_cat, search=search_term)

st.write(f"Showing **{len(myths)}** verified evidence items:")

for item in myths:
    st.markdown(
        f"""
        <div class="health-card">
            <span class="badge-teal">{item.category}</span>
            <div class="myth-card" style="margin-top: 12px;">
                <div style="font-size: 0.75rem; font-weight: 700; color: #f87171;
                            text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px;">❌ Myth</div>
                <div style="color: #fca5a5; font-size: 0.98rem; font-weight: 600; line-height: 1.5;">"{item.myth}"</div>
            </div>
            <div class="fact-card">
                <div style="font-size: 0.75rem; font-weight: 700; color: #34d399;
                            text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px;">✅ Fact</div>
                <div style="color: #a7f3d0; font-size: 0.98rem; font-weight: 600; line-height: 1.5; margin-bottom: 8px;">{item.fact}</div>
                <div style="color: #94a3b8; font-size: 0.875rem; line-height: 1.6;">{item.explanation}</div>
            </div>
            <div style="font-size: 0.78rem; color: #64748b; border-top: 1px solid rgba(255,255,255,0.06);
                        padding-top: 8px; margin-top: 4px;">
                📖 <strong>Evidence Source:</strong> {item.source}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
