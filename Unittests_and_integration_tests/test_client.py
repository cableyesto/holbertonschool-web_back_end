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


@parameterized_class(
    ("org_data", "repos_data"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ Integration test for public_repos """
    @classmethod
    def setUpClass(cls):
        """Patch requests.get to return fixture payloads."""
        cls.get_patcher = patch("utils.requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Side effect to return the correct payload based on URL
        def get_side_effect(url, *args, **kwargs):
            mock_response = Mock()
            if url == cls.org_data["repos_url"]:
                mock_response.json.return_value = cls.repos_data
            elif url.startswith("https://api.github.com/orgs/"):
                mock_response.json.return_value = cls.org_data
            else:
                mock_response.json.return_value = {}
            return mock_response

        cls.mock_get.side_effect = get_side_effect

        # Precompute expected results
        cls.expected_repos = extract_repo_names(cls.repos_data)
        cls.apache2_repos = filter_repos_by_license(
            cls.repos_data,
            "apache-2.0"
        )

    @classmethod
    def tearDownClass(cls):
        """Stop patcher to clean up."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns the correct repository names."""
        client = GithubOrgClient(self.org_data["repos_url"].split("/")[-2])
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that public_repos filters repositories by license."""
        client = GithubOrgClient(self.org_data["repos_url"].split("/")[-2])
        apache_repos = client.public_repos(license="apache-2.0")
        self.assertEqual(apache_repos, self.apache2_repos)


if __name__ == '__main__':
    unittest.main()
