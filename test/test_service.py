import unittest
from unittest.mock import patch
import http.client

from src.sync_ends_service import get_postman_collections
from src.sync_ends_service import get_selected_collection
from src.sync_ends_service import regex


class Test(unittest.TestCase):

    postman_connection = http.client.HTTPSConnection("api.getpostman.com")

    def test_regex(self):
        self.assertEqual(regex(str([{'key': 'asdf'}, {'key': 'qwer'}])), [["'asdf'", "'qwer'"], [], [], []])
        self.assertEqual(regex(str([{'value': 'abc'}, {'value': 'xyz'}])), [[], ["'abc'", "'xyz'"], [], []])
        self.assertEqual(regex(str([{'key': 'asdf', 'value': 'abc'}, {'key': 'qwer', 'value': 'xyz'}])), [["'asdf'", "'qwer'"], ["'abc'", "'xyz'"], [], []])
        self.assertEqual(regex(str([{'delete': [1]}, {'insert': [(1, {'key': 'qwer', 'value': 'xyz'})]}])), [["'qwer'"], ["'xyz'"], [], []])
        self.assertEqual(regex(str([{'insert': [(1, {'key': 'qwer', 'value': 'xyz'})]}, {'delete': [1]}])), [["'qwer'"], ["'xyz'"], [], []])

    def test_getcollections(self):
        with patch(__name__ + '.get_postman_collections') as mock_request:
            result = mock_request.return_value
            result.method.return_value = {'qwer': 'wxyz'}
            data = get_postman_collections(self.postman_connection, 'abcd')
            self.assertIsNotNone(data.read())

    def test_selectedcollection(self):
        with patch(__name__ + '.regex') as mock_regex:
            with patch(__name__ + '.get_selected_collection') as mock_request:
                result = mock_request.return_value
                result.method.return_value = [["'asdf'", "'qwer'"], [], [], []]
                data = get_selected_collection('collection_1', self.postman_connection, 'abcd')
                self.assertIsNotNone(data)
