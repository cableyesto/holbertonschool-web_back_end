#!/usr/bin/env python3
""" Module of Authentication
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """ Class Authentication """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Require authentication """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path in excluded_paths or path + '/' in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """ Authorization header """
        if request is None:
            return None
        head_auth = request.headers.get('Authorization', type=str)
        if head_auth is None:
            return None
        return head_auth

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user """
        return None
