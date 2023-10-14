import sys
from os.path import abspath, dirname

sys.path.append(dirname(dirname(abspath(__file__))))

from sync_ends_service import SyncEnd  # noqa: E402
from parser import Parser  # noqa: E402

def main():
    """
    A method which is the main entry point for the CLI.

    This method calls the Parser() class to parse command line arguments and \
    then instantiates the SyncEnd() class with input arguments.
    It then calls the start() method which is the interface of \
    the CLI with Postman and Slack.
    """

    # get the arguments from command line
    parser = Parser()
    (
        collection_name,
        api_key,
        trigger_interval,
        slack_channel,
        slack_token,
    ) = parser.get_arguments()
    sync_end = SyncEnd(
        api_key, collection_name, trigger_interval, slack_channel, slack_token
    )

    sync_end.start()
    # try:
    #     sync_end.start()
    # except Exception as e:
    #     print("Spam" + str(e))

if __name__ == "__main__":
    main()
