#!/usr/bin/env python3
""" Module of Session Authentication
"""
from api.v1.auth.auth import Auth
from uuid import uuid4


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
