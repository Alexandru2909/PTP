class Activity:
    def __init__(self, place, time, requestID, load, last_load):
        self.place = place
        self.time = time
        self.requestID = requestID
        self.load = load
        self.lastLoad = last_load
    def __eq__(self,other):
        if other == None:
            return False
        if self == None:
            return False
        if self.place==other.place and self.time == other.time and self.requestID == other.requestID and self.load==other.load and self.lastLoad == other.lastLoad:
            return True
        return False


