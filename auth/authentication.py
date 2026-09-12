"""
HealthAware AI - Authentication Service
Handles registration, login, logout, and Streamlit session integration.
"""

from typing import Optional, Dict, Any, Tuple
import streamlit as st
from database.connection import get_db_session
from database.repositories import UserRepository, AuditLogRepository
from auth.password_utils import hash_password, verify_password


class AuthService:
    @staticmethod
    def register_user(username: str, email: str, password: str, full_name: str = "", language: str = "en") -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """Register a new user after validation."""
        username = username.strip().lower()
        email = email.strip().lower()

        if len(username) < 3:
            return False, "Username must be at least 3 characters long.", None
        if len(password) < 6:
            return False, "Password must be at least 6 characters long.", None
        if "@" not in email or "." not in email:
            return False, "Please enter a valid email address.", None

        with get_db_session() as db:
            if UserRepository.get_by_username(db, username):
                return False, "Username is already registered.", None
            if UserRepository.get_by_email(db, email):
                return False, "Email address is already in use.", None

            pwd_hash = hash_password(password)
            user = UserRepository.create(
                db=db,
                username=username,
                email=email,
                password_hash=pwd_hash,
                full_name=full_name,
                role="user",
                language=language
            )
            AuditLogRepository.log(db, action="USER_REGISTER", user_id=user.id, resource="auth", details=f"User {username} registered")
            
            user_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role,
                "language": user.preferred_language
            }
            return True, "Registration successful!", user_data

    @staticmethod
    def login_user(username_or_email: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """Authenticate user by username or email."""
        identifier = username_or_email.strip().lower()
        if not identifier or not password:
            return False, "Please provide both username/email and password.", None

        # Keep the simple demo credentials convenient for local evaluation while
        # preserving the existing seeded account and stored password hash.
        if identifier == "demo" and password == "123":
            identifier = "demouser"
            password = "User@123"

        with get_db_session() as db:
            user = UserRepository.get_by_username(db, identifier)
            if not user:
                user = UserRepository.get_by_email(db, identifier)

            if not user or not verify_password(password, user.password_hash):
                AuditLogRepository.log(db, action="LOGIN_FAILED", resource="auth", status="FAILED", details=f"Failed attempt for {identifier}")
                return False, "Invalid credentials. Please check your username and password.", None

            AuditLogRepository.log(db, action="USER_LOGIN", user_id=user.id, resource="auth", details=f"User {user.username} logged in")

            user_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role,
                "language": user.preferred_language
            }
            return True, "Login successful!", user_data

    @staticmethod
    def init_default_accounts():
        """Create initial admin and demo user accounts if they don't exist."""
        with get_db_session() as db:
            # Check admin
            if not UserRepository.get_by_username(db, "admin"):
                admin_hash = hash_password("Admin@123")
                admin = UserRepository.create(
                    db=db,
                    username="admin",
                    email="admin@healthaware.ai",
                    password_hash=admin_hash,
                    full_name="System Administrator",
                    role="admin",
                    language="en"
                )
                AuditLogRepository.log(db, action="SYSTEM_INIT", user_id=admin.id, details="Created default admin account")

            # Check demo user
            if not UserRepository.get_by_username(db, "demouser"):
                user_hash = hash_password("User@123")
                demo_user = UserRepository.create(
                    db=db,
                    username="demouser",
                    email="demo@healthaware.ai",
                    password_hash=user_hash,
                    full_name="Alex Morgan",
                    role="user",
                    language="en"
                )
                AuditLogRepository.log(db, action="SYSTEM_INIT", user_id=demo_user.id, details="Created default demo user account")


def get_current_user() -> Optional[Dict[str, Any]]:
    """Retrieve currently authenticated user from Streamlit session state."""
    return st.session_state.get("user")


def set_current_user(user_data: Optional[Dict[str, Any]]):
    """Set or clear active user in Streamlit session state."""
    st.session_state["user"] = user_data


def logout_user():
    """Clear session authentication state."""
    if "user" in st.session_state and st.session_state["user"]:
        with get_db_session() as db:
            AuditLogRepository.log(db, action="USER_LOGOUT", user_id=st.session_state["user"]["id"], details="User logged out")
    st.session_state["user"] = None
    if "conversation_id" in st.session_state:
        del st.session_state["conversation_id"]
