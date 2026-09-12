"""
HealthAware AI - Healthcare Services Directory
Search verified local hospitals, walk-in clinics, 24/7 pharmacies, and diagnostic laboratories.
Provides standard external navigation links. NO JAVASCRIPT MAPS.
Strictly Python + Streamlit.
"""

import streamlit as st
from database.connection import get_db_session
from database.repositories import HealthcareServiceRepository
from services.healthcare_directory_service import HealthcareDirectoryService
from components.common import render_header, render_disclaimer, apply_theme
from components.sidebar import render_sidebar

st.set_page_config(page_title="Healthcare Directory - HealthAware AI", page_icon="🏥", layout="wide")
apply_theme()
render_sidebar()

render_header(
    title="Healthcare Services Directory",
    subtitle="Locate verified emergency departments, community clinics, 24/7 pharmacies, and diagnostic centers.",
    icon="🏥"
)

render_disclaimer()

with get_db_session() as db:
    cities = ["All"] + HealthcareServiceRepository.get_cities(db)

col1, col2, col3 = st.columns([1.5, 1, 1])
with col1:
    search_q = st.text_input("🔎 Search by facility name or address...", "")
with col2:
    category_options = ["All", "Hospital", "Clinic", "Pharmacy", "Laboratory"]
    selected_category = st.selectbox("Category Filter", options=category_options, index=0)
with col3:
    selected_city = st.selectbox("City / Region", options=cities, index=0)

with get_db_session() as db:
    cat_filter = None if selected_category == "All" else selected_category.lower()
    city_filter = None if selected_city == "All" else selected_city
    facilities = HealthcareDirectoryService.get_services(
        db=db,
        category=cat_filter,
        city=city_filter,
        search_query=search_q if search_q.strip() else None
    )

st.markdown(f"Found **{len(facilities)}** healthcare facilities:")

for f in facilities:
    emergency_tag = '<span style="background: #fee2e2; color: #991b1b; padding: 3px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: bold;">🚨 24/7 Emergency Available</span>' if f["emergency_available"] else ""
    directions_label = "📍 Get Directions ↗"
    encoded_url = f["map_url"].replace('"', '%22')
    st.markdown(
        f"""
        <div class="health-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <h4 style="margin: 0; color: #0d9488;">{f['name']}</h4>
                    <span class="badge-teal">{f['category']}</span> {emergency_tag}
                </div>
                <a href="{encoded_url}" target="_blank" rel="noopener noreferrer" style="text-decoration: none; background: #0284c7; color: white; padding: 6px 12px; border-radius: 6px; font-size: 0.85rem; font-weight: 600;">
                    {directions_label}
                </a>
            </div>
            <div style="margin-top: 10px; font-size: 0.92rem; color: #334155;">
                📍 <strong>Address:</strong> {f['address']}, {f['city']}<br>
                📞 <strong>Phone:</strong> {f['phone']} • 🕒 <strong>Hours:</strong> {f['open_hours']}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
