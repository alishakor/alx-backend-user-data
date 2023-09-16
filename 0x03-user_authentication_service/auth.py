#!/usr/bin/env python3
"""
Authentication module
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """hashes a user password"""
    salt = bcrypt.gensalt(rounds=12)  # rounds helps make hashing more secure
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """generate a unique id"""
    return str(uuid4)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers user by email and password"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_pswd = _hash_password(password)
            return self._db.add_user(email, hashed_pswd)

    def valid_login(self, email: str, password: str) -> bool:
        """validates the user's Login credentials"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                user_password = user.hashed_password
                if bcrypt.checkpw(password.encode('utf-8'), user_password):
                    return True
                else:
                    return False
        except NoResultFound:
            return False
