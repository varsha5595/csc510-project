import argparse


class Parser:
    """
    The design of the CLI is
    $ SyncEnd --api_key <key> --collection_name <name of collection> --trigger_interval <time in second>
    """

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--collection_name", required=True, dest="collection_name")
        parser.add_argument("--api_key", required=True, dest="key")
        parser.add_argument(
            "--slack_channel", required=False, dest="slack_channel", default="general"
        )
        parser.add_argument(
            "--trigger_interval", required=False, dest="trigger_interval", default=10
        )
        parser.add_argument("--slack_token", required=True, dest="slack_token")
        self.parser = parser

    def get_argumenets(self):
        args = self.parser.parse_args()
        return args.collection_name, args.key, args.trigger_interval, args.slack_channel, args.slack_token