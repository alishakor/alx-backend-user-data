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
    return str(uuid4())


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

    def create_session(self, email: str) -> str:
        """Get a user's session id"""
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()
            return user.session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Find user by session_id"""
        try:
            if session_id is None:
                return None
            user = self._db.find_user_by(session_id=session_id)
            if user:
                return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys session using user_id"""
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generate a reset password token to a user"""
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates a user's password using reset token"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            if user is None:
                raise ValueError
            new_hashed_pwd = _hash_password(password)
            self._db.update_user(user.id, hashed_password=new_hashed_pwd,
                                 reset_token=None)
        except Exception:
            raise ValueError
