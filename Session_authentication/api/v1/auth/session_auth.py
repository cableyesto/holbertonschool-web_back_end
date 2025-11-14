#!/usr/bin/env python3
""" Module of Session Authentication
"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """ Session Authentication class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create a session ID for a user_id """
        if user_id is None:
            return None

        if isinstance(user_id, str) is False:
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id.update({session_id: user_id})

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID based on a Session ID """
        if session_id is None:
            return None

        if isinstance(session_id, str) is False:
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ Returns a User instance based on a cookie value """
        session_id_from_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id_from_cookie)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """ deletes the user session """
        if request is None:
            return False

        session_id_from_cookie = self.session_cookie(request)
        if not session_id_from_cookie:
            return False

        user_id = self.user_id_for_session_id(session_id_from_cookie)
        if not user_id:
            return False

        self.user_id_by_session_id.pop(session_id_from_cookie)
        return True
