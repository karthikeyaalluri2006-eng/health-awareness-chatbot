"""
HealthAware AI - Administrator Dashboard
Role-protected administration portal for document ingestion,
knowledge base indexing, system health, and audit logs.
Strictly Python + Streamlit. NO JAVASCRIPT.
"""

import streamlit as st
import pandas as pd
from database.connection import get_db_session
from database.repositories import DocumentRepository, AuditLogRepository
from auth.authentication import get_current_user
from auth.authorization import is_admin
from rag.ingestion import ingest_document
from components.common import render_header, render_disclaimer, apply_theme
from components.sidebar import render_sidebar

st.set_page_config(page_title="Admin Portal - HealthAware AI", page_icon="🔒", layout="wide")
apply_theme()
render_sidebar()

render_header(
    title="Healthcare Knowledge Administration",
    subtitle="Ingest verified medical documents, manage vector chunks, and monitor system audit trails.",
    icon="🔒"
)

render_disclaimer()

# Enforce admin check
user = get_current_user()
if not is_admin():
    st.error("⛔ Access Restricted: Administrator credentials required.")
    st.info("💡 You can log in with the default admin account: `admin` / `Admin@123` on the Home Dashboard.")
    st.stop()

tab_ingest, tab_docs, tab_audit = st.tabs([
    "📤 Document Ingestion",
    "📚 Knowledge Base Catalog",
    "📜 System Audit Logs"
])

# ==============================================================================
# TAB 1: MULTI-FORMAT DOCUMENT INGESTION
# ==============================================================================
with tab_ingest:
    st.subheader("Ingest New Healthcare Literature")
    st.caption("Supported file formats: **PDF, DOCX, TXT, JSON, CSV**. Documents are parsed, chunked, and vector-indexed automatically.")

    with st.form("ingest_form"):
        uploaded_file = st.file_uploader("Upload Clinical Guidelines Document", type=["pdf", "docx", "txt", "json", "csv"])
        doc_title = st.text_input("Document Title (Optional)", placeholder="e.g. Hypertension Prevention Guidelines 2026")
        doc_category = st.selectbox("Medical Category", ["Cardiovascular", "Endocrinology", "Immunology", "General Health", "Mental Health", "Nutrition"])
        doc_source = st.text_input("Source Citation / Authority", placeholder="e.g. American Heart Association (AHA) 2026")

        submit_ingest = st.form_submit_button("Ingest & Vector Index Document", type="primary", use_container_width=True)

    if submit_ingest:
        if not uploaded_file:
            st.error("Please upload a valid document file.")
        else:
            with st.spinner(f"Processing and vector-indexing '{uploaded_file.name}'..."):
                file_bytes = uploaded_file.read()
                with get_db_session() as db:
                    success, msg, chunk_count = ingest_document(
                        db=db,
                        filename=uploaded_file.name,
                        file_bytes=file_bytes,
                        title=doc_title,
                        category=doc_category,
                        source_citation=doc_source
                    )
                    if success:
                        AuditLogRepository.log(db, action="DOC_INGEST", user_id=user["id"], details=f"Ingested {uploaded_file.name} ({chunk_count} chunks)")

            if success:
                st.success(f"✅ {msg}")
            else:
                st.error(f"❌ {msg}")

# ==============================================================================
# TAB 2: KNOWLEDGE BASE CATALOG
# ==============================================================================
with tab_docs:
    st.subheader("Currently Indexed Knowledge Base Documents")
    with get_db_session() as db:
        documents = DocumentRepository.get_all_documents(db)

    if not documents:
        st.info("No documents currently indexed.")
    else:
        doc_records = [
            {
                "ID": d.id,
                "Filename": d.filename,
                "Title": d.title,
                "Category": d.category,
                "Format": d.file_type.upper(),
                "Indexed Chunks": d.total_chunks,
                "Added Date": d.created_at.strftime("%b %d, %Y")
            }
            for d in documents
        ]
        df_docs = pd.DataFrame(doc_records)
        st.dataframe(df_docs, use_container_width=True)

        # Deletion control
        st.write("---")
        doc_to_delete = st.selectbox("Select document to remove:", options=[d.id for d in documents], format_func=lambda did: next(d.title for d in documents if d.id == did))
        if st.button("🗑️ Remove Selected Document from Vector Store"):
            with get_db_session() as db:
                DocumentRepository.delete_document(db, doc_to_delete)
            st.toast("Document removed and vector index updated.", icon="🗑️")
            st.rerun()

# ==============================================================================
# TAB 3: SYSTEM AUDIT LOGS
# ==============================================================================
with tab_audit:
    st.subheader("System Security & Operational Audit Trail")
    st.caption("Tracks authentication events, queries, emergency triggers, and document updates.")

    with get_db_session() as db:
        logs = AuditLogRepository.get_recent(db, limit=50)

    if logs:
        audit_data = [
            {
                "Timestamp": l.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "User ID": l.user_id or "Guest",
                "Action": l.action,
                "Status": l.status,
                "Details": l.details or ""
            }
            for l in logs
        ]
        df_audit = pd.DataFrame(audit_data)
        st.dataframe(df_audit, use_container_width=True)
    else:
        st.info("No audit logs recorded yet.")
