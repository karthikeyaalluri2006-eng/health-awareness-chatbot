"""
HealthAware AI - Quiz UI Component
Renders interactive educational quiz question cards and result scorecards.
"""

import streamlit as st
from typing import Dict, Any


def render_quiz_scorecard(score: int, total: int, topic: str):
    """Renders final quiz completion scorecard."""
    pct = round((score / total) * 100) if total > 0 else 0
    color = "#10b981" if pct >= 80 else "#3b82f6" if pct >= 60 else "#f59e0b"

    st.markdown(
        f"""
        <div class="health-card" style="text-align: center; border-top: 4px solid {color};">
            <h2 style="color: #0f172a; margin-bottom: 4px;">Quiz Completed: {topic}</h2>
            <p style="color: #64748b; font-size: 0.95rem;">Educational Quiz Assessment</p>
            <div style="font-size: 3rem; font-weight: 700; color: {color}; margin: 12px 0;">
                {score} / {total}
            </div>
            <p style="font-size: 1.1rem; font-weight: 600; color: #334155;">
                Score: {pct}%
            </p>
            <p style="font-size: 0.88rem; color: #64748b;">
                {'🌟 Outstanding! You have great healthcare awareness.' if pct >= 80 else '👍 Good effort! Review the topics to deepen your understanding.'}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
