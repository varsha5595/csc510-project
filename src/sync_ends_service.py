# Standard library imports
import http.client
import json
import os
import time
import ssl

# Third party imports
from slack import WebClient
from src.collection import Collection

ssl._create_default_https_context = ssl._create_unverified_context


class SyncEnd:
    def __init__(self, api_key, collection_name, trigger_interval, slack_channel, slack_token):

        self.api_key = api_key
        self.collection_name = collection_name
        self.trigger_interval = trigger_interval
        self.slack_channel = slack_channel
        self.slack_token = slack_token
        self.collection_id = 0

    def get_collection_schema(self):

        boundary = ""
        payload = ""
        headers = {
            "X-Api-Key": self.api_key,
            "Content-type": "multipart/form-data; boundary={}".format(boundary)
        }
        connection = http.client.HTTPSConnection("api.getpostman.com")
        connection.request("GET", "/collections", payload, headers)
        response = connection.getresponse()
        collections = json.loads(response.read())
        collection = list(
            filter(
                lambda x: self.collection_name == x["name"],
                collections.get("collections"),
            )
        )
        if len(collection) == 0:
            raise NameError("Invalid collection name !!!")
        self.collection_id = collection[0]["uid"]
        connection.request(
            "GET", "/collections/" + self.collection_id, payload, headers
        )
        collection_schema_response = connection.getresponse()
        return json.loads(collection_schema_response.read())

    def post_data_to_slack(self, data):

        slack_web_client = WebClient(
            # Add the slack access token here
            token=self.slack_token
        )
        for x in data:
            if x != None and len(x) > 0:
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
            output = (
                output
                + "\t"
                + str(i + 1)
                + ")  "
                + end_point.name
                + "\n"
                + "\t"
                + "URL: "
                + end_point.url
                + "\n"
                + "\t"
                + "Request Method: "
                + end_point.method
                + "\n\n"
            )
        if output == "":
            return None
        return title + output

    def get_delete_message(self, end_point_list):
        title = "Following end points are deleted from the collection\n\n"
        output = ""
        for i, end_point in enumerate(end_point_list):
            output = (
                output
                + "\t"
                + str(i + 1)
                + ")  "
                + "EndPoint Name: "
                + end_point.name
                + "\n"
                + "\t"
                + "URL: "
                + end_point.url
                + "\n"
                + "\t"
                + "Request Method: "
                + end_point.method
                + "\n\n"
            )
        if output == "":
            return None
        return title + output

    def get_updated_end_point_message(self, common_end_points):
        title = "Following is the list of change in the existing end points:\n\n"
        difference = ""
        for end_point_tuple in common_end_points:
            difference = ""
            new_end_point = end_point_tuple[0]
            old_end_point = end_point_tuple[1]

            # compute change in name
            if new_end_point.name != old_end_point.name:
                difference += (
                    "\tNew name: "
                    + new_end_point.name
                    + " "
                    + "Old name: "
                    + old_end_point.name
                    + "\n"
                )

            if new_end_point.url != old_end_point.url:
                difference += (
                    "\tNew URL: "
                    + new_end_point.url
                    + " "
                    + "Old URL: "
                    + old_end_point.url
                    + "\n"
                )

            # compute change in authentication
            if new_end_point.authentication != old_end_point.authentication:
                if new_end_point.authentication == None:
                    difference += "\tNew Authentication: None"
                else:
                    difference += (
                        "\tNew Authentication: Key :"
                        + new_end_point.authentication["apikey"][1]["value"]
                        + ", Value : "
                        + new_end_point.authentication["apikey"][0]["value"]
                        + "\n"
                    )

            # Compute change in the HTTP request type
            if new_end_point.method != old_end_point.method:
                difference += (
                    "\t New HTTP method: "
                    + new_end_point.method
                    + " "
                    + "Old HTTP method: "
                    + old_end_point.method
                    + "\n"
                )

        if difference == "":
            return None

        return title + difference

    def compute_difference(self, new_collection_schema):

        filepath = "./data/" + self.collection_id + ".txt"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        if not os.path.exists(filepath):
            with open(filepath, "w") as file:
                # file.write("{\"item\":[]}")
                file.write(json.dumps(new_collection_schema.get("collection")))

        file = open(filepath, "r")
        old_collection_schema = json.load(file)

        # read the data from file and convrt it to collection object
        old_schema_obj = Collection(old_collection_schema)
        new_collection_obj = Collection(new_collection_schema.get("collection"))
        common_end_points = []
        for new_end_point in new_collection_obj.get_end_points():
            for old_end_point in old_schema_obj.get_end_points():
                if new_end_point.id == old_end_point.id:
                    common_end_points.append((new_end_point, old_end_point))
                    old_schema_obj.remove_end_point(old_end_point)
                    new_collection_obj.remove_end_point(new_end_point)

        newly_added_end_point = self.get_newly_added_message(
            new_collection_obj.get_end_points()
        )

        deleted_end_points = self.get_delete_message(old_schema_obj.get_end_points())

        updated_end_point = self.get_updated_end_point_message(common_end_points)

        message = [newly_added_end_point, deleted_end_points, updated_end_point]

        return message

    def store_file(self, new_collection):

        filepath = "./data/" + self.collection_id + ".txt"
        with open(filepath, "w") as file:
            file.write(json.dumps(new_collection.get("collection")))

    def start(self):

        while True:

            # get the current configuration of the schema
            new_collection_schema = self.get_collection_schema()

            # compute the difference with the previous schema
            difference = self.compute_difference(new_collection_schema)

            # post the difference to the slack
            self.post_data_to_slack(difference)

            # store new schema to the file
            self.store_file(new_collection_schema)
            
            time.sleep(self.trigger_interval)
