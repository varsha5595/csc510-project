from sync_ends_parser import Parser
from sync_ends_service import SyncEnd

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
        webhook,
        channel_type,
        sender_email,
        sender_pwd,
        recipient_email
    ) = parser.get_arguments()
    sync_end = SyncEnd(
        api_key,
        collection_name,
        trigger_interval,
        slack_channel,
        slack_token,
        webhook,
        channel_type,
        sender_email,
        sender_pwd,
        recipient_email
    )

    try:
        sync_end.start()
    except Exception as excepion:
        print(excepion)


if __name__ == "__main__":
    main()
