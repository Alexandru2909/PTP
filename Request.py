import datetime

class Request:
    # Starting place of the patient linked to request
    startPlace = None
    # Place where the care is delivered for the patient of request
    destPlace = None
    # Number of places taken by the patient of request
    placesVehicle = None
    # Time at which the health care service begins for request
    serviceBegin = None
    # Time needed to deliver the care for the patient of request
    serviceDuration = None
    # Category of patient of request(wheelchair, without, etc.)
    category = None
    # Embark/Disembark time
    embark = None
    #If the request was selected (1) or not (0)
    selected = 0
    def __init__(self,start,dest,ret,places,servicebegin,servicedur,category,embarkdisembark):
        self.startPlace=start
        self.destPlace=dest
        self.placesVehicle=places
        self.returnPlace=ret
        self.serviceBegin=servicebegin
        self.serviceDuration=servicedur
        self.category=category
        self.embark=embarkdisembark

    def getReqTime(self):
        H, M = self.serviceBegin.split("h")
        return datetime.timedelta(hours=int(H), minutes=int(M))

    def getReqDur(self):
        H, M = self.serviceDuration.split("h")
        return datetime.timedelta(hours=int(H), minutes=int(M))

    def getEmbarkDisembark(self):
        H, M = self.embark.split("h")
        return datetime.timedelta(hours=int(H), minutes=int(M))
