import slack
from slack import WebClient
import os

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Create a slack client
slack_web_client = WebClient(token = "")

# Slack Channel to post the message
channel = "postman"

# Get the onboarding message payload
message = {
            "channel": channel,
            "blocks": [
                { "type": "section", "text": { "type": "plain_text", "text": "Sending Differences in Json"}}
            ],
        }

# Post the onboarding message in Slack
slack_web_client.chat_postMessage(**message)