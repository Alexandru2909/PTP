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
        # return datetime.datetime.strptime(serviceBegin, '%Hh%M').time()
        return datetime.timedelta(hours=int(self.serviceBegin.split("h")[0], minutes=int(self.serviceBegin.split("h")[1])))

    def getReqDur(self):
        # return datetime.datetime.strptime(self.serviceDuration, '%Hh%M').time()
        return datetime.timedelta(hours=int(self.serviceDuration.split("h")[0], minutes=int(self.serviceDuration.split("h")[1])))

    def getEmbarkDisembark(self):
        # return datetime.datetime.strptime(self.embark, '%Hh%M').time()
        return datetime.timedelta(hours=int(self.embark.split("h")[0], minutes=int(self.embark.split("h")[1])))