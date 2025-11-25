#!/usr/bin/env python3
""" Unit tests and integration of client module """

import unittest
from unittest.mock import Mock, patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
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

    @patch('client.get_json')
    def test_public_repos(self, mock_json) -> None:
        """ Unit test public repos """
        repos_url_str = "https://api.github.com/orgs/google/repos"
        mock_json.return_value = [
            {"name": "episodes.dart"},
            {"name": "cpp-netlib"}
        ]

        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock
        ) as mock_public:
            mock_public.return_value = repos_url_str
            repos_list_expected = [
                "episodes.dart",
                "cpp-netlib"
            ]

            instance = GithubOrgClient('google')
            res = instance.public_repos()

            self.assertEqual(res, repos_list_expected)
            mock_public.assert_called_once()

        mock_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self,
                         repo: Dict[str, Dict],
                         license_key: str,
                         expected: Any) -> None:
        """ Unit test has license """
        instance = GithubOrgClient('google')
        res = instance.has_license(repo, license_key)

        self.assertEqual(res, expected)


def extract_repo_names(repos):
    """Helper function to extract repository names from repo dicts."""
    return [repo["name"] for repo in repos]


def filter_repos_by_license(repos, license_key):
    """Helper function to filter repositories by license key."""
    return [repo["name"] for repo in repos if repo.get("license")
            and repo["license"]["key"] == license_key]

# Build parameter tuples including all required names
PARAMS = []
for item in TEST_PAYLOAD:
    org_data = item[0]
    repos_data = item[1]
    expected = [repo["name"] for repo in repos_data]
    apache = [repo["name"] for repo in repos_data
              if repo.get("license") and repo["license"]["key"] == "apache-2.0"]
    PARAMS.append((org_data, repos_data, expected, apache, item))

# Decorate class with all five parameter names
@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos", "TEST_PAYLOAD"),
    PARAMS
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""
    @classmethod
    def setUpClass(cls):
        """Patch requests.get to return fixture payloads."""
        cls.get_patcher = patch("utils.requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Side effect to return correct JSON depending on URL
        def get_side_effect(url, *args, **kwargs):
            mock_response = Mock()
            if url == cls.org_payload["repos_url"]:
                mock_response.json.return_value = cls.repos_payload
            elif url.startswith("https://api.github.com/orgs/"):
                mock_response.json.return_value = cls.org_payload
            else:
                mock_response.json.return_value = {}
            return mock_response

        cls.mock_get.side_effect = get_side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Return all public repo names."""
        client = GithubOrgClient(self.org_payload["repos_url"].split("/")[-2])
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Return repos filtered by license."""
        client = GithubOrgClient(self.org_payload["repos_url"].split("/")[-2])
        apache_repos = client.public_repos(license="apache-2.0")
        self.assertEqual(apache_repos, self.apache2_repos)