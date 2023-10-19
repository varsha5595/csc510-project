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

            data = ["New endpoint added.", "Endpoint deleted.", "Endpoint updated"]
            sync_end.post_data_to_email(data)

            expected_message = (
            'Content-Type: multipart/mixed; boundary="===============3354826013420575687=="\n'
            'MIME-Version: 1.0\n'
            'From: example1@example.com\n'
            'To: example2@example.com\n'
            'Subject: Postman API Changes\n'
            '\n'
            '--===============3354826013420575687==\n'
            'Content-Type: text/plain; charset="us-ascii"\n'
            'MIME-Version: 1.0\n'
            'Content-Transfer-Encoding: 7bit\n'
            '\n'
            'New endpoint added.\n\nEndpoint deleted.\n\nEndpoint updated\n'
            '--===============3354826013420575687==--\n'
        )

            # Assertions to verify that email sending process is correctly called
            smtp_instance.login.assert_called_once_with(sync_end.sender_email, sync_end.sender_pwd)
            smtp_instance.sendmail.assert_has_calls([
            call(sync_end.sender_email, sync_end.recipient_email, 'New endpoint added.'),
            call(sync_end.sender_email, sync_end.recipient_email, 'Endpoint deleted.'),
            call(sync_end.sender_email, sync_end.recipient_email, 'Endpoint updated')
            ])
            smtp_instance.sendmail.assert_any_call(
                sync_end.sender_email,
                sync_end.recipient_email,
                'New endpoint added.'
            )
            smtp_instance.sendmail.assert_any_call(
                sync_end.sender_email,
                sync_end.recipient_email,
                'Endpoint deleted.'
            )
            smtp_instance.sendmail.assert_any_call(
                sync_end.sender_email,
                sync_end.recipient_email,
                'Endpoint updated.'
            )

    def test_compute_difference(self):
        # Define the old schema and new schema as dictionaries
        old_schema = {
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
                            "url": "http://example.com/api/endpoint1",
                        }
                    },
                    {
                        "name": "Endpoint 2",
                        "id" : "old-collection-id",
                        "request": {
                            "method": "POST",
                            "url": "http://example.com/api/endpoint2",
                        }
                    }
                ]
            }
        }

        new_schema = {
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
                            "url": "http://example.com/api/endpoint1",
                        }
                    },
                    {
                        "name": "Endpoint 3", # New endpoint
                        "id" : "new-collection-id",
                        "request": {
                            "method": "PUT",  # Method changed
                            "url": "http://example.com/api/endpoint3",  # URL changed
                        }
                    }
                ]
            }
        }

        # Create a SyncEnd instance and set the collection ID
        sync_end = SyncEnd(api_key="sample-api-key", collection_name="test_collection", trigger_interval=60,
                            slack_channel="test_channel", slack_token="sample-slack-token", webhook="sample-webhook",
                            channel_type="all", sender_email="example1@example.com", sender_pwd="example1",
                            recipient_email="example2@example.com")
        sync_end.collection_id = "new-collection-id"

        # Mock the 'open' function to return the old schema when reading
        print(json.dumps(old_schema))
        with patch("builtins.open", mock_open(read_data=json.dumps(old_schema))):
            difference = sync_end.compute_difference(new_schema)

        # Define the expected difference based on the provided old and new schemas
        expected_difference = [
            "Following end points are newly added in the collection :: \n\n"
            "\t1)  EndPoint Name: Endpoint 3\n"
            "\tURL: http://example.com/api/endpoint3\n"
            "\tRequest Method: PUT\n\n",

            "Following end points are deleted from the collection :: \n\n"
            "\t1)  EndPoint Name: Endpoint 2\n"
            "\tURL: http://example.com/api/endpoint2\n"
            "\tRequest Method: POST\n\n",

            "Following is the list of change in the existing end points ::\n\n"
            "\tNew name: Endpoint 3\nOld name: Endpoint 2\n"
            "\tNew URL: http://example.com/api/endpoint3\nOld URL: http://example.com/api/endpoint2\n"
            "\t New HTTP method: PUT\nOld HTTP method: POST\n"
        ]

        # Check if the computed difference matches the expected difference
        self.assertEqual(difference, expected_difference)

if __name__ == "__main__":
    unittest.main()
