import datetime 

class Vehicle:
    def __init__(self, id1, canTake, start, end, capacity, availability):
        """
        Parameters:
            “id” which contains the id of the vehicle.
            “canTake” which is a set of categories of patients that the vehicle can take.
            “start” and “end” which are the ids of the starting and ending depots of the vehicle. A -1 value indicates that the vehicle has no depot.
            “max_capacity” which is the capacity of the vehicle.
            “capacity” which is the remaining capacity of the vehicle.
            “availability” which is a set of time windows when the vehicle is available. Each time window is encoded by a string having the following format: “HHhMM:HHhMM”.
            "history" list of tuples: location-time
        """
        self.id = id1
        self.canTake = canTake
        self.start = start
        self.end = end
        self.max_capacity = capacity
        self.capacity = capacity
        self.availability = availability
        self.history = list()

    def getLastActivity(self):
        return self.history[-1]

    def setActivity(self,act):
        self.history.append(act)
        self.history.sort(key=lambda x:x.startTime)
    
    def deleteActivity(self,act):
        self.history.remove(act)

    def __eq__(self,other):
        return self.id == other.id and self.canTake == other.canTake and self.start == other.start and self.end == other.end and self.capacity == other.capacity and self.availability == other.availability

    def getTimeWindow(self):
        # windows = []
        # for it in self.availability:
        start, end = self.availability.split(":")
        startH, startM = start.split("h")
        endH, endM = end.split("h")
        st = datetime.timedelta(hours=int(startH), minutes=int(startM))
        en = datetime.timedelta(hours=int(endH), minutes=int(endM))
        # windows.append((st, en))
        return (st, en)
