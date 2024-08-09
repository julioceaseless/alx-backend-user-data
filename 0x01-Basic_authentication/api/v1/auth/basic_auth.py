#!/usr/bin/env python3
"""Basic authentication"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """Basic auth"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extract authorization header"""

        # check if authorization_header is valid
        if authorization_header is None or\
           not isinstance(authorization_header, str) or\
           not authorization_header.startswith('Basic '):
            return None

        # strip the header to extract base64 part
        base64_part = authorization_header.lstrip('Basic').strip()
        return base64_part

    def decode_base64_authorization_header(self,
                                           base64_auth_header: str) -> str:
        """decode base64 string"""
        if base64_auth_header is None or\
           not isinstance(base64_auth_header, str):
            return None
        try:
            # decode base64
            decoded_bytes = base64.b64decode(base64_auth_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_auth_hdr: str) -> (str, str):
        """extract basic user credentials"""
        if decoded_base64_auth_hdr is None or\
           not isinstance(decoded_base64_auth_hdr, str) or\
           decoded_base64_auth_hdr.find(':') == -1:
            return (None, None)
        email, password = decoded_base64_auth_hdr.split(':')
        return (email, password)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Retrieve user instance based in email and pass"""
        if user_email is None or user_pwd is None:
            return None
        # get all users with matching email
        users = User.search({'email': user_email})
        if not users:
            return None

        for user in users:
            if not user.is_valid_password(user_pwd):
                return None
            return user
