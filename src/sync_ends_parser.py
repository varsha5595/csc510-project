import argparse
import json


class Parser:
    """
    A class to represent the parser object which parses the command \
        line input arguments.

    Attributes
    ----------
        parser : Instance of Parser class, needed to fetch CLI arguments

    The design of the CLI is:

    """

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--config_file",
            required=True,
            dest="config_file",
            default="sync-ends-config.json",
        )
        self.collection_name = ""
        self.postman_api_key = ""
        self.trigger_interval = 10
        self.slack_channel = "general"
        self.slack_token = ""
        self.webhook = ""
        self.channel_type = ""
        self.sender_email = ""
        self.sender_pwd = ""
        self.recipient_email = ""
        self.parser = parser

    def get_arguments(self):
        """
        Return all arguments required to execute CLI
        """
        args = self.parser.parse_args()
        config = None
        with open(args.config_file, "r", encoding="utf-8") as f:
            config = json.load(f)

        if "collections" in config:
            if len(config["collections"]) > 0:
                collection = config["collections"][0]
                if "collection_name" in collection:
                    self.collection_name = collection["collection_name"]
                else:
                    raise AttributeError(
                        "'collection_name' not present in 'collections'!"
                    )
                self.webhook = collection["microsoft_teams_webhook"]
                self.channel_type = collection["channel_type"]
                self.slack_channel = collection["slack_channel"]
                self.sender_email = collection["sender_email"]
                self.sender_pwd = collection["sender_pwd"]
                self.recipient_email = collection["recipient_email"]
            else:
                raise AttributeError(
                    "No 'collections' details found in config_file!"
                )
        else:
            raise AttributeError("'collections' not present in config_file!")

        if "postman_api_key" in config:
            self.postman_api_key = config["postman_api_key"]
        else:
            raise AttributeError(
                "'postman_api_key' not present in config_file!"
            )

        if "trigger_interval" in config:
            self.trigger_interval = config["trigger_interval"]

        if "slack_token" in config:
            self.slack_token = config["slack_token"]
        else:
            raise AttributeError("'slack_token' not present in config_file!")

        return (
            self.collection_name,
            self.postman_api_key,
            self.trigger_interval,
            self.slack_channel,
            self.slack_token,
            self.webhook,
            self.channel_type,
            self.sender_email,
            self.sender_pwd,
            self.recipient_email
        )
