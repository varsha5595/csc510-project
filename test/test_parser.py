import sys
import argparse
import unittest
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from unittest import mock  # noqa: E402
from src.parser import Parser  # noqa: E402


class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    @mock.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            collection_name="test server",
            key="SAM-Key-123fg",
            trigger_interval=9,
            slack_channel="sample channel",
            slack_token="123ff",
        ),
    )
    def test_get_args(self, mock_args):
        (
            collection_name,
            api_key,
            trigger_interval,
            slack_channel,
            slack_token,
        ) = self.parser.get_arguments()
        self.assertEqual(collection_name, "test server")
        self.assertEqual(api_key, "SAM-Key-123fg")
        self.assertEqual(trigger_interval, 9)
        self.assertEqual(slack_channel, "sample channel")
        self.assertEqual(slack_token, "123ff")


if __name__ == "__main__":
    unittest.main()
