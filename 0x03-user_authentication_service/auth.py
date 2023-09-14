#!/usr/bin/env python3
"""
Authentication module
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """hashes a user password"""
    salt = bcrypt.gensalt(rounds=12)  # rounds helps make hashing more secure
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
