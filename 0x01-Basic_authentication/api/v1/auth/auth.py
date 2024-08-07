#!/usr/bin/env python3
"""Class to manage API authentication"""

from flask import request
from typing import List, TypeVar


class Auth:
    """ Authentication class to handle all authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require authentication"""
        if excluded_paths is None or path is None:
            return True

        path = path.rstrip('/') + '/'
        if path not in excluded_paths:
            return True

        return False

    def authorization_header(self, request=None) -> str:
        """authorization header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        return None
