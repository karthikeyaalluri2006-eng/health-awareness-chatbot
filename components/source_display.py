"""
HealthAware AI - RAG Sources Display Component
Renders verified knowledge citations retrieved during RAG generation.
Strict rule: Never fabricates sources; only shows retrieved documents.
"""

import streamlit as st
from typing import List, Dict, Any


def render_sources(sources: List[Dict[str, Any]]):
    """Displays collapsible citation card showing verified medical references used."""
    if not sources:
        return

    with st.expander(f"📚 Verified Sources & References ({len(sources)})", expanded=False):
        for i, s in enumerate(sources, 1):
            st.markdown(
                f"""
                <div class="source-card">
                    <div class="source-title">{i}. {s.get('title', 'Clinical Reference')}</div>
                    <div class="source-meta">
                        📖 {s.get('source', 'Healthcare Knowledge Store')} &nbsp;•&nbsp;
                        🏷️ {s.get('category', 'General Health')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
