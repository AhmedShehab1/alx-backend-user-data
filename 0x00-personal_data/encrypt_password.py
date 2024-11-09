#!/usr/bin/env python3
"""
encrypt_password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    generates a salt and hashes the plain-text password
    Args:
        password (str): plain-text password

    Returns:
        bytes: hashed password (salt included)
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    verifies if an input password matches the hashed password
    Args:
        hashed_password (bytes): hashed password
        password (str): input password

    Returns:
        bool: True if matches else False
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
