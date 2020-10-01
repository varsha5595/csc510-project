

class EndPoint:

    def __init__(self, end_point_json):
        self.id = end_point_json['_postman_id']
        self.name = end_point_json['name']
        self.authentication = end_point_json['request'].get('auth')
        self.method = end_point_json['request']['method']
        self.header = end_point_json['request'].get('header')
        self.url = end_point_json['request']['url']['raw']
        self.query_parameters = end_point_json['request']['url'].get('query')

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_authentication(self):
        return self.authentication

    def get_method(self):
        return self.method

    def get_header(self):
        return self.header

    def get_url(self):
        return self.url

    def get_query_parameters(self):
        return self.query_parameters
