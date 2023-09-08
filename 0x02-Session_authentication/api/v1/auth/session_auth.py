#!/usr/bin/env python3
"""Session auth class
"""
from api.v1.auth.auth import Auth
from typing import Dict
import uuid
from models.user import User


class SessionAuth(Auth):
    """inherits from the parent class - Auth"""

    user_id_by_session_id: Dict = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a session ID"""
        if user_id is None:
            return None
        if type(user_id) != str:
            return None
        generated_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[generated_id] = user_id
        return generated_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ To get user_id based on a  Session_id"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Identify the current user with session ID"""
        user_session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(user_session_cookie)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """Destroys the current session"""
        if request is None:
            return False
        user_session_cookie = self.session_cookie(request)
        if user_session_cookie is None:
            return False
        linked = self.user_id_for_session_id(user_session_cookie)
        if not linked:
            return False
        self.user_id_by_session_id.pop(user_session_cookie)
        return True
