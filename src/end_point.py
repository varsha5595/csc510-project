

class EndPoint:

    def __init__(self, end_point_json):
        self.id = end_point_json['_postman_id']
        self.name = end_point_json['name']
        self.authentication = end_point_json['request'].get('auth')
        self.method = end_point_json['request']['method']
        self.header = end_point_json['request'].get('header')
        self.url = end_point_json['request']['url']['raw']
        self.query_parameters = end_point_json['request']['url'].get('query')
