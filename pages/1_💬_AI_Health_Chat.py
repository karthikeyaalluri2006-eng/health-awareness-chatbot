"""
HealthAware AI - AI Health Chat Module
Fully integrated conversational AI with RAG, emergency detection, voice input, and citations.
"""

import streamlit as st
import json
from database.connection import get_db_session
from database.repositories import ChatRepository
from auth.authentication import get_current_user
from services.rag_service import RAGService, casual_greeting_response, is_casual_greeting
from services.speech_service import get_speech_provider
from components.common import render_header, render_disclaimer, apply_theme
from components.sidebar import render_sidebar
from components.emergency_alert import render_emergency_banner, render_crisis_banner
from components.source_display import render_sources
from services.localization_service import translate_ui

# ──────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG & THEME
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Health Chat – HealthAware AI",
    page_icon="💬",
    layout="wide"
)
apply_theme()
render_sidebar()

render_header(
    title="AI Healthcare Chat",
    subtitle="Ask evidence-grounded questions about symptoms, preventive wellness, and medical awareness. "
             "Powered by RAG with verified healthcare knowledge.",
    icon="💬"
)
render_disclaimer()

# ──────────────────────────────────────────────────────────────────────────────
# USER & SESSION SETUP
# ──────────────────────────────────────────────────────────────────────────────
user = get_current_user()
user_id = user["id"] if user else 1   # Guest fallback → demo user id=1
language = st.session_state.get("preferred_language", "en")

# ──────────────────────────────────────────────────────────────────────────────
# CONVERSATION MANAGEMENT (sidebar)
# ──────────────────────────────────────────────────────────────────────────────
with get_db_session() as db:
    conversations = ChatRepository.get_user_conversations(db, user_id)

    st.sidebar.markdown(
        "<hr style='border-color: rgba(255,255,255,0.07); margin: 8px 0 12px;'>",
        unsafe_allow_html=True
    )
    st.sidebar.markdown(
        f"<div style='font-size:0.72rem; font-weight:700; color:#64748b; "
        f"text-transform:uppercase; letter-spacing:0.08em; margin-bottom:8px;'>{translate_ui('Consultations', language)}</div>",
        unsafe_allow_html=True
    )

    if st.sidebar.button(f"➕ {translate_ui('New Consultation', language)}", use_container_width=True, key="btn_new_conv"):
        with get_db_session() as db2:
            new_conv = ChatRepository.create_conversation(db2, user_id=user_id, language=language)
            st.session_state["conversation_id"] = new_conv.id
        st.rerun()

    if conversations:
        conversation_messages = {
            conversation.id: ChatRepository.get_messages(db, conversation.id)
            for conversation in conversations
        }
        conv_options = {}
        for conversation in conversations:
            messages_for_conversation = conversation_messages[conversation.id]
            first_user_message = next(
                (message.content for message in messages_for_conversation if message.role == "user"),
                "New health consultation"
            )
            preview = " ".join(first_user_message.split())[:42]
            if len(first_user_message) > 42:
                preview += "..."
            conv_options[conversation.id] = (
                f"{preview} ({conversation.created_at.strftime('%b %d')})"
            )

        current_conv_id = st.session_state.get("conversation_id")
        if current_conv_id not in conv_options:
            current_conv_id = next(
                (
                    conversation.id
                    for conversation in conversations
                    if conversation_messages[conversation.id]
                ),
                conversations[0].id
            )
            st.session_state["conversation_id"] = current_conv_id

        st.session_state["chat_select_history"] = current_conv_id
        selected_conv_id = st.sidebar.selectbox(
            translate_ui("Select Consultation", language),
            options=list(conv_options.keys()),
            format_func=lambda x: conv_options.get(x, "Consultation"),
            index=list(conv_options.keys()).index(current_conv_id),
            key="chat_select_history",
            label_visibility="collapsed"
        )
        st.session_state["conversation_id"] = selected_conv_id
    else:
        with get_db_session() as db2:
            new_conv = ChatRepository.create_conversation(db2, user_id=user_id, language=language)
            st.session_state["conversation_id"] = new_conv.id

active_conv_id = st.session_state.get("conversation_id")

# ──────────────────────────────────────────────────────────────────────────────
# SUGGESTED PROMPT CHIPS
# ──────────────────────────────────────────────────────────────────────────────
SUGGESTED_PROMPTS = [
    "🩸 Symptoms of Type 2 Diabetes?",
    "💓 How to lower high blood pressure naturally?",
    "🤧 Flu vs Common Cold — what's the difference?",
    "💉 Which vaccines do adults need?",
    "🧠 Signs of high cholesterol and risks?",
]

st.markdown(
    "<p style='font-size: 0.82rem; color: #64748b; margin-bottom: 8px;'>"
    f"💡 <strong style='color:#94a3b8;'>{translate_ui('Quick Topics — click to ask:', language)}</strong></p>",
    unsafe_allow_html=True
)
chip_cols = st.columns(len(SUGGESTED_PROMPTS))
for i, prompt in enumerate(SUGGESTED_PROMPTS):
    with chip_cols[i]:
        if st.button(prompt, key=f"chip_{i}", use_container_width=True):
            st.session_state["pending_query"] = prompt.split(" ", 1)[1] if " " in prompt else prompt
            st.rerun()

