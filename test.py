import unittest
from unittest.mock import MagicMock

from window_rate import FixedWindow


class TestFixedWindow(unittest.TestCase):

    def setUp(self):
        self.cache_server = MagicMock()  # Mock the cache server
        self.fixed_window = FixedWindow(self.cache_server, requests_per_minute=2)

    def test_get_window_start_time(self):
        expected_start_time = 1629835680  # Expected start time in seconds (rounded to the nearest minute)
        self.fixed_window.get_window_start_time = MagicMock(return_value=expected_start_time)

        self.assertEqual(self.fixed_window.get_window_start_time(), expected_start_time)

    def test_is_within_rate_limit_within_limit(self):
        user_id = 'user123'
        self.cache_server.get.return_value = 1  # Assuming one request has been made
        self.assertTrue(self.fixed_window.is_within_rate_limit(user_id))

    def test_is_within_rate_limit_exceeded_limit(self):
        user_id = 'user456'
        self.cache_server.get.return_value = 2  # Assuming two requests have been made (exceeding the limit)
        self.assertFalse(self.fixed_window.is_within_rate_limit(user_id))

    def test_rate_limit_within_limit(self):
        token = 'valid_token'
        self.fixed_window.get_user_id_from_jwt = MagicMock(return_value='user123')
        self.cache_server.get.return_value = 1  # Assuming one request has been made
        self.assertTrue(self.fixed_window.rate_limit(token))

    def test_rate_limit_exceeded_limit(self):
        token = 'valid_token'
        self.fixed_window.get_user_id_from_jwt = MagicMock(return_value='user456')
        self.cache_server.get.return_value = 2  # Assuming two requests have been made (exceeding the limit)
        self.assertFalse(self.fixed_window.rate_limit(token))

if __name__ == '__main__':
    unittest.main()
