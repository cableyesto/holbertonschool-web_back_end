#!/usr/bin/env python3
""" Unit tests and integration tests module"""

import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized
from utils import (
    access_nested_map,
    get_json,
    requests,
    memoize
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


class TestMemoize(unittest.TestCase):
    """ Unit test memoize """
    def test_memoize(self):
        """ Test memoize function """
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock_function:
            mock_function.return_value = 42
            my_object = TestClass()
            res1 = my_object.a_property
            self.assertEqual(res1, 42)
            res2 = my_object.a_property
            self.assertEqual(res1, 42)
            mock_function.assert_called_once()


if __name__ == '__main__':
    unittest.main()
