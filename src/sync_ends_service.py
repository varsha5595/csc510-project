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
            # Add the slack access token here
            token="xxxxxxxx"
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

    def compute_difference(self, new_collection_schema):

        filepath = "./data/" + self.collection_id + ".txt"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        if not os.path.exists(filepath):
            with open(filepath, "w") as file:
                # file.write("{\"item\":[]}")
                file.write(json.dumps(new_collection_schema.get('collection')))

        file = open(filepath, "r")
        old_collection_schema = json.load(file)

        # read the data from file and convrt it to collection object
        old_schema_obj = Collection(old_collection_schema)
        new_collection_obj = Collection(new_collection_schema.get('collection'))
        common_end_points = []
        for new_end_point in new_collection_obj.get_end_points():
            for old_end_point in old_schema_obj.get_end_points():
                if(new_end_point.id == old_end_point.id):
                    common_end_points.append((new_end_point, old_end_point))
                    old_schema_obj.remove_end_point(old_end_point)
                    new_collection_obj.remove_end_point(new_end_point)

        newly_added_end_point = self.get_newly_added_message(new_collection_obj.get_end_points())

        # TODO: deleted_end_points = self.get_delete_message(old_schema_obj.get_end_points())

        # TODO: updated_end_point = self.get_updated_end_point_message(common_end_points)

        # TODO: message = [newly_added_end_point, deleted_end_points, updated_end_point]

        return [newly_added_end_point]  # TODO: return message variable

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