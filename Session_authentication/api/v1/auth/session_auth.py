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
