import sys
import argparse
import unittest
import json
from os.path import dirname, abspath
from copy import deepcopy
from unittest.mock import patch, mock_open

sys.path.append(dirname(dirname(abspath(__file__))))

from src.sync_ends_parser import Parser  # noqa: E402


class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()
        self.collection_name = "test server"
        self.postman_api_key = "SAM-Key-123fg"
        self.trigger_interval = 15
        self.slack_channel = "sample channel"
        self.slack_token = "123ff"
        self.webhook = "ms teams link"
        self.sender_email = "example1@example.com"
        self.sender_pwd = "example1"
        self.recipient_email = "example2@example.com"
        self.channel_type = "all"
        self.good_config = {

            "postman_api_key": self.postman_api_key,
            "slack_token": self.slack_token,
            "trigger_interval": self.trigger_interval,
            "collections": [
                {
                    "channel_type": self.channel_type,
                    "collection_name": self.collection_name,
                    "slack_channel": self.slack_channel,
                    "microsoft_teams_webhook" :  self.webhook,
                    "sender_email": self.sender_email,
                    "sender_pwd": self.sender_pwd,
                    "recipient_email": self.recipient_email
                }
            ],
        }

    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            config_file="somefile.json",
        ),
    )
    def test_get_args(self, mock_args):

        with patch(
            "builtins.open", mock_open(read_data=json.dumps(self.good_config))
        ):
            (
                collection_name,
                postman_api_key,
                trigger_interval,
                slack_channel,
                slack_token,
                webhook,
                channel_type,
                sender_email,
                sender_pwd,
                recipient_email

            ) = self.parser.get_arguments()
            self.assertEqual(collection_name, self.collection_name)
            self.assertEqual(postman_api_key, self.postman_api_key)
            self.assertEqual(trigger_interval, self.trigger_interval)
            self.assertEqual(slack_channel, self.slack_channel)
            self.assertEqual(slack_token, self.slack_token)

            self.assertEqual(webhook, self.webhook)
            self.assertEqual(channel_type, self.channel_type)
            self.assertEqual(sender_email, self.sender_email)
            self.assertEqual(sender_pwd, self.sender_pwd)
            self.assertEqual(recipient_email, self.recipient_email)

    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            config_file="somefile.json",
        ),
    )
    def test_get_args_throws_exception_when_missing_postmanapikey(
        self, mock_args
    ):
        bad_config = deepcopy(self.good_config)
        bad_config.pop("postman_api_key", None)
        bad_config = json.dumps(bad_config)
        m = mock_open(read_data=bad_config)
        with patch("builtins.open", m):
            with self.assertRaises(AttributeError):
                (
                    collection_name,
                    postman_api_key,
                    trigger_interval,
                    slack_channel,
                    slack_token,
                    webhook,
                    channel_type,
                    sender_email,
                    sender_pwd,
                    recipient_email
                ) = self.parser.get_arguments()

    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            config_file="somefile.json",
        ),
    )
    def test_get_args_throws_exception_when_missing_slacktoken(
        self, mock_args
    ):
        bad_config = deepcopy(self.good_config)
        bad_config.pop("slack_token", None)
        bad_config = json.dumps(bad_config)
        m = mock_open(read_data=bad_config)
        with patch("builtins.open", m):
            with self.assertRaises(AttributeError):
                (
                    collection_name,
                    postman_api_key,
                    trigger_interval,
                    slack_channel,
                    slack_token,
                    webhook,
                    channel_type,
                    sender_email,
                    sender_pwd,
                    recipient_email
                ) = self.parser.get_arguments()

    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            config_file="somefile.json",
        ),
    )
    def test_get_args_throws_exception_when_missing_collections(
        self, mock_args
    ):
        bad_config = deepcopy(self.good_config)
        bad_config.pop("collections", None)
        bad_config = json.dumps(bad_config)
        m = mock_open(read_data=bad_config)
        with patch("builtins.open", m):
            with self.assertRaises(AttributeError):
                (
                    collection_name,
                    postman_api_key,
                    trigger_interval,
                    slack_channel,
                    slack_token,
                    webhook,
                    channel_type,
                    sender_email,
                    sender_pwd,
                    recipient_email
                ) = self.parser.get_arguments()

    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            config_file="somefile.json",
        ),
    )
    def test_get_args_throws_exception_when_missing_collections_len0(
        self, mock_args
    ):
        bad_config = deepcopy(self.good_config)
        bad_config["collections"] = []
        bad_config = json.dumps(bad_config)
        m = mock_open(read_data=bad_config)
        with patch("builtins.open", m):
            with self.assertRaises(AttributeError):
                (
                    collection_name,
                    postman_api_key,
                    trigger_interval,
                    slack_channel,
                    slack_token,
                    webhook,
                    channel_type,
                    sender_email,
                    sender_pwd,
                    recipient_email
                ) = self.parser.get_arguments()

    @patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            config_file="somefile.json",
        ),
    )
    def test_get_args_throws_exception_when_missing_collection_name(
        self, mock_args
    ):
        bad_config = deepcopy(self.good_config)
        bad_config["collections"][0].pop("collection_name", None)
        bad_config = json.dumps(bad_config)
        m = mock_open(read_data=bad_config)
        with patch("builtins.open", m):
            with self.assertRaises(AttributeError):
                (
                    collection_name,
                    postman_api_key,
                    trigger_interval,
                    slack_channel,
                    slack_token,
                    webhook,
                    channel_type,
                    sender_email,
                    sender_pwd,
                    recipient_email
                ) = self.parser.get_arguments()


if __name__ == "__main__":
    unittest.main()
