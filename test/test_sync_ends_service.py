import sys
import unittest
from unittest.mock import Mock, patch, mock_open
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))
from src.sync_ends_service import SyncEnd  # noqa: E402


class TestSyncEndsService(unittest.TestCase):
    def setUp(self):
        self.sync_end = SyncEnd(
            "SAM-Key-123fg", "test server", 9, "sample channel", "123ff"
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
                dirname(dirname(abspath(__file__))) + "/src/data/custom_id.txt"
            )
            mocked_file.assert_called_once_with(file_path, "w")
            mocked_file().write.assert_called_once_with(
                str(collection_schema["collection"]).replace("'", '"')
            )


if __name__ == "__main__":
    unittest.main()
