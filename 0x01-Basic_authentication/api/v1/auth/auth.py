#!/usr/bin/env python3
"""Class to manage API authentication"""
import re
from flask import request
from typing import List, TypeVar


class Auth:
    """ Authentication class to handle all authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require authentication"""
        """
        if excluded_paths is None or path is None:
            return True

        path = path.rstrip('/') + '/'
        if path not in excluded_paths:
            return True

        return False
        """
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pattern = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization header"""
        # retrieve the 'Authrization' key in headers
        # Return none if reqest is none or doesnt contain header key
        if request:
            return request.headers.get('Authorization')
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        return None
