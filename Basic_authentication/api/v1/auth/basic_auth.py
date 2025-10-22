#!/usr/bin/env python3
""" Module of Basic Authentication
"""
from api.v1.auth.auth import Auth
from re import search
from base64 import b64encode, b64decode


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