st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# VOICE INPUT EXPANDER
# ──────────────────────────────────────────────────────────────────────────────
with st.expander(f"🎙️ {translate_ui('Voice / Audio Input', language)}", expanded=False):
    st.caption("Upload a short voice note (WAV, MP3, M4A) to ask your health question.")
    audio_file = st.file_uploader(
        "Upload Audio File", type=["wav", "mp3", "m4a"], key="voice_uploader",
        label_visibility="collapsed"
    )
    if audio_file is not None:
        speech_provider = get_speech_provider()
        success, transcribed_text = speech_provider.transcribe(audio_file.read(), audio_file.name)
        if success:
            st.success(f"**Transcribed:** *\"{transcribed_text}\"*")
            if st.button("✅ Use This Transcribed Question", key="btn_use_audio"):
                st.session_state["pending_query"] = transcribed_text
                st.rerun()
        else:
            st.error(transcribed_text)

st.divider()

# ──────────────────────────────────────────────────────────────────────────────
# RENDER CHAT HISTORY
# ──────────────────────────────────────────────────────────────────────────────
if active_conv_id:
    with get_db_session() as db:
        messages = ChatRepository.get_messages(db, active_conv_id)

    if not messages:
        # Empty state
        st.markdown(
            """
            <div style="text-align: center; padding: 60px 20px; color: #475569;">
                <div style="font-size: 3.5rem; margin-bottom: 14px;">💬</div>
                <div style="font-size: 1.2rem; font-weight: 600; color: #64748b; margin-bottom: 8px;">
                    Start a Health Conversation
                </div>
                <div style="font-size: 0.9rem; max-width: 440px; margin: 0 auto; line-height: 1.6;">
                    Say hello or ask about symptoms, preventive care, medications, nutrition, or any health topic.
                    Get clear, evidence-based health awareness guidance in a friendly conversation.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        for message_index, msg in enumerate(messages):
            with st.chat_message(msg.role):
                displayed_content = msg.content
                has_legacy_greeting = (
                    msg.role == "assistant"
                    and message_index > 0
                    and messages[message_index - 1].role == "user"
                    and is_casual_greeting(messages[message_index - 1].content)
                    and "Health Awareness:" in msg.content
                )
                if has_legacy_greeting:
                    displayed_content = casual_greeting_response()
                st.markdown(displayed_content)
                if msg.role == "assistant" and msg.sources_json:
                    try:
                        sources = json.loads(msg.sources_json)
                        if sources:
                            render_sources(sources)
                    except Exception:
                        pass
                    # Feedback buttons
                    fb_col1, fb_col2, fb_col3 = st.columns([1, 1, 10])
                    with fb_col1:
                        if st.button("👍", key=f"up_{msg.id}", help="Helpful answer"):
                            st.toast("Thanks for the positive feedback! 💚", icon="💚")
                    with fb_col2:
                        if st.button("👎", key=f"dn_{msg.id}", help="Not helpful"):
                            st.toast("Feedback recorded. We'll improve! 📝", icon="📝")

# ──────────────────────────────────────────────────────────────────────────────
# PROCESS NEW QUERY
# ──────────────────────────────────────────────────────────────────────────────
user_input = st.chat_input(
    f"{translate_ui('Say hello or ask a health question', language)} ..."
)

# Determine which query to process
query_to_process = None
if user_input and user_input.strip():
    query_to_process = user_input.strip()
elif st.session_state.get("pending_query"):
    query_to_process = st.session_state.pop("pending_query").strip()

if query_to_process:
    # Show user message immediately
    with st.chat_message("user"):
        st.markdown(query_to_process)

    # Generate AI response with spinner
    with st.chat_message("assistant"):
        thinking_placeholder = st.empty()
        thinking_placeholder.markdown(
            "<span style='color:#64748b; font-size:0.88rem;'>"
            "<span class='typing-dot'></span>"
            "<span class='typing-dot'></span>"
            "<span class='typing-dot'></span>"
            " &nbsp;Preparing your response...</span>",
            unsafe_allow_html=True
        )

        try:
            with get_db_session() as db:
                rag_result = RAGService.process_query(
                    db=db,
                    query=query_to_process,
                    user_id=user_id,
                    conversation_id=active_conv_id,
                    language=language
                )
        except Exception as e:
            rag_result = {
                "success": False,
                "is_emergency": False,
                "is_crisis": False,
                "response": (
                    "I encountered a temporary issue while processing your request. "
                    "Please try again — or if you have an urgent health concern, "
                    "contact a licensed healthcare professional immediately."
                ),
                "sources": []
            }

        thinking_placeholder.empty()

        # Handle response type
        if rag_result.get("is_emergency"):
            render_emergency_banner(rag_result["emergency_details"])

        elif rag_result.get("is_crisis"):
            render_crisis_banner(
                rag_result["response"],
                rag_result["crisis_details"].resources
            )

        else:
            st.markdown(rag_result.get("response", "No response generated."))
            sources = rag_result.get("sources", [])
            if sources:
                render_sources(sources)

    # Update conversation_id if a new one was created
    if rag_result.get("conversation_id"):
        st.session_state["conversation_id"] = rag_result["conversation_id"]

    st.rerun()

# ──────────────────────────────────────────────────────────────────────────────
# BOTTOM INFO STRIP
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="margin-top: 24px; padding: 14px 20px;
                background: rgba(14,165,233,0.05); border: 1px solid rgba(14,165,233,0.12);
                border-radius: 12px; font-size: 0.82rem; color: #64748b; text-align: center;">
        🔒 All responses are education-only &nbsp;|&nbsp;
        💡 Powered by RAG with offline knowledge engine &nbsp;|&nbsp;
        🚨 Emergency? Call <strong style='color:#fda4af;'>112 (India)</strong> or your local emergency number
    </div>
    """,
    unsafe_allow_html=True
)
