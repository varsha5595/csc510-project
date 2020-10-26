import sys

sys.path.append("..")

import argparse
import unittest
from unittest import mock
from src.parser import Parser


class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()
        
    @mock.patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(collection_name='test server', key='SAM-Key-123fg', trigger_interval=9, slack_channel='sample channel', slack_token='123ff'))
    def test_get_args(self,mock_args):
        (
        collection_name,
        api_key,
        trigger_interval,
        slack_channel,
        slack_token,
        ) = self.parser.get_arguments()
        # print(args)
        self.assertEqual(collection_name, 'test server')
        self.assertEqual(api_key, 'SAM-Key-123fg')
        self.assertEqual(trigger_interval, 9)
        self.assertEqual(slack_channel, 'sample channel')
        self.assertEqual(slack_token, '123ff')
    
if __name__ == "__main__":
    unittest.main()
