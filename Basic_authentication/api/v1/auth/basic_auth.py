#!/usr/bin/env python3
""" Module of Basic Authentication
"""
from api.v1.auth.auth import Auth
from re import search
from base64 import b64encode, b64decode
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """ Basic Authentication class """
    def extract_base64_authorization_header(self,
                                            authorization_header: str
                                            ) -> str:
        """ Extract base64 of Authorization header """
        if authorization_header is None:
            return None

        if isinstance(authorization_header, str) is False:
            return None

        regex = r'^Basic '
        res = bool(search(regex, authorization_header))
        if res is False:
            return None
        else:
            regex_after = r'(?<=\bBasic\s).*'
            res_match = search(regex_after, authorization_header)
            return res_match[0]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ Decode base64 header """
        if base64_authorization_header is None:
            return None

        if isinstance(base64_authorization_header, str) is False:
            return None

        try:
            decoded = b64decode(base64_authorization_header,
                                validate=True)
            encoded = b64encode(decoded).decode("utf-8")
            res = encoded == base64_authorization_header
            if res is False:
                return None
            else:
                return decoded.decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """ Extract user credentials """
        if decoded_base64_authorization_header is None:
            return (None, None)

        if isinstance(decoded_base64_authorization_header, str) is False:
            return (None, None)

        if decoded_base64_authorization_header.find(":") == -1:
            return (None, None)
        else:
            split = decoded_base64_authorization_header.split(":", maxsplit=1)
            return (split[0], split[1])

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str
                                     ) -> TypeVar('User'):
        """ Return user object """
        if user_email is None or type(user_email) is not str:
            return None

        if user_pwd is None or type(user_pwd) is not str:
            return None

        user = User()
        user_empty = user.count()
        if user.count() < 1:
            return None

        user_presence = user.search({"email": "{}".format(user_email)})
        if len(user_presence) < 1:
            return None

        user_matching_email = user_presence.pop()
        if user_matching_email.is_valid_password(user_pwd) is False:
            return None
        else:
            return user_matching_email

    def current_user(self, request=None) -> TypeVar('User'):
        """ Return current user """
        auth_head = self.authorization_header(request)
        basic_key = self.extract_base64_authorization_header(auth_head)
        decode_basic_key = self.decode_base64_authorization_header(basic_key)
        user_cred = self.extract_user_credentials(decode_basic_key)
        current_user = self.user_object_from_credentials(user_cred[0],
                                                         user_cred[1])
        return current_user
