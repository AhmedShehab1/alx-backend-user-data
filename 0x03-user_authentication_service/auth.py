#!/usr/bin/env python3
"""
Authentication Module
"""
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    generates a salt and hashes the plain-text password
    Args:
        password (str): plain-txt password

    Returns:
        bytes: hashed pwd
    """
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode(), salt)
    return hashed_pwd


class Auth:
    """Auth class to interact with the authentication database"""

    def __init__(self) -> None:
        """Constructor Special Function"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user

        Returns New User Instance
        Args:
            email (str): User Email
            password (str): User Password

        Raises:
            ValueError: Raised if a usr already exist with the given email

        Returns:
            User: New User Instance
        """
        try:
            usr = self._db.find_user_by(email=email)
        except Exception:
            usr = None

        if usr:
            raise ValueError(f"User {email} already exists")

        new_usr = self._db.add_user(
            email=email, hashed_password=_hash_password(password)
        )
        return new_usr
