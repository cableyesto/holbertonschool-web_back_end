#!/usr/bin/env python3
"""
Auth module
"""
from bcrypt import gensalt, hashpw, checkpw
from uuid import uuid4
from db import DB
from sqlalchemy.orm.exc import NoResultFound

from user import User


def _hash_password(password: str) -> bytes:
    """ Hash function based on bcrypt """
    bytes = password.encode('utf-8')
    salt = gensalt()
    hash = hashpw(bytes, salt)
    return hash


def _generate_uuid() -> str:
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ Initialize the Auth class """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register a user with DB methods """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError("User {} already exists.".format(email))

        except NoResultFound:
            hashed_password = _hash_password(password)

            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """ Verify the login credentials """
        try:
            user = self._db.find_user_by(email=email)
            pw_encoded = password.encode('utf-8')
            return checkpw(pw_encoded, user.hashed_password)

        except NoResultFound:
            return False
