"""
HealthAware AI - Premium Sidebar Component
Consistent navigation, auth status, language selector, and emergency quick-access.
"""

import streamlit as st
from auth.authentication import get_current_user, logout_user
from safety.emergency_detection import VERIFIED_EMERGENCY_HOTLINES
from services.localization_service import translate_ui


NAVIGATION = [
    ("app.py", "🏠", {"en": "Home", "te": "హోమ్", "hi": "होम", "ta": "முகப்பு", "kn": "ಮುಖಪುಟ"}),
    ("pages/1_💬_AI_Health_Chat.py", "💬", {"en": "AI Health Chat", "te": "AI ఆరోగ్య చాట్", "hi": "AI स्वास्थ्य चैट", "ta": "AI சுகாதார உரையாடல்", "kn": "AI ಆರೋಗ್ಯ ಚಾಟ್"}),
    ("pages/2_📚_Health_Learning.py", "📚", {"en": "Health Learning", "te": "ఆరోగ్య అభ్యాసం", "hi": "स्वास्थ्य शिक्षा", "ta": "சுகாதாரக் கற்றல்", "kn": "ಆರೋಗ್ಯ ಕಲಿಕೆ"}),
    ("pages/3_📝_Interactive_Quizzes.py", "📝", {"en": "Interactive Quizzes", "te": "ఇంటరాక్టివ్ క్విజ్‌లు", "hi": "इंटरैक्टिव क्विज़", "ta": "வினாடி வினாக்கள்", "kn": "ಸಂವಾದಾತ್ಮಕ ಕ್ವಿಜ್‌ಗಳು"}),
    ("pages/4_⚖️_Risk_Assessment.py", "⚖️", {"en": "Risk Assessment", "te": "ప్రమాద అంచనా", "hi": "जोखिम आकलन", "ta": "ஆபத்து மதிப்பீடு", "kn": "ಅಪಾಯ ಮೌಲ್ಯಮಾಪನ"}),
    ("pages/5_🔍_Myth_vs_Fact.py", "🔍", {"en": "Myth vs Fact", "te": "అపోహ vs వాస్తవం", "hi": "मिथक बनाम तथ्य", "ta": "கட்டுக்கதை vs உண்மை", "kn": "ಮಿಥ್ಯೆ vs ಸತ್ಯ"}),
    ("pages/6_🩺_Symptom_Checker.py", "🩺", {"en": "Symptom Checker", "te": "లక్షణాల తనిఖీ", "hi": "लक्षण जांच", "ta": "அறிகுறி சரிபார்ப்பு", "kn": "ಲಕ್ಷಣ ಪರಿಶೀಲನೆ"}),
    ("pages/7_💊_Medications.py", "💊", {"en": "Medications", "te": "మందులు", "hi": "दवाएं", "ta": "மருந்துகள்", "kn": "ಔಷಧಗಳು"}),
    ("pages/8_📅_Appointments.py", "📅", {"en": "Appointments", "te": "అపాయింట్‌మెంట్లు", "hi": "अपॉइंटमेंट", "ta": "சந்திப்புகள்", "kn": "ಅಪಾಯಿಂಟ್‌ಮೆಂಟ್‌ಗಳು"}),
    ("pages/9_🏥_Healthcare_Directory.py", "🏥", {"en": "Healthcare Directory", "te": "ఆరోగ్య డైరెక్టరీ", "hi": "स्वास्थ्य निर्देशिका", "ta": "சுகாதார அடைவு", "kn": "ಆರೋಗ್ಯ ಡೈರೆಕ್ಟರಿ"}),
    ("pages/10_🛡️_Insurance_Billing.py", "🛡️", {"en": "Insurance & Billing", "te": "బీమా & బిల్లింగ్", "hi": "बीमा और बिलिंग", "ta": "காப்பீடு மற்றும் பில்லிங்", "kn": "ವಿಮೆ ಮತ್ತು ಬಿಲ್ಲಿಂಗ್"}),
    ("pages/11_🧘_Mental_Wellness.py", "🧘", {"en": "Mental Wellness", "te": "మానసిక ఆరోగ్యం", "hi": "मानसिक स्वास्थ्य", "ta": "மனநலம்", "kn": "ಮಾನಸಿಕ ಸ್ವಾಸ್ಥ್ಯ"}),
    ("pages/12_⌚_Wearable_Health.py", "⌚", {"en": "Wearable Health", "te": "వేర్‌బుల్ ఆరోగ్యం", "hi": "वियरेबल स्वास्थ्य", "ta": "அணியக்கூடிய சுகாதாரம்", "kn": "ಧರಿಸಬಹುದಾದ ಆರೋಗ್ಯ"}),
    ("pages/13_👤_Profile.py", "👤", {"en": "Profile", "te": "ప్రొఫైల్", "hi": "प्रोफ़ाइल", "ta": "சுயவிவரம்", "kn": "ಪ್ರೊಫೈಲ್"}),
    ("pages/14_⚙️_Settings.py", "⚙️", {"en": "Settings", "te": "సెట్టింగ్‌లు", "hi": "सेटिंग्स", "ta": "அமைப்புகள்", "kn": "ಸೆಟ್ಟಿಂಗ್‌ಗಳು"}),
]


