import datetime

class Request:
    class Variable:
        start=None
        end= None
        duration = None
        execute = None
        def set(self,s,e,x,v):
            self.start=s
            self.end=e
            self.duration=self.start-self.end
            self.execute=x
            self.vehicle=v
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
    forward = Variable()
    backward = Variable()
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

    def setActivity(self,start1,end1,execute1,vehicle1,start2,end2,execute2,vehicle2):
        self.forward.set(datetime.timedelta(hours=int(start1.split("h")[0], minutes=int(start1.split("h")[1]))),datetime.timedelta(hours=int(end1.split("h")[0], minutes=int(end1.split("h")[1]))),execute1,vehicle1)
        self.forward.set(datetime.timedelta(hours=int(start2.split("h")[0], minutes=int(start2.split("h")[1]))),datetime.timedelta(hours=int(end2.split("h")[0], minutes=int(end2.split("h")[1]))),execute2,vehicle2)