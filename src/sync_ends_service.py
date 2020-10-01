# Standard library imports
import http.client
import json
import os
import re
import time
import ssl

# Third party imports
from jsondiff import diff
from slack import WebClient

ssl._create_default_https_context = ssl._create_unverified_context


class SyncEnd:

    def __init__(self, api_key, collection_name, trigger_interval, slack_channel):

        self.api_key = api_key
        self.collection_name = collection_name
        self.trigger_interval = trigger_interval
        self.slack_channel = slack_channel
        self.collection_id = 0

    def get_collection_schema(self):

        boundary = ""
        payload = ""
        headers = {
            "X-Api-Key": self.api_key,
            "Content-type": "multipart/form-data; boundary={}".format(boundary),
        }
        connection = http.client.HTTPSConnection("api.getpostman.com")
        connection.request("GET", "/collections", payload, headers)
        response = connection.getresponse()
        collections = json.loads(response.read())
        collection = list(filter(lambda x: self.collection_name == x['name'], collections.get('collections')))
        if(len(collection) == 0):
            raise NameError("Invalid collection name !!!")
        self.collection_id = collection[0]["uid"]
        connection.request("GET", "/collections/" + self.collection_id , payload, headers)
        collection_schema_response = connection.getresponse()
        return json.loads(collection_schema_response.read())

    def post_data_to_slack(self, data):
        
        slack_web_client = WebClient(
            token="xoxb-1402730973745-1375362971159-nYAbxKiu34jjEvlWMzN02rgm"
            )
        for x in data:
            if x != None:
                message = {
                    "channel": self.slack_channel,
                    "blocks": [
                        {
                            "type": "section",
                            "text": {"type": "plain_text", "text": x},
                        }
                    ],
                }
                slack_web_client.chat_postMessage(**message)
    
    def get_newly_added_message(self, end_point_list):
        title = "Following end points are newly added in the collection\n\n"
        output = ""
        for i, end_point in enumerate(end_point_list):
            output = output + "\t" + str(i+1) + ")  " + end_point.name + "\n" +\
                    "\t" + "URL: " + end_point.url + "\n" +\
                    "\t" + "Request Method: " + end_point.method + "\n\n"
        return title + output

    def start(self):

        # get the current configuration of the schema
        new_collection_schema = self.get_collection_schema()

        # compute the difference with the previous schema
        difference = self.compute_difference(new_collection_schema)

        # post the difference to the slack
        self.post_data_to_slack(difference)

        # store new schema to the file
        # TODO: add method to write the current schema to file

        # wait fpr the trigger interval time period
        time.sleep(self.trigger_interval)