import unittest
from src.end_point import EndPoint


class TestEndPoint(unittest.TestCase):
    def setUp(self):
        json_dict = {
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
        self.endPoint = EndPoint(json_dict)

    def tearDown(self):
        pass

    def test_get_id(self):
        self.assertEqual(
            self.endPoint.get_id(), "385f7848-62db-4435-b7cf-820c3e7e5097"
        )  # noqa: E501

    def test_get_name(self):
        self.assertEqual(self.endPoint.get_name(), "Get employee details")

    def test_get_authentication(self):
        self.assertIsNone(self.endPoint.get_authentication())

    def test_get_method(self):
        self.assertEqual(self.endPoint.get_method(), "POST")

    def test_get_header(self):
        self.assertEqual(self.endPoint.get_header(), [])

    def test_get_url(self):
        self.assertEqual(
            self.endPoint.get_url(), "http://127.0.0.1:5002/employee?emp_id=1"
        )

    def test_get_query_parameters(self):
        self.assertEqual(
            self.endPoint.get_query_parameters(),
            [{"key": "emp_id", "value": "1"}],
        )


if __name__ == "__main__":
    unittest.main()
