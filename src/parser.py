import argparse


class Parser:
    """
    A class to represent the parser object which parses the command \
        line input arguments.

    Attributes
    ----------
        parser : Instance of Parser class, needed to fetch CLI arguments

    The design of the CLI is:
    $ SyncEnd --api_key <key> --collection_name <name of collection> \
    --slack_channel <name_of_slack_channel> --trigger_interval \
    <time in second> --slack_token <slack_token>
    """

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--collection_name", required=True, dest="collection_name"
        )  # noqa: E501
        parser.add_argument("--api_key", required=True, dest="key")
        parser.add_argument(
            "--slack_channel",
            required=False,
            dest="slack_channel",
            default="general",
        )
        parser.add_argument(
            "--trigger_interval",
            required=False,
            dest="trigger_interval",
            default=10,
        )
        parser.add_argument("--slack_token", required=True, dest="slack_token")
        self.parser = parser

    def get_arguments(self):
        """
        Return all arguments required to execute CLI
        """
        args = self.parser.parse_args()
        return (
            args.collection_name,
            args.key,
            args.trigger_interval,
            args.slack_channel,
            args.slack_token,
        )
