#!/usr/bin/env python3
"""Unit tests for utils module."""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns expected results."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError)
    ])
    def test_access_nested_map_exception(self, nested_map, path, exception):
        """Test that KeyError is raised for invalid paths."""
        with self.assertRaises(exception) as cm:
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test cases for get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url, test_payload):
        """Test that get_json returns expected result."""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response
            
            result = get_json(test_url)
            
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test cases for memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches method results."""
        
        class TestClass:
            """Test class for memoize decorator."""
            
            def a_method(self):
                """Simple method that returns 42."""
                return 42

            @memoize
            def a_property(self):
                """Memoized property that calls a_method."""
                return self.a_method()
        
        with patch.object(TestClass, 'a_method',
                          return_value=42) as mock_method:
            test_obj = TestClass()
            
            # Call a_property twice
            result1 = test_obj.a_property
            result2 = test_obj.a_property
            
            # Check that results are correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            
            # Check that a_method was called only once
            mock_method.assert_called_once()


if __name__ == '__main__':
    unittest.main()
