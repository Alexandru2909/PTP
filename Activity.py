class Activity:
    def __init__(self, place, time, requestID, load, last_load):
        self.place = place
        self.time = time
        self.requestID = requestID
        self.load = load
        self.lastLoad = last_load
    def __eq__(self,other):
        if self.place==other.place and self.time == other.time and self.requestID == other.requestID and self.load==other.load and self.lastLoad == other.lastLoad:
            return True
        return False
# import datetime
# class Activity:
#     def __init__(self,startPlace,startTime,midPlace,midTime,endPlace,endTime,timeleft,requestInd,load):
#         self.startPlace=startPlace
#         self.startTime=startTime
#         self.midPlace = midPlace
#         self.midTime = midTime
#         self.endPlace = endPlace
#         self.endTime = endTime
#         self.timeleft = timeleft
#         self.requestIndex = requestInd
#         self.load = load

