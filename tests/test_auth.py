"""
Unit and Integration Tests for Authentication & Password Security
"""

import pytest
from auth.password_utils import hash_password, verify_password
from auth.authentication import AuthService
from database.connection import get_db_session, init_db
from database.repositories import UserRepository


@pytest.fixture(autouse=True)
def setup_db():
    init_db()


def test_password_hashing():
    pwd = "TestPassword@123"
    hashed = hash_password(pwd)
    assert hashed != pwd
    assert "$" in hashed
    assert verify_password(pwd, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_user_registration_and_login():
    test_username = "test_patient_user"
    test_email = "patient@testdomain.com"
    test_pwd = "SecurePassword@123"

    # 1. Clean up if exists
    with get_db_session() as db:
        existing = UserRepository.get_by_username(db, test_username)
        if existing:
            UserRepository.delete_user(db, existing.id)

    # 2. Register
    success, msg, user_data = AuthService.register_user(
        username=test_username,
        email=test_email,
        password=test_pwd,
        full_name="Test Patient"
    )
    assert success is True
    assert user_data["username"] == test_username

    # 3. Duplicate registration should fail
    dup_success, dup_msg, _ = AuthService.register_user(
        username=test_username,
        email=test_email,
        password=test_pwd
    )
    assert dup_success is False

    # 4. Valid Login
    login_success, login_msg, logged_user = AuthService.login_user(test_username, test_pwd)
    assert login_success is True
    assert logged_user["email"] == test_email

    # 5. Invalid Login
    fail_success, fail_msg, _ = AuthService.login_user(test_username, "IncorrectPassword")
    assert fail_success is False
