class EndPoint:
    """
    A class to represent a EndPoint(API) in the code.

    Attributes
    ----------
        id : Id of Postman API/EndPoint
        name : Name of Postman API
        authentication : Authentication method of the API
        method : Method of API request (eg. GET, POST, etc.)
        header : header parameters in the request
        url : URL in the API request
        query_parameters : input query parameters
    """

    def __init__(self, end_point_json):
        self.id = end_point_json["_postman_id"]
        self.name = end_point_json["name"]
        self.authentication = end_point_json["request"].get("auth")
        self.method = end_point_json["request"]["method"]
        self.header = end_point_json["request"].get("header")
        self.url = end_point_json["request"]["url"]["raw"]
        self.query_parameters = end_point_json["request"]["url"].get("query")

    def get_id(self):
        """
        Get ID of the API
        """
        return self.id

    def get_name(self):
        """
        Get name of the API
        """
        return self.name

    def get_authentication(self):
        """
        Get authentication type of API
        """
        return self.authentication

    def get_method(self):
        """
        Get method of API request
        """
        return self.method

    def get_header(self):
        """
        Get header in the API request
        """
        return self.header

    def get_url(self):
        """
        Get url of the API request
        """
        return self.url

    def get_query_parameters(self):
        """
        Get query params of the API request
        """
        return self.query_parameters
