#!/usr/bin/env python3
"""a module that describes BasicAuth
"""

from api.v1.auth.auth import Auth
import base64
import binascii


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

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
            ) -> str:
        """ Base64 decode
        Return: decoded value of base64 string
                else None if not a string or none or not valid Base64
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            # Attempt to decode the bas64 string
            decoded_header = base64.b64decode(base64_authorization_header)
            # convert the decoded header to a UTF-8 string
            decoded_string = decoded_header.decode('utf-8')
            if decoded_header:
                return decoded_string
            return None
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> (str, str):
        """extract user credentials from decoded base64
        Return: user email and password
                else None if not string or if none or not present
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ":" in decoded_base64_authorization_header:
            split_detail = decoded_base64_authorization_header.split(":", 1)
            return split_detail[0], split_detail[-1]
        return None, None
