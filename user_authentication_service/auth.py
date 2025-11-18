#!/usr/bin/env python3
"""
Auth module
"""
from bcrypt import gensalt, hashpw


def _hash_password(password: str) -> bytes:
    """ Hash function based on bcrypt """
    bytes = password.encode('utf-8')
    salt = gensalt()
    hash = hashpw(bytes, salt)
    return hash
