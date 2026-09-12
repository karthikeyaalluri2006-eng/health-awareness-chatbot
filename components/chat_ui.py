"""
HealthAware AI - Chat UI Components
Renders suggested prompt chips, message bubbles, and feedback buttons.
"""

import streamlit as st
from typing import List, Callable, Optional


def render_suggested_questions(on_select: Callable[[str], None], custom_questions: Optional[List[str]] = None):
    """Renders interactive quick-select prompt buttons for common health inquiries."""
    defaults = [
        "What are the common symptoms of Type 2 Diabetes?",
        "How can I prevent high blood pressure naturally?",
        "What is the difference between flu and a common cold?",
        "Which adult vaccines are generally recommended?",
        "What does high LDL cholesterol mean for heart health?"
    ]
    questions = custom_questions or defaults

    st.markdown("<p style='font-size: 0.88rem; color: #64748b; margin-bottom: 6px;'>💡 <strong>Suggested Health Topics:</strong></p>", unsafe_allow_html=True)
    cols = st.columns(len(questions))
    for i, q in enumerate(questions):
        with cols[i]:
            if st.button(q, key=f"suggested_q_{i}", use_container_width=True):
                on_select(q)


def render_message_feedback(message_id: int):
    """Renders thumbs-up and thumbs-down feedback buttons for AI answers."""
    c1, c2, c3 = st.columns([1, 1, 10])
    with c1:
        if st.button("👍", key=f"thumb_up_{message_id}", help="This answer was helpful and clear"):
            st.toast("Thank you for your feedback!", icon="💚")
    with c2:
        if st.button("👎", key=f"thumb_down_{message_id}", help="This answer was unhelpful"):
            st.toast("Feedback recorded. We'll improve our healthcare guidance.", icon="📝")
