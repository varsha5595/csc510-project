import sys

sys.path.append("..")

from src.sync_ends_service import SyncEnd  # noqa: 402
from src.parser import Parser  # noqa: 402


def main():
    # get the arguments from commadn line
    parser = Parser()
    (
        collection_name,
        api_key,
        trigger_interval,
        slack_channel,
        slack_token,
    ) = parser.get_argumenets()
    sync_end = SyncEnd(
        api_key, collection_name, trigger_interval, slack_channel, slack_token
    )

    try:
        sync_end.start()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
