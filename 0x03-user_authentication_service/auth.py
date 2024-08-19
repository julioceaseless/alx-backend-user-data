#!/usr/bin/env python3
"""Authentication module"""
from db import DB
from user import User
import bcrypt
import uuid


def _hash_password(password: str) -> bytes:
    """encrypts password"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password


def _generate_uuid(self) -> str:
    """generate UUID"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers a new user"""
        session = self._db._session
        user = session.query(User).filter(User.email == email).first()
        if user:
            raise ValueError(f"User {email} already exists")

        hash_password = _hash_password(password)
        new_user = self._db.add_user(email, hash_password)
        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """validate login details"""
        session = self._db._session
        user = session.query(User).filter(User.email == email).first()
        if user:
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        return False
