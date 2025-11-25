#!/usr/bin/env python3
""" Unit tests and integration tests module"""

import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized
from utils import (
    access_nested_map,
    get_json,
    requests
)
from typing import (
    Mapping,
    Sequence,
    Any,
    Dict,
    Callable,
)


class TestAccessNestedMap(unittest.TestCase):
    """ Unit test the access_nested_map """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self,
                               nested_map: Mapping,
                               path: Sequence,
                               expected: Any) -> bool:
        """ Testing the method to return the correct path """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError("a")),
        ({"a": 1}, ("a", "b"), KeyError("b"))
    ])
    def test_access_nested_map_exception(self,
                                         nested_map: Mapping,
                                         path: Sequence,
                                         expected: Any) -> bool:
        """ Testing exception return """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), str(expected))


class TestGetJson(unittest.TestCase):
    """ Unit test get_json """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch('requests.get')
    def test_get_json(self, url: str, expected: Any, mock_get) -> None:
        """ Function to test json """
        mock_response = Mock()
        mock_get.return_value = mock_response

        mock_response.json.return_value = expected

        res = get_json(url)

        mock_get.assert_called_once_with(url)
        self.assertEqual(res, expected)


if __name__ == '__main__':
    unittest.main()
