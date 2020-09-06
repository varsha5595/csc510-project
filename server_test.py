import slack
from slack import WebClient
from coinbot import CoinBot
import os

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Create a slack client
slack_web_client = WebClient(token = "")
# Get a new CoinBot
coin_bot = CoinBot("#postman")

# Get the onboarding message payload
message = coin_bot.get_message_payload()

# Post the onboarding message in Slack
slack_web_client.chat_postMessage(**message)