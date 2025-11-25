#!/usr/bin/env python3
""" Unit tests and integration of client module """

import unittest
from unittest.mock import Mock, patch, PropertyMock
from parameterized import parameterized
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

    def test_public_repos_url(self):
        """ Property mocking test """
        with patch(
            'client.GithubOrgClient.org',
            new_callable=PropertyMock
        ) as mock_memoize:
            repos_url_str = "https://api.github.com/orgs/google/repos"
            mock_memoize.return_value = {"repos_url": repos_url_str}

            instance = GithubOrgClient('google')
            res = instance._public_repos_url

            self.assertEqual(res, repos_url_str)


if __name__ == '__main__':
    unittest.main()
