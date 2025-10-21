#!/usr/bin/env python3
""" Encrypt password module """

import bcrypt


def hash_password(password: str):
    """ Hash password """
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Verify that hash match a password """
    userBytes = password.encode('utf-8')
    result = bcrypt.checkpw(userBytes, hashed_password)
    return result
