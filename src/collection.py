from src.end_point import EndPoint


class Collection:
    """
    A class to represent a Postman Collection in the code.

    Attributes
    ----------
        end_points : List of EndPoints (APIs) that are to be tested via Postman collection  # noqa: E501
    """

    def __init__(self, collection_json):
        self.end_points = [EndPoint(x) for x in collection_json["item"]]

    def get_end_points(self):
        """
        Returns the list of end points from the Collection object
        """
        return self.end_points

    def remove_end_point(self, end_point):
        """
        Removes the end point from the list of endpoints in the Collection object  # noqa: E501
        """
        self.end_points.remove(end_point)
