import sys
import unittest
from unittest.mock import Mock, patch, mock_open,call
import os
from os.path import dirname, abspath
import json

sys.path.append(dirname(dirname(abspath(__file__))))
from src.sync_ends_service import SyncEnd  # noqa: E402


class TestSyncEndsService(unittest.TestCase):
    def setUp(self):
        self.api_key = "SAM-Key-123fg"
        self.collection_name = "test server"
        self.trigger_interval = 9
        self.slack_channel = "sample channel"
        self.slack_token = "123ff"
        self.webhook = "sample MS teams webhook URL"
        self.channel_type = "all"
        self.sender_email = "example1@example.com"
        self.sender_pwd = "example1"
        self.recipient_email = "example2@example.com"

        self.sync_end = SyncEnd(
        api_key = self.api_key,
        collection_name = self.collection_name,
        trigger_interval = self.trigger_interval,
        slack_channel = self.slack_channel,
        slack_token = self.slack_token,
        webhook = self.webhook,
        channel_type = self.channel_type,
        sender_email = self.sender_email,
        sender_pwd = self.sender_pwd,
        recipient_email = self.recipient_email
        )

        self.end_point_list = []
        self.common_end_point = []
        endpoint1 = Mock()
        endpoint1.id = "385f7848-62db-4435-b7cf-820c3e7e5097"
        endpoint1.name = "Endpoint 1"
        endpoint1.authentication = None
        endpoint1.method = "POST"
        endpoint1.header = []
        endpoint1.url = "http://127.0.0.1:5002/endpoint?ep_id=1"
        endpoint1.query_parameters = [{"key": "ep_id", "value": "1"}]

        self.end_point_list.append(endpoint1)
        endpoint2 = Mock()
        endpoint2.id = "3234dt48-62db-4435-b7cf-820c3e7e5097"
        endpoint2.name = "Endpoint 2"
        endpoint2.authentication = None
        endpoint2.method = "GET"
        endpoint2.header = []
        endpoint2.url = "http://127.0.0.1:5003/endpoint?ep_id=2"
        endpoint2.query_parameters = [{"key": "ep_id", "value": "2"}]
        self.end_point_list.append(endpoint2)
        self.common_end_point.append((endpoint1, endpoint2))
        self.old_schema = {
            "collection": {
                "info": {
                    "_postman_id": "old-collection-id",
                    "id" : "old-collection-id"
                },
                "item": [
                    {
                        "name": "Endpoint 1",
                        "id" : "old-collection-id",

                        "request": {
                            "method": "GET",
                            "header": [],
                            "url": {'raw': r'{{base_url}}/info?id=3','query': [{'key': 'id', 'value': '3'}]},
                        }
                    },
                    {
                        "name": "Endpoint 2",
                        "id" : "old-collection-id",
                        "request": {
                            "method": "POST",
                            "header": [],
                            "url": {'raw': r'{{base_url}}/info?id=4','query': [{'key': 'id', 'value': '4'}]},
                        }
                    }
                ]
            }
        }
        self.new_schema = {
            "collection": {
                "info": {
                    "_postman_id": "new-collection-id",
                    "id" : "new-collection-id",
                },
                "item": [
                    {
                        "name": "Endpoint 1",
                        "id" : "new-collection-id",
                        "request": {
                            "method": "GET",
                            "header": [],
                            "url": {'raw': r'{{base_url}}/info?id=3','query': [{'key': 'id', 'value': '3'}]},
                        }
                    },
                    {
                        "name": "Endpoint 3", # New endpoint
                        "id" : "new-collection-id",
                        "request": {
                            "method": "PUT",  # Method changed
                            "header": [],
                            "url": {'raw': r'{{base_url}}/info?id=5','query': [{'key': 'id', 'value': '5'}]},  # URL changed
                        }
                    }
                ]
            }
        }
    def test_get_newly_added_message(self):
        # Test when there are newly added endpoints.

        title = (
            "Following end points are newly added in the collection :: \n\n"
        )
        output = (
            "\t"
            + str(1)
            + ")  "
            + "EndPoint Name: Endpoint 1"
            + "\n"
            + "\t"
            + "URL: "
            + "http://127.0.0.1:5002/endpoint?ep_id=1"
            + "\n"
            + "\t"
            + "Request Method: "
            + "POST"
            + "\n\n"
            + "\t"
            + str(2)
            + ")  "
            + "EndPoint Name: Endpoint 2"
            + "\n"
            + "\t"
            + "URL: "
            + "http://127.0.0.1:5003/endpoint?ep_id=2"
            + "\n"
            + "\t"
            + "Request Method: "
            + "GET"
            + "\n\n"
        )
        result = self.sync_end.get_newly_added_message(self.end_point_list)
        self.assertEqual(result, title + output)

        # Test when there are no newly added endpoints.
        result = self.sync_end.get_newly_added_message([])
        self.assertIsNone(result)

    def test_get_delete_message(self):

        title = "Following end points are deleted from the collection :: \n\n"
        output = (
            "\t"
            + str(1)
            + ")  "
            + "EndPoint Name: Endpoint 1"
            + "\n"
            + "\t"
            + "URL: "
            + "http://127.0.0.1:5002/endpoint?ep_id=1"
            + "\n"
            + "\t"
            + "Request Method: "
            + "POST"
            + "\n\n"
            + "\t"
            + str(2)
            + ")  "
            + "EndPoint Name: Endpoint 2"
            + "\n"
            + "\t"
            + "URL: "
            + "http://127.0.0.1:5003/endpoint?ep_id=2"
            + "\n"
            + "\t"
            + "Request Method: "
            + "GET"
            + "\n\n"
        )
        result = self.sync_end.get_delete_message(self.end_point_list)
        self.assertEqual(result, title + output)

        # Test when there are no deleted endpoints.
        result = self.sync_end.get_delete_message([])
        self.assertIsNone(result)

    def test_post_data_to_slack(self):
        with patch("slack.WebClient.chat_postMessage") as mock_slack:
            mock_slack.return_value = True

            data = ["New", "Delete", "Update"]
            response = self.sync_end.post_data_to_slack(data)

            self.assertEqual(response, 3)

    def test_get_updated_end_point_message(self):
        title = "Following is the list of change in the existing end points ::\n\n"  # noqa: E501
        difference = (
                    "\tNew name: "  # noqa: E126
                    + "Endpoint 1"
                    + " "
                    + "\nOld name: "
                    + "Endpoint 2"
                    + "\n"
                    + "\tNew URL: "
                    + "http://127.0.0.1:5002/endpoint?ep_id=1"
                    + " "
                    + "\nOld URL: "
                    + "http://127.0.0.1:5003/endpoint?ep_id=2"
                    + "\n"
                    + "\t New HTTP method: "
                    + "POST"
                    + " "
                    + "\nOld HTTP method: "
                    + "GET"
                    + "\n"
        )

        result = self.sync_end.get_updated_end_point_message(self.common_end_point)  # noqa: E501
        self.assertEqual(result, title + difference)

    def test_store_file(self):
        collection_schema = {
            "collection": {"info": {"_postman_id": "0000f-0f"}}
        }

        self.sync_end.collection_id = "custom_id"

        with patch("src.sync_ends_service.open", mock_open()) as mocked_file:
            self.sync_end.store_file(collection_schema)

            file_path = (
                os.path.join(dirname(dirname(abspath(__file__))), "src","data","custom_id.txt")
            )
            mocked_file.assert_called_once_with(file_path, "w", encoding="utf-8")
            mocked_file().write.assert_called_once_with(
                str(collection_schema["collection"]).replace("'", '"')
            )

    def test_post_data_to_email_success(self):
        with patch('smtplib.SMTP', autospec=True) as MockSMTP:
            # Mock the SMTP server
            smtp_instance = MockSMTP.return_value
            smtp_instance.starttls.return_value = None  # No encryption for testing

            sync_end = self.sync_end

            data = [
            'Following end points are newly added in the collection :: \n\n\t1)  EndPoint Name: Endpoint 1\n\tURL: {{base_url}}/info?id=3\n\tRequest Method: GET\n\n\t2)  EndPoint Name: Endpoint 3\n\tURL: {{base_url}}/info?id=5\n\tRequest Method: PUT\n\n', 'Following end points are deleted from the collection :: \n\n\t1)  EndPoint Name: Endpoint 1\n\tURL: {{base_url}}/info?id=3\n\tRequest Method: GET\n\n\t2)  EndPoint Name: Endpoint 2\n\tURL: {{base_url}}/info?id=4\n\tRequest Method: POST\n\n', None
            ]
            email_body = sync_end.post_data_to_email(data)
            # Assertions to verify that email sending process is correctly called
            smtp_instance.login.assert_called_once_with(sync_end.sender_email, sync_end.sender_pwd)
            smtp_instance.sendmail.assert_has_calls([
            call(sync_end.sender_email, sync_end.recipient_email, email_body),
            ])

    def test_compute_difference(self):
        # Define the old schema and new schema as dictionaries.
        # DO NOT CHANGE FORMAT as Some formats are required by files
        old_schema = self.old_schema
        new_schema = self.new_schema

        # Create a SyncEnd instance and set the collection ID
        sync_end = SyncEnd(api_key="sample-api-key", collection_name="test_collection", trigger_interval=60,
                            slack_channel="test_channel", slack_token="sample-slack-token", webhook="sample-webhook",
                            channel_type="all", sender_email="example1@example.com", sender_pwd="example1",
                            recipient_email="example2@example.com")
        sync_end.collection_id = "new-collection-id"

        # Mock the 'open' function to return the old schema when reading
        with patch("builtins.open", mock_open(read_data=json.dumps(old_schema['collection']))):
            difference = sync_end.compute_difference(new_schema)
        # Define the expected difference based on the provided old and new schemas
        expected_difference = [
            'Following end points are newly added in the collection :: \n\n\t1)  EndPoint Name: Endpoint 1\n\tURL: {{base_url}}/info?id=3\n\tRequest Method: GET\n\n\t2)  EndPoint Name: Endpoint 3\n\tURL: {{base_url}}/info?id=5\n\tRequest Method: PUT\n\n', 'Following end points are deleted from the collection :: \n\n\t1)  EndPoint Name: Endpoint 1\n\tURL: {{base_url}}/info?id=3\n\tRequest Method: GET\n\n\t2)  EndPoint Name: Endpoint 2\n\tURL: {{base_url}}/info?id=4\n\tRequest Method: POST\n\n', None
            ]

        # Check if the computed difference matches the expected difference
        self.assertEqual(difference, expected_difference)

    @patch('http.client.HTTPSConnection', autospec=True)
    def test_get_collection_schema_success(self, mock_connection):
        # Mock the HTTP connection to return a successful response
        api_key = "your_api_key"
        collection_name = "your_collection_name"
        mock_response = Mock()
        #Sample postman API response for colelction. It has lots of other info as well!
        mock_response.read.return_value = json.dumps({
            "collections": [
                {
                    "uid": "collection_uid",
                    "name": "your_collection_name"
                }
            ]
        })

        mock_connection.return_value.getresponse.return_value = mock_response

        sync_end = SyncEnd(api_key, collection_name, 60, "slack_channel", "slack_token", "webhook", "all", "sender_email", "sender_pwd", "recipient_email")

        collection_schema = sync_end.get_collection_schema()

        # Ensure the correct HTTP request is made
        mock_connection.assert_called_once_with("api.getpostman.com")

        # Ensure the returned collection schema is as expected
        expected_schema = {
            "collections": [
                {
                    "uid": "collection_uid",
                    "name": "your_collection_name"
                }
            ]
        }
        self.assertEqual(collection_schema, expected_schema)

    @patch('requests.post')
    def test_post_data_to_teams_success(self, mock_post):
        # Mock the requests.post function
        mock_response = Mock()
        mock_response.status_code = 200  # Simulate a successful POST request
        mock_post.return_value = mock_response

        difference = ["Message 1", "Message 2", ""]

        # Call the function you want to test
        self.sync_end.post_data_to_teams(difference)

        # Assertions
        expected_url = self.sync_end.ms_teams_webhook
        expected_headers = {'Content-type': 'application/json'}
        expected_calls = [call(expected_url, headers=expected_headers, data='{"text": "Message 1"}', timeout=10),
                          call(expected_url, headers=expected_headers, data='{"text": "Message 2"}', timeout=10)]

        # Verify that requests.post was called with the expected arguments
        mock_post.assert_has_calls(expected_calls, any_order=True)

    @patch('requests.post')
    def test_post_data_to_teams_empty_message(self, mock_post):
        # Mock the requests.post function
        mock_response = Mock()
        mock_response.status_code = 200  # Simulate a successful POST request
        mock_post.return_value = mock_response

        difference = []

        # Call the function you want to test
        self.sync_end.post_data_to_teams(difference)

        # Assertions
        expected_url = self.sync_end.ms_teams_webhook
        expected_headers = {'Content-type': 'application/json'}

        # Verify that requests.post was not called because messages are empty
        mock_post.assert_not_called()



if __name__ == "__main__":
    unittest.main()
