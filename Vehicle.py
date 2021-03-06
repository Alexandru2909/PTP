import datetime, Activity

class Vehicle:
    def __init__(self, id1, canTake, start, end, capacity, availability):
        """
        Parameters:
            “id” which contains the id of the vehicle.
            “canTake” which is a set of categories of patients that the vehicle can take.
            “start” and “end” which are the ids of the starting and ending depots of the vehicle. A -1 value indicates that the vehicle has no depot.
            “max_capacity” which is the capacity of the vehicle.
            “availability” which is a set of time windows when the vehicle is available. Each time window is encoded by a string having the following format: “HHhMM:HHhMM”.
            "history" list of activities
        """
        self.id = id1
        self.canTake = canTake
        self.start = start
        self.end = end
        self.max_capacity = capacity
        self.availability = availability
        self.history = list()

    def setActivity(self,act):
        self.history.append(act)
    
    def deleteActivity(self,act):
        self.history.remove(act)

    def __eq__(self,other):
        if other == None:
            return False
        if self == None:
            return False
        return self.id == other.id and self.canTake == other.canTake and self.start == other.start and self.end == other.end and self.max_capacity == other.max_capacity and self.availability == other.availability

    def getLastAct(self,time):
        history_sorted = sorted(self.history,key=lambda y:y.time)
        i = 0
        if len(history_sorted)==0:
            return Activity.Activity(self.start,self.getTimeWindow()[0],-1,0,0)
        while i<len(history_sorted) and history_sorted[i].time<time :
            i+=1
        if i==len(history_sorted):
            return history_sorted[-1]
        return history_sorted[i-1]

    def getTimeWindow(self):
        windows = []
        for it in self.availability:
            start, end = it.split(":")
            startH, startM = start.split("h")
            endH, endM = end.split("h")
            st = datetime.timedelta(hours=int(startH), minutes=int(startM))
            en = datetime.timedelta(hours=int(endH), minutes=int(endM))
            windows.append((st, en))
        return windows
