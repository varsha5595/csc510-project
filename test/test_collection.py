import unittest
from unittest.mock import Mock

from src.collection import Collection


class TestCollection(unittest.TestCase):
    def test_get_end_points(self):
        def compareObj(obj1, obj2):
            if (
                obj1.id == obj2.id
                and obj1.name == obj2.name
                and obj1.authentication == obj2.authentication
                and obj1.method == obj2.method
                and obj1.header == obj2.header
                and obj1.url == obj2.url
                and obj1.query_parameters == obj2.query_parameters
            ):
                return True
            return False

        json_dict = {
            "info": {
                "_postman_id": "1757f50c-60d1-4a48-a552-baa96d722e0f",
                "name": "Sample Server",
                "description": "This collection contains sample APIs that can be used to test the Sync Ends service.",  # noqa: E501
                "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",  # noqa: E501
            },
            "item": [
                {
                    "name": "Get employee details",
                    "_postman_id": "385f7848-62db-4435-b7cf-820c3e7e5097",
                    "protocolProfileBehavior": {"disableBodyPruning": True},
                    "request": {
                        "method": "POST",
                        "header": [],
                        "url": {
                            "raw": "http://127.0.0.1:5002/employee?emp_id=1",
                            "protocol": "http",
                            "host": ["127", "0", "0", "1"],
                            "port": "5002",
                            "path": ["employee"],
                            "query": [{"key": "emp_id", "value": "1"}],
                        },
                    },
                    "response": [],
                }
            ],
        }

        collection = Collection(json_dict)

        endpoint = Mock()
        endpoint.id = "385f7848-62db-4435-b7cf-820c3e7e5097"
        endpoint.name = "Get employee details"
        endpoint.authentication = None
        endpoint.method = "POST"
        endpoint.header = []
        endpoint.url = "http://127.0.0.1:5002/employee?emp_id=1"
        endpoint.query_parameters = [{"key": "emp_id", "value": "1"}]

        input_end_points = collection.get_end_points()[0]
        self.assertTrue(compareObj(endpoint, input_end_points))

    def test_remove_end_point(self):

        json_dict = {
            "info": {
                "_postman_id": "1757f50c-60d1-4a48-a552-baa96d722e0f",
                "name": "Sample Server",
                "description": "This collection contains sample APIs that can be used to test the Sync Ends service.",  # noqa: E501
                "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",  # noqa: E501
            },
            "item": [
                {
                    "name": "Get employee details",
                    "_postman_id": "385f7848-62db-4435-b7cf-820c3e7e5097",
                    "protocolProfileBehavior": {"disableBodyPruning": True},
                    "request": {
                        "method": "POST",
                        "header": [],
                        "url": {
                            "raw": "http://127.0.0.1:5002/employee?emp_id=1",
                            "protocol": "http",
                            "host": ["127", "0", "0", "1"],
                            "port": "5002",
                            "path": ["employee"],
                            "query": [{"key": "emp_id", "value": "1"}],
                        },
                    },
                    "response": [],
                }
            ],
        }

        collection = Collection(json_dict)

        end = collection.get_end_points()[0]
        collection.remove_end_point(end)
        self.assertEqual(len(collection.end_points), 0)


if __name__ == "__main__":
    unittest.main()
