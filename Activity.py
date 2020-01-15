import datetime
class Activity:
    def __init__(self,startPlace,startTime,midPlace,midTime,endPlace,endTime,timeleft,requestInd,load):
        self.startPlace=startPlace
        self.startTime=startTime
        self.midPlace = midPlace
        self.midTime = midTime
        self.endPlace = endPlace
        self.endTime = endTime
        self.timeleft = timeleft
        self.requestIndex = requestInd
        self.load = load