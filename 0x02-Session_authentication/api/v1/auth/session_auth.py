#!/usr/bin/env python3
"""Session auth class
"""
from api.v1.auth.auth import Auth
from typing import Dict
import uuid


class SessionAuth(Auth):
    """inherits from the parent class - Auth"""

    user_id_by_session_id: Dict = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a session ID"""
        if user_id is None:
            return None
        if type(user_id) != str:
            return None
        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id
