#!/usr/bin/env python3
"""Uses regex to obfuscate a message"""
import bcrypt


def hash_password(password: str) -> bytes:
    """hash password"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """validates that the given password matches the hashed password"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
