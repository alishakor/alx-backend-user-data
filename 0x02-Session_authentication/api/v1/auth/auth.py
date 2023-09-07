#!/usr/bin/env python3
"""a module that describes the auth class
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """manages the API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Handles path
        Return:
            False if its in  excluded_paths else True
        """
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        if path in excluded_paths:
            return False
        # Removing the trailing slashes
        normalize_path = path.rstrip('/')
        for paths in excluded_paths:
            normalize_excluded_path = paths.rstrip('/')
            if normalize_path == normalize_excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Authorization header
        Returns: True if path not in excluded_paths
        """
        if request is None:
            return None
        if 'Authorization' in request.headers:
            return request.headers['Authorization']
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Current user's info
        returns None"""
        return None
