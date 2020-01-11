class Place:
    def __init__(self, id1, lat, long, category):
        """
        Parameters:
            “id” is the id of the location. It corresponds to its position in the list of locations.
            “lat” and “long” are the coordinates of the location.
            “category” is the category of the location. Its value can be 0 for a medical center, 1 for a vehicle depot and 2 for a patient location.
        """
        self.id = id1
        self.lat = lat
        self.long = long
        self.category = category