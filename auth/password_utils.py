"""
HealthAware AI - Secure Password Utilities
Uses PBKDF2-HMAC-SHA256 with 100,000 iterations and a 16-byte random salt.
Provides cryptographic security without binary dependencies.
"""

import hashlib
import os
import secrets


def hash_password(password: str) -> str:
    """Hash a password using PBKDF2-HMAC-SHA256 with a unique salt."""
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return f"{salt}${key.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    """Verify a plain password against the stored salt$hash string."""
    try:
        salt, key_hex = stored_hash.split('$')
        computed_key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return secrets.compare_digest(computed_key.hex(), key_hex)
    except Exception:
        return False
