import sys
import unittest
from os.path import dirname, abspath
from unittest.mock import patch
import unittest.mock

sys.path.append(dirname(dirname(abspath(__file__))))

import src.main as mn  # noqa: E402


class TestParser(unittest.TestCase):
    def setUp(self):
        self.collection_name = "test server"
        self.postman_api_key = "SAM-Key-123fg"
        self.trigger_interval = 15
        self.slack_channel = "sample channel"
        self.slack_token = "123ff"

    @patch("src.main.SyncEnd")
    @patch("src.main.Parser")
    def test_main(self, parser, syncend):
        parser.return_value.get_arguments.return_value = (
            self.collection_name,
            self.postman_api_key,
            self.trigger_interval,
            self.slack_channel,
            self.slack_token,
        )
        mn.main()

    @patch("src.main.SyncEnd")
    @patch("src.main.Parser")
    def test_main_exception(self, parser, syncend):
        parser.return_value.get_arguments.return_value = (
            self.collection_name,
            self.postman_api_key,
            self.trigger_interval,
            self.slack_channel,
            self.slack_token,
        )
        syncend.return_value.start.side_effect = Exception()
        mn.main()


if __name__ == "__main__":
    unittest.main()
