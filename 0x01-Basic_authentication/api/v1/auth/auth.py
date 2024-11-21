#!/usr/bin/env python3
"""
Authentication Module
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """Authentication Class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        checks wether path is in excluded_paths list
        Args:
            path (str): path
            excluded_paths (List[str]): list of excluded paths

        Returns:
            bool: True if path is not in excluded_paths
        """
        if not path or not excluded_paths:
            return True
        if path[-1] != "/":
            path += "/"
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Checks wether Authorization header is set
        and if so returns its value
        Args:
            request (_type_, optional): _description_. Defaults to None.

        Returns:
            str: Authorization Header
        """
        if request is None:
            return None
        auth = request.headers.get("Authorization")
        if not auth:
            return None
        return auth

    def current_user(self, request=None) -> TypeVar("User"):
        """
        Overloaded Method
        Returns:
            _type_: _description_
        """
        return None
