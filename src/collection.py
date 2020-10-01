from src.end_point import EndPoint


class Collection:

    def __init__(self, collection_json):
        self.end_points = [EndPoint(x) for x in collection_json["item"]]

    def get_end_points(self):
        return self.end_points
