"""
HealthAware AI - Health Learning Modules
Bite-sized, interactive healthcare awareness curriculum covering Diabetes,
Cardiovascular Wellness, Immunization, and Seasonal Respiratory Illness.
Strictly Python + Streamlit. NO JAVASCRIPT.
"""

import streamlit as st
import json
from database.connection import get_db_session
from database.repositories import HealthModuleRepository
from auth.authentication import get_current_user
from components.common import render_header, render_disclaimer, apply_theme
from components.sidebar import render_sidebar
from services.localization_service import translate_ui

st.set_page_config(page_title="Health Learning - HealthAware AI", page_icon="📚", layout="wide")
apply_theme()
render_sidebar()

render_header(
    title="Health Learning Curriculum",
    subtitle="Evidence-grounded, bite-sized lessons to enhance your healthcare literacy and preventive habits.",
    icon="📚"
)

render_disclaimer()

user = get_current_user()
user_id = user["id"] if user else 1
language = st.session_state.get("preferred_language", "en")

with get_db_session() as db:
    modules = HealthModuleRepository.get_all(db)

if not modules:
    st.info(translate_ui("No learning modules found. Please initialize the database.", language))
    st.stop()

# Tab navigation across modules
tab_titles = [f"{m.icon} {translate_ui(m.title.split('&')[0].strip(), language)}" for m in modules]
tabs = st.tabs(tab_titles)

for idx, module in enumerate(modules):
    with tabs[idx]:
        st.markdown(f"### {module.icon} {translate_ui(module.title, language)}")
        st.caption(
            f"{translate_ui('Category', language)}: **{translate_ui(module.category, language)}** • "
            f"{translate_ui('Estimated reading time', language)}: **{module.estimated_mins} minutes**"
        )

        # Parse content
        try:
            content = json.loads(module.content_json)
        except Exception:
            content = {"lessons": [], "key_takeaways": []}

        # Check user completion status
        with get_db_session() as db:
            progress = HealthModuleRepository.get_user_progress(db, user_id, module.id)
            is_completed = progress.completed if progress else False

        if is_completed:
            st.success(f"🎉 {translate_ui('You have completed this educational module!', language)}")

        # Render lessons in expandable accordions
        st.subheader(f"📖 {translate_ui('Lessons', language)}")
        for i, lesson in enumerate(content.get("lessons", []), 1):
            with st.expander(f"{translate_ui('Lesson', language)} {i}: {lesson.get('title')}", expanded=(i == 1)):
                st.markdown(lesson.get("text"))

        # Render key takeaways
        st.subheader(f"💡 {translate_ui('Key Takeaways', language)}")
        for pt in content.get("key_takeaways", []):
            st.markdown(f"• **{pt}**")

        st.write("")
        col1, col2 = st.columns([1, 2])
        with col1:
            if not is_completed:
                if st.button(f"{translate_ui('Mark', language)} '{module.title[:20]}...' {translate_ui('Completed', language)}", key=f"complete_mod_{module.id}", type="primary"):
                    with get_db_session() as db:
                        HealthModuleRepository.update_progress(db, user_id, module.id, step=4, completed=True)
                    st.toast("Module completed!", icon="🌟")
                    st.rerun()
            else:
                st.button(f"{translate_ui('Completed', language)} ✅", key=f"done_btn_{module.id}", disabled=True)

        with col2:
            st.info(translate_ui("Healthcare education does not substitute for personalized medical check-ups with your physician.", language))
