#!/usr/bin/env python3
"""
Session Authentication Module
"""
from typing import TypeVar
import uuid
from models.user import User
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """Session Authentication Class"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a New Session

        Returns the ID for the created Session
        Args:
            user_id (str, optional): User ID associated with Session.
            Defaults to None.

        Returns:
            str: Created Session ID
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves a USER ID based on a given Session ID
        Args:
            session_id (str, optional): Session ID. Defaults to None.

        Returns:
            str: user id associated with current session if any
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar("User"):
        """
        Retrieves User based on his session ID
        Returns:
            _type_: _description_
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """Destroy Session Method
           Returns:
              _type_: _description_
        """
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        user = User.get(user_id)
        if not user:
            return False
        self.user_id_by_session_id.pop(session_id)
        return True
