#!/usr/bin/env python3
"""Basic authentication"""
from api.v1.auth.auth import Auth
import base64


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
