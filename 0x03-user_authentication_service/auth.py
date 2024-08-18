#!/usr/bin/env python3
"""Authentication module"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """encrypts password"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password
