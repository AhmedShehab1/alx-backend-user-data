#!/usr/bin/env python3
"""
BasicAuth Module
"""
from api.v1.auth.auth import Auth
import base64
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    """BasicAuth Class"""

    def extract_base64_authorization_header(self, authorization_header: str)\
            -> str:
        """
        Returns Base64 part of the Authorization header
        Args:
            authorization_header (str): authorization header

        Returns:
            str: _description_
        """
        if (
            authorization_header is None
            or not isinstance(authorization_header, str)
            or not authorization_header.startswith("Basic ")
        ):
            return None
        return authorization_header.split()[1]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """
        Decodes a Base64 string into a UTF-8 string.

        Returns None if the input is not a valid Base64
        string or if input is invalid

        Args:
            base64_authorization_header (str): Base64 encoded string.

        Returns:
            str: The decoded string if valid, otherwise None
        """
        if base64_authorization_header is None or not isinstance(
            base64_authorization_header, str
        ):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode("utf-8")
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> Tuple[str, str]:
        """
        Extracts User data from decoded Base64 String

        Returns None if the input is not valid
        (i.e Doesnt include ':' || Not a str || None)

        Args:
            decoded_base64_authorization_header (str): Decoded String

        Returns:
            Tuple[str, str]: user data
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if decoded_base64_authorization_header.find(":") == -1:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(":"))

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar("User"):
        """
        Returns User instance based on email & password
        Args:
            self (_type_): _description_

        Returns:
            _type_: _description_
        """
        if (
            not user_email
            or not user_pwd
            or not isinstance(user_pwd, str)
            or not isinstance(user_email, str)
        ):
            return None
        user = User.search({"email": user_email})[0]
        if not user:
            return None
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar("User"):
        """
        Retrieves User instance for a request
        Returns:
            _type_: _description_
        """
        auth = self.authorization_header(request)
        if auth is None:
            return None
        token = self.extract_base64_authorization_header(auth)
        if not token:
            return None
        decoded_token = self.decode_base64_authorization_header(token)
        if not decoded_token:
            return None
        extracted_credentials = self.extract_user_credentials(decoded_token)
        if not extracted_credentials:
            return None
        user = self.user_object_from_credentials(*extracted_credentials)
        if not user:
            return None
        return user
