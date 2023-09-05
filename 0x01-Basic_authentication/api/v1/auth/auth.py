#!/usr/bin/env python3
"""a module that describes the auth class
"""

import request from flask

class Auth:
    """manage the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns False -path and excluded_paths"""
        return False

    def authorization_header(self, request=None) -> str:
        """returns None"""
        return None
    def current_user(self, request=None) -> TypeVar('User'):
        """returns None"""
        return None
