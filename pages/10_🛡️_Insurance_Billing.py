"""
HealthAware AI - Health Insurance & Medical Billing Guide
Educational explanations of health insurance terminology, deductibles, and hospital billing.
Strictly Python + Streamlit. NO JAVASCRIPT.
"""

import streamlit as st
from database.connection import get_db_session
from database.repositories import InsuranceFAQRepository
from components.common import render_header, render_disclaimer, apply_theme
from components.sidebar import render_sidebar

st.set_page_config(page_title="Insurance & Billing - HealthAware AI", page_icon="🛡️", layout="wide")
apply_theme()
render_sidebar()

render_header(
    title="Health Insurance & Billing Guide",
    subtitle="Demystify premiums, deductibles, copays, out-of-pocket limits, and hospital billing statements.",
    icon="🛡️"
)

render_disclaimer()

st.warning(
    "📋 **Insurance Notice:** Coverage and out-of-pocket costs vary significantly depending on your specific policy. "
    "Always verify benefit details and in-network network status directly with your insurer or provider."
)

tab_glossary, tab_bills, tab_calc = st.tabs([
    "📖 Terminology Glossary",
    "🧾 How to Read a Medical Bill",
    "🧮 Deductible & Coinsurance Visualizer"
])

# ==============================================================================
# TAB 1: TERMINOLOGY GLOSSARY
# ==============================================================================
with tab_glossary:
    st.subheader("Essential Insurance Concepts")
    search_term = st.text_input("Search terms (e.g., 'deductible', 'coinsurance', 'eob')...", "")

    with get_db_session() as db:
        faqs = InsuranceFAQRepository.get_all(db, search=search_term if search_term.strip() else None)

    for item in faqs:
        with st.expander(f"📘 {item.term} ({item.category})", expanded=True):
            st.markdown(f"**Definition:** {item.definition}")
            if item.example:
                st.markdown(f"💡 *Example:* {item.example}")

# ==============================================================================
# TAB 2: MEDICAL BILL CHECKLIST
# ==============================================================================
with tab_bills:
    st.subheader("🧾 Step-by-Step Medical Bill Audit Checklist")
    st.markdown(
        """
        Before paying a medical bill or hospital invoice, follow these consumer protection best practices:

        1. **Request an Itemized Bill:**
           Ask the billing department for a comprehensive itemized statement with exact procedure and CPT/HCPCS codes.
        2. **Compare Against Your EOB:**
           Wait for your health plan's *Explanation of Benefits (EOB)*. Verify that the 'Amount You Owe' matches what the provider is billing.
        3. **Check for Duplicate Charges:**
           Look closely for repeated line items for medications, supplies, or lab draws on the same date of service.
        4. **Verify In-Network Status:**
           Confirm that treating physicians, anesthesiologists, and imaging labs at the facility were in-network.
        5. **Inquire About Financial Assistance / Payment Plans:**
           Non-profit hospitals are legally required to provide financial hardship policies. Requesting a prompt-pay cash discount often reduces bills by 20-40%.
        """
    )

# ==============================================================================
# TAB 3: DEDUCTIBLE & COINSURANCE CALCULATOR
# ==============================================================================
with tab_calc:
    st.subheader("🧮 Educational Cost-Sharing Visualizer")
    st.caption("Understand how deductibles, coinsurance, and out-of-pocket maximums interact during a covered medical event.")

    col1, col2 = st.columns(2)
    with col1:
        annual_deductible = st.number_input("Annual Plan Deductible ($)", value=1500, step=250)
        coinsurance_pct = st.slider("Your Coinsurance Percentage (%)", min_value=0, max_value=50, value=20, step=5)
        oop_max = st.number_input("Out-of-Pocket Maximum Cap ($)", value=6000, step=500)

    with col2:
        procedure_cost = st.number_input("Total Medical Bill for Covered Procedure ($)", value=4500, step=500)

        # Calculation logic
        # 1. You pay 100% up to deductible
        you_pay_deductible = min(procedure_cost, annual_deductible)
        remaining_cost = max(0, procedure_cost - you_pay_deductible)

        # 2. Coinsurance on remainder
        you_pay_coinsurance = remaining_cost * (coinsurance_pct / 100.0)

        total_you_pay = min(you_pay_deductible + you_pay_coinsurance, float(oop_max))
        insurance_pays = procedure_cost - total_you_pay

        st.metric("Estimated Your Out-of-Pocket Share", f"${total_you_pay:,.2f}")
        st.metric("Estimated Plan Payment", f"${insurance_pays:,.2f}")

    st.caption("Note: This simulation illustrates standard in-network cost-sharing models. Actual coverage depends on policy provisions.")
