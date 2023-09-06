#!/usr/bin/env python3
"""a module that describes BasicAuth
"""

from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """inherit from Auth class"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extract base64 part of authorization header of basic
        authentication
        Return: Base64 part of authorization header
                else None if not a string or none or doesnt start by Basic
        """
        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        division = authorization_header.split()
        if division[0] == 'Basic' and len(division) == 2:
            return division[1]
        return None
