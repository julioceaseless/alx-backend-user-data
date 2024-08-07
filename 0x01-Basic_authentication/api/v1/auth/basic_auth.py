#!/usr/bin/env python3
"""Basic authentication"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Basic auth"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        if authorization_header is None or\
           not isinstance(authorization_header, str) or\
           not authorization_header.startswith('Basic '):
            return None
        stripped_auth_header = authorization_header.lstrip('Basic').strip()
        return stripped_auth_header
