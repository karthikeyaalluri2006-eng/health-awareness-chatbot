"""
HealthAware AI - Interactive Health Quizzes
Evidence-based multiple-choice quizzes to reinforce healthcare literacy.
Strictly Python + Streamlit. NO JAVASCRIPT.
"""

import streamlit as st
import json
from database.connection import get_db_session
from database.repositories import QuizRepository
from auth.authentication import get_current_user
from components.common import render_header, render_disclaimer, apply_theme
from components.sidebar import render_sidebar
from components.quiz_ui import render_quiz_scorecard
from services.localization_service import translate_ui

st.set_page_config(page_title="Interactive Quizzes - HealthAware AI", page_icon="📝", layout="wide")
apply_theme()
render_sidebar()

render_header(
    title="Interactive Healthcare Quizzes",
    subtitle="Test and sharpen your awareness on cardiovascular health, diabetes, preventive immunization, and first aid.",
    icon="📝"
)

render_disclaimer()
language = st.session_state.get("preferred_language", "en")

user = get_current_user()
user_id = user["id"] if user else 1

with get_db_session() as db:
    topics = ["All"] + QuizRepository.get_topics(db)

col1, col2 = st.columns([1, 2])
with col1:
    selected_topic = st.selectbox(f"🎯 {translate_ui('Choose Quiz Topic:', language)}", options=topics, index=0)

# Initialize quiz state
if "quiz_questions" not in st.session_state or st.session_state.get("quiz_topic") != selected_topic:
    with get_db_session() as db:
        raw_questions = QuizRepository.get_questions_by_topic(db, selected_topic, limit=5)
        st.session_state["quiz_questions"] = [
            {
                "id": q.id,
                "topic": q.topic,
                "question": q.question,
                "options": json.loads(q.options_json),
                "correct": q.correct_answer,
                "explanation": q.explanation
            }
            for q in raw_questions
        ]
        st.session_state["quiz_topic"] = selected_topic
        st.session_state["quiz_user_answers"] = {}
        st.session_state["quiz_submitted"] = False

questions = st.session_state["quiz_questions"]

if not questions:
    st.info(translate_ui("No questions available for this topic yet.", language))
    st.stop()

# Reset Quiz Button
if st.button(f"🔄 {translate_ui('Restart / Load New Questions', language)}"):
    del st.session_state["quiz_questions"]
    st.rerun()

st.write("")

# Form for Quiz
with st.form("quiz_form"):
    st.markdown(f"**{translate_ui('Topic:', language)}** `{selected_topic}` • **{translate_ui('Questions:', language)}** `{len(questions)}`")
    user_selections = {}

    for i, q in enumerate(questions, 1):
        st.markdown(f"#### {translate_ui('Question', language)} {i}: {q['question']}")
        opts = q["options"]
        selected_opt = st.radio(
            f"{translate_ui('Select your answer for question', language)} {i}:",
            options=opts,
            key=f"q_radio_{q['id']}",
            index=None
        )
        user_selections[q["id"]] = selected_opt
        st.divider()

    submitted = st.form_submit_button(translate_ui("Submit Quiz Answers", language), type="primary", use_container_width=True)

if submitted:
    st.session_state["quiz_submitted"] = True
    st.session_state["quiz_user_answers"] = user_selections

if st.session_state.get("quiz_submitted"):
    user_answers = st.session_state.get("quiz_user_answers", {})
    score = 0

    st.subheader(f"📋 {translate_ui('Quiz Results & Explanations', language)}")

    for i, q in enumerate(questions, 1):
        ans = user_answers.get(q["id"])
        is_correct = (ans == q["correct"])
        if is_correct:
            score += 1
            st.success(f"**{translate_ui('Question', language)} {i}: {translate_ui('Correct!', language)}** ✅ (Your answer: {ans})")
        else:
            st.error(f"**{translate_ui('Question', language)} {i}: {translate_ui('Incorrect', language)}** ❌ (Your answer: {ans or translate_ui('Unanswered', language)} • {translate_ui('Correct:', language)} **{q['correct']}**)")

        st.info(f"💡 **{translate_ui('Explanation:', language)}** {q['explanation']}")
        st.write("")

    render_quiz_scorecard(score=score, total=len(questions), topic=selected_topic)

    # Save to database
    with get_db_session() as db:
        QuizRepository.save_attempt(
            db=db,
            user_id=user_id,
            topic=selected_topic,
            score=score,
            total_questions=len(questions),
            answers=user_answers
        )
