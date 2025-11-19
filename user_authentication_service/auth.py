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

    def create_session(self, email: str) -> str:
        """ Create a session ID """
        try:
            user = self._db.find_user_by(email=email)
            uuid = _generate_uuid()
            self._db.update_user(user.id, session_id=uuid)
            return user.session_id

        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """ Return user based on session_id """
        if not session_id:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user

        except NoResultFound:
            return None

    def destroy_session(self, user_id: int):
        """ Destroy session """
        try:
            self._db.update_user(user_id, session_id=None)
            return None

        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ Send reset password token """
        try:
            user = self._db.find_user_by(email=email)
            uuid = _generate_uuid()
            self._db.update_user(user.id, reset_token=uuid)

            return uuid

        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str):
        """ Update the password """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            # hash_pw = _hash_password(password).decode("utf-8")
            hash_pw = _hash_password(password)
            self._db.update_user(
                user.id,
                hashed_password=hash_pw,
                reset_token=None
            )

        except NoResultFound:
            raise ValueError
