"""
HealthAware AI - Authorization & Role Checks
Enforces access control for regular users and administrator views.
"""

from typing import Optional, Dict, Any
import streamlit as st
from auth.authentication import get_current_user


def is_authenticated() -> bool:
    """Return True if a user is currently logged in."""
    user = get_current_user()
    return user is not None and "id" in user


def is_admin() -> bool:
    """Return True if currently logged in user has the 'admin' role."""
    user = get_current_user()
    return user is not None and user.get("role") == "admin"


def require_auth():
    """Display warning and stop rendering if user is unauthenticated."""
    if not is_authenticated():
        st.warning("⚠️ You must be logged in to access this feature.")
        st.info("Please go to the **Home Dashboard** or use the sidebar to log in or register.")
        st.stop()


def require_admin():
    """Display error and stop rendering if user is not an administrator."""
    require_auth()
    if not is_admin():
        st.error("⛔ Access Denied: Administrator privileges required to view this page.")
        st.stop()
