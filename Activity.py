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


class Activity:
    def __init__(self, place, time, requestID, load):
        self.place = place
        self.time = time
        self.requestID = requestID
        self.load = load