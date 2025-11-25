#!/usr/bin/env python3
""" Unit tests and integration of client module """

import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized
# from utils import (
#     access_nested_map,
#     get_json
# )
from client import GithubOrgClient
from typing import (
    List,
    Dict,
    Any
)


class TestGithubOrgClient(unittest.TestCase):
    """ GitHub client mock """
    @parameterized.expand([
        ('google'),
        ('abc')
    ])
    @patch('client.get_json')
    def test_org(self, org: str, mock_json) -> None:
        """ Testing mock different organizations """
        instance = GithubOrgClient(org)
        res = instance.org()

        mock_json.assert_called_once_with(
            GithubOrgClient.ORG_URL.format(org=org)
        )


if __name__ == '__main__':
    unittest.main()
