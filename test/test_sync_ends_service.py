import sys
import unittest
from unittest.mock import Mock
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))


class TestParser(unittest.TestCase):
    def setUp(self):      
        self.end_point_list = []
        endpoint = Mock()
        endpoint.id = "385f7848-62db-4435-b7cf-820c3e7e5097"
        endpoint.name = "Endpoint 1"
        endpoint.authentication = None
        endpoint.method = "POST"
        endpoint.header = []
        endpoint.url = "http://127.0.0.1:5002/endpoint?ep_id=1"
        endpoint.query_parameters = [{"key": "ep_id", "value": "1"}]
        self.end_point_list.append(endpoint)
        endpoint.id = "3234dt48-62db-4435-b7cf-820c3e7e5097"
        endpoint.name = "Endpoint 2"
        endpoint.authentication = None
        endpoint.method = "POST"
        endpoint.header = []
        endpoint.url = "http://127.0.0.1:5003/endpoint?ep_id=2"
        endpoint.query_parameters = [{"key": "ep_id", "value": "2"}]
        self.end_point_list.append(endpoint)

    def test_get_newly_added_message(self):
        title = "Following end points are newly added in the collection :: \n\n"
        output = (
            "\t"
            + str(1)
            + ")  "
            + "Endpoint 1"
            + "\n"
            + "\t"
            + "URL: "
            + "http://127.0.0.1:5002/endpoint?ep_id=1"
            + "\n"
            + "\t"
            + "Request Method: "
            + "POST"
            + "\n\n"
            )


if __name__ == "__main__":
    unittest.main()