#!/usr/bin/env python3
"""Uses regex to obfuscate a message"""
import bcrypt


def hash_password(password: str) -> bytes:
    """hash password"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password
