class Vehicle:
    def __init__(self, id1, canTake, start, end, capacity, availability):
        """
        Parameters:
            “id” which contains the id of the vehicle.
            “canTake” which is a set of categories of patients that the vehicle can take.
            “start” and “end” which are the ids of the starting and ending depots of the vehicle. A -1 value indicates that the vehicle has no depot.
            “capacity” which is the capacity of the vehicle.
            “availability” which is a set of time windows when the vehicle is available. Each time window is encoded by a string having the following format: “HHhMM:HHhMM”.
        """
        self.id = id1
        self.canTake = canTake
        self.start = start
        self.end = end
        self.capacity = capacity
        self.availability = availability