def render_sidebar():
    """Renders the premium application sidebar with navigation and user info."""
    with st.sidebar:
        # Logo & Brand
        st.markdown(
            """
            <div style="text-align: center; padding: 20px 0 18px; border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 18px;">
                <div style="font-size: 2.2rem; margin-bottom: 4px;">🩺</div>
                <div style="font-size: 1.15rem; font-weight: 800; background: linear-gradient(135deg, #0ea5e9, #14b8a6);
                            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                            background-clip: text;">HealthAware AI</div>
                <div style="font-size: 0.75rem; color: #64748b; margin-top: 3px;">Healthcare Awareness & Wellness</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        languages = {
            "en": "English",
            "te": "Telugu (తెలుగు)",
            "hi": "Hindi (हिन्दी)",
            "ta": "Tamil (தமிழ்)",
            "kn": "Kannada (ಕನ್ನಡ)",
        }
        current_language = st.session_state.get("preferred_language", "en")
        st.selectbox(
            "Language",
            options=list(languages.keys()),
            format_func=lambda code: languages[code],
            index=list(languages.keys()).index(current_language) if current_language in languages else 0,
            key="sidebar_language_selector",
        )
        st.session_state["preferred_language"] = st.session_state["sidebar_language_selector"]

        user = get_current_user()

        selected_language = st.session_state["preferred_language"]
        st.markdown(
            f"<div style='font-size: 0.72rem; font-weight: 700; color: #64748b; "
            f"text-transform: uppercase; letter-spacing: 0.08em; margin: 18px 0 8px;'>{translate_ui('App', selected_language)}</div>",
            unsafe_allow_html=True
        )
        if user:
            for page_path, icon, labels in NAVIGATION:
                st.page_link(
                    page_path,
                    label=labels.get(st.session_state["preferred_language"], labels["en"]),
                    icon=icon,
                    use_container_width=True,
                )

        if user:
            role_icon = "🛡️" if user.get("role") == "admin" else "👤"
            role_label = "Administrator" if user.get("role") == "admin" else "Patient"
            display_name = user.get("full_name") or user.get("username", "User")
            st.markdown(
                f"""
                <div class="sidebar-user-card">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <div style="width: 38px; height: 38px; border-radius: 50%;
                                    background: linear-gradient(135deg, #0ea5e9, #14b8a6);
                                    display: flex; align-items: center; justify-content: center;
                                    font-size: 1rem; font-weight: 700; color: white; flex-shrink: 0;">
                            {display_name[0].upper()}
                        </div>
                        <div>
                            <div style="font-weight: 600; color: #f1f5f9; font-size: 0.9rem;">{display_name}</div>
                            <div style="font-size: 0.75rem; color: #5eead4;">{role_icon} {role_label}</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button("🚪 Sign Out", key="sidebar_logout_btn", use_container_width=True):
                logout_user()
                st.rerun()
        else:
            st.markdown(
                """
                <div style="background: rgba(14,165,233,0.06); border: 1px solid rgba(14,165,233,0.15);
                            border-radius: 10px; padding: 12px 14px; margin-bottom: 14px;
                            font-size: 0.82rem; color: #7dd3fc; line-height: 1.5;">
                    💡 <strong>Guest Mode</strong> — Sign in on the Home page to save chat history,
                    track medications, and personalize your experience.
                </div>
                """,
                unsafe_allow_html=True
            )
            auth_col1, auth_col2 = st.columns(2)
            with auth_col1:
                if st.button("🔑 Sign In", key="sidebar_sign_in", use_container_width=True):
                    st.session_state["auth_tab"] = "signin"
                    st.switch_page("app.py")
            with auth_col2:
                if st.button("📝 Create Account", key="sidebar_create_account", use_container_width=True):
                    st.session_state["auth_tab"] = "create"
                    st.switch_page("app.py")

        st.divider()

        # Emergency Hotlines
        with st.expander("🚨 Emergency Hotlines", expanded=False):
            st.markdown(
                "<div style='background: rgba(244,63,94,0.10); border: 1px solid rgba(244,63,94,0.25); "
                "border-radius: 8px; padding: 10px 12px; margin-bottom: 8px; font-size: 0.82rem; "
                "color: #fda4af; font-weight: 600;'>⚡ Dial immediately in life-threatening emergencies</div>",
                unsafe_allow_html=True
            )
            for h in VERIFIED_EMERGENCY_HOTLINES[:4]:
                st.markdown(
                    f"<div style='padding: 4px 0; font-size: 0.82rem;'>"
                    f"<span style='color: #94a3b8;'>{h['region']}:</span> "
                    f"<span style='color: #f1f5f9; font-weight: 700; font-family: monospace;'>{h['number']}</span></div>",
                    unsafe_allow_html=True
                )
            st.caption("Available 24/7 • Free from any telephone")

        # Footer
        st.markdown(
            """
            <div style="margin-top: 24px; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.06);
                        text-align: center; font-size: 0.72rem; color: #475569; line-height: 1.5;">
                <div style="margin-bottom: 4px;">🔒 HIPAA-Aware Design</div>
                <div>v2.0 — Final Year Project</div>
                <div style="margin-top: 4px; color: #334155;">Not a substitute for medical advice</div>
            </div>
            """,
            unsafe_allow_html=True
        )
