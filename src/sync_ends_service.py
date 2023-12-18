# Standard library imports
import http.client
import json
import os
import time
import ssl
import requests
from os.path import abspath, dirname, join
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from os.path import dirname,abspath
import sys
# Append src absolute file path for test cases to execute
sys.path.append(dirname(abspath(__file__)))

# Third party imports
from slack import WebClient
from collection import Collection
from slack.errors import SlackApiError
import pymsteams

ssl._create_default_https_context = ssl._create_unverified_context


class SyncEnd:
    """
    A class to represent the SyncEnd object in the code. This object contains \
    the methods that serve as the interface for the \
    package with Postman and Slack.

    Attributes
    ----------
        api_key : API key for Postman to fetch collections
        collection_name : Postman collection name from which to fetch APIs' \
schema
        trigger_interval : interval (in seconds) post which to again fetch \
APIs schemas
        slack_channel : Slack channel name where the message will be sent
        slack_token : Slack Bot token to authorize the sending of message
        collection_id : ID of Postman collection
    """

    def __init__(
        self,
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
    ):
        self.api_key = api_key
        self.collection_name = collection_name
        self.trigger_interval = trigger_interval
        self.slack_channel = slack_channel
        self.slack_token = slack_token
        self.ms_teams_webhook = webhook
        self.channel_type = channel_type
        self.sender_email = sender_email
        self.sender_pwd = sender_pwd
        self.recipient_email = recipient_email

        self.collection_id = 0
        self.data_folder_path = join(dirname(abspath(__file__)), "data")

    def get_collection_schema(self):
        """
        Fetches the APIs schemas from the Postman collection
        """

        boundary = ""
        payload = ""
        headers = {
            "X-Api-Key": self.api_key,
            "Content-type": "multipart/form-data; boundary={}".format(
                boundary
            ),  # noqa: E501
        }

        # create a HTTPS connection object
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

        # if collection is empty, it is an invalid connection
        if len(collection) == 0:
            raise NameError("Invalid collection name !!!")

        self.collection_id = collection[0]["uid"]
        connection.request(
            "GET", "/collections/" + self.collection_id, payload, headers
        )

        # fetch the response and load the API schema as a JSON
        collection_schema_response = connection.getresponse()
        return json.loads(collection_schema_response.read())



    def post_data_to_email(self,data):
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587  # Use the appropriate SMTP port
        sender_email = self.sender_email
        sender_password = self.sender_pwd
        receiver_email = self.recipient_email
        subject = 'Postman API Changes'
        message=""
        ret_msg = ""
        for x in data:
            if x is not None and len(x) > 0:
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = receiver_email
                msg['Subject'] = subject
                message= message+"\n"+"\n"+x
        if message != "":
            msg.attach(MIMEText(message, 'plain'))
            try:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()  # Enable TLS encryption
                server.login(sender_email, sender_password)

                # Send the email
                server.sendmail(sender_email, receiver_email, msg.as_string())
                ret_msg = msg.as_string()
                print('Email sent successfully')
            except Exception as e:
                print('Error sending email:', str(e))
            finally:
                server.quit()
        # Added return to compare message body during testing
        return ret_msg


    def post_data_to_slack(self, data):
        """
        Posts the messages for APIs added, deleted and updated based on the \
        input data

        Inputs
        ----------
            data : list of strings pertaining to APIs added, deleted and \
updated
        """
        try:
            slack_web_client = WebClient(
                # Add the slack access token here
                token=self.slack_token
            )

            response_true_cnt = 0
            for x in data:
                if x is not None and len(x) > 0:
                    message = {
                        "channel": self.slack_channel,
                        "blocks": [
                            {
                                "type": "section",
                                "text": {"type": "plain_text", "text": x},
                            }
                        ],
                    }
                    response = slack_web_client.chat_postMessage(**message)

                    if response:
                        response_true_cnt += 1
        except SlackApiError as e:
            return e

        return response_true_cnt

    def get_newly_added_message(self, end_point_list):
        """
        Returns the message string for each API end point added to the \
        collection

        Inputs
        ----------
            end_point_list : list of endpoints which are newly added to the \
collection
        """
        title = "Following end points are newly added in the collection :: \n\n"  # noqa: E501
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

    def get_delete_message(self, end_point_list):
        """
        Returns the message string for each API end point deleted from the \
        collection

        Inputs
        ----------
            end_point_list : list of endpoints which are deleted from the \
collection
        """
        title = "Following end points are deleted from the collection :: \n\n"
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
        """
        Returns the message string for each API end point updated in the \
        collection

        Inputs
        ----------
            common_end_points : list of endpoints (APIs) which are modified \
in the collection
        """
        title = "Following is the list of change in the existing end points ::\n\n"  # noqa: E501
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
                    + "\nOld name: "
                    + old_end_point.name
                    + "\n"
                )

            if new_end_point.url != old_end_point.url:
                difference += (
                    "\tNew URL: "
                    + new_end_point.url
                    + " "
                    + "\nOld URL: "
                    + old_end_point.url
                    + "\n"
                )

            # compute change in authentication
            if new_end_point.authentication != old_end_point.authentication:
                if new_end_point.authentication is None:
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
                    + "\nOld HTTP method: "
                    + old_end_point.method
                    + "\n"
                )

        if difference == "":
            return None

        return title + difference

    def compute_difference(self, new_collection_schema):
        """
        Computes the difference between the new and the old collection \
        schema. The old collection schema is stored as a file in the \
        data/ directory.

        Inputs
        ----------
            new_collection_schema : dictionary representing the collection \
schema fetched through the Postman API
        """

        # specify the filepath for the collection schema, create the file if \
        # not already present
        filepath = join(self.data_folder_path, self.collection_id + ".txt")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as file:
                file.write('{"item":[]}')

        # the old (previous) collection schema is stored as a file in data/
        file = open(filepath, "r", encoding="utf-8")
        old_collection_schema = json.load(file)

        # read the data from file and convert it to collection object
        old_schema_obj = Collection(old_collection_schema)
        new_collection_obj = Collection(
            new_collection_schema.get("collection")
        )  # noqa: E501

        # iterate over each new endpoint(API) in the collection and compare
        # with old endpoint
        common_end_points = []
        old_remove = []
        new_remove = []
        for new_end_point in new_collection_obj.get_end_points():
            for old_end_point in old_schema_obj.get_end_points():

                # if same id endpoint in both old and new schemas, add it
                # to common_end_points, remove it from old endpoints
                # and new endpoints
                if new_end_point.id == old_end_point.id:
                    # if same id ,
                    # append it to common_end_points list
                    common_end_points.append((new_end_point, old_end_point))
                    old_remove.append(old_end_point)
                    new_remove.append(new_end_point)

        for endpoint in old_remove:
            old_schema_obj.remove_end_point(endpoint)

        for endpoint in new_remove:
            new_collection_obj.remove_end_point(endpoint)

        # at the end of above for loop, the 3 objects store the following information:  # noqa: E501
        # old_schema_obj - only those endpoints which are now deleted from the collection  # noqa: E501
        # new_collection_obj - only those endpoints which have been added to the collection  # noqa: E501
        # common_end_points - only those endpoints which are common b/w old and new collection schemas  # noqa: E501

        newly_added_end_point = self.get_newly_added_message(
            new_collection_obj.get_end_points()
        )

        deleted_end_points = self.get_delete_message(
            old_schema_obj.get_end_points()
        )  # noqa: E501

        updated_end_point = self.get_updated_end_point_message(
            common_end_points
        )  # noqa: E501

        message = [
            newly_added_end_point,
            deleted_end_points,
            updated_end_point,
        ]

        return message

    def store_file(self, new_collection):
        """
        Stores the collection schema as a txt file in data/ directory. This \
        will be used to fetch the schema in compute_difference().

        Inputs
        ----------
            new_collection : collection schema to be saved in the file
        """
        filepath = join(self.data_folder_path, self.collection_id + ".txt")
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(json.dumps(new_collection.get("collection")))

    def post_data_to_teams(self, difference):
        url = self.ms_teams_webhook
        for x in difference:
            if x is not None and len(x) > 0:
                message = {
                    "text": x
                }
                headers = {
                    'Content-type': 'application/json'
                }
                requests.post(url, headers=headers, data=json.dumps(message),timeout=10)


    def start(self):
        """
        Main driver function which is called from main.py to run CLI. \
        This function fetches the new collection schema through Postman API.
        Then, it computes the difference with old schema and posts the \
        relevant messages to Slack channel.
        Finally, it overwrites the new schema fetched through the API in the \
        file.
        """
        while True:

            # get the current configuration of the schema
            new_collection_schema = self.get_collection_schema()

            # compute the difference with the previous schema
            difference = self.compute_difference(new_collection_schema)

            # post the difference to the specified messaging platform
            match self.channel_type:
                case "slack":
                    self.post_data_to_slack(difference)
                case "teams":
                    self.post_data_to_teams(difference)
                case "email":
                    self.post_data_to_email(difference)
                case "slack_and_teams":
                    self.post_data_to_slack(difference)
                    self.post_data_to_teams(difference)
                case "slack_and_email":
                    self.post_data_to_slack(difference)
                    self.post_data_to_email(difference)
                case "teams_and_email":
                    self.post_data_to_teams(difference)
                    self.post_data_to_email(difference)
                case "all":
                    self.post_data_to_slack(difference)
                    self.post_data_to_teams(difference)
                    self.post_data_to_email(difference)
                case _:
                    print("Please input a valid choice into the 'channel_type' field in your configuration file")

            # if difference and self.sender_email and self.recipient_email:
            #     print("Sending Email from "+self.sender_email+ " to "+ self.recipient_email)
            #     self.post_data_to_email(difference)
            # store new schema to the file
            self.store_file(new_collection_schema)

            time.sleep(self.trigger_interval)
