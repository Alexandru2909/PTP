import json
import Place, Vehicle, Patient, Request, Instance, Activity
import datetime

def convertTime(x):
    h,m=x.split('h')
    return datetime.timedelta(hours=int(h), minutes=int(m))


class Problem:
    places = list()
    vehicles = list()
    patients = list()
    requests = list()
    distMatrix = list()
    maxWaitTime = list()

    def __init__(self, jsonFile):
        print("Json file is : " + jsonFile.split("/")[-1])
        with open(jsonFile) as json_file:
            data = json.load(json_file)
            H, M = data['maxWaitTime'].split("h")
            self.maxWaitTime = datetime.timedelta(hours=int(H), minutes=int(M))
            self.sameVehicleBackWard = bool(data['sameVehicleBackward'])
            self.distMatrix = data['distMatrix']

            for i in range(len(self.distMatrix)):
                for j in range(len(self.distMatrix[i])):
                    self.distMatrix[i][j] = datetime.timedelta(minutes=self.distMatrix[i][j])

            for place in data['places']:
                self.places.append(Place.Place(place['id'], place['lat'], place['long'], place['category']))

            for vehicle in data['vehicles']:
                if len(vehicle["availability"]) > 1:
                    for i in range(len(vehicle["availability"])):
                        self.vehicles.append(Vehicle.Vehicle(vehicle["id"], vehicle["canTake"], vehicle["start"], vehicle["end"],
                                                        vehicle["capacity"], vehicle["availability"][i]))
                # print( vehicle["availability"],self.vehicles[-1].availability[0])

            for patient in data['patients']:
                self.patients.append(Patient.Patient(patient["id"], patient["category"],patient["load"],  patient["start"],
                                                patient["destination"], patient["end"], patient["rdvTime"], patient["rdvDuration"], patient["srvDuration"]))
            # for vh in self.vehicles:
            #     # for i in range(len(vh.getTimeWindow())):
            #     vh.history.append((vh.start, vh.getTimeWindow()[0]))
  

    def getPlaces(self):
        return self.places

    def getVehicles(self):
        return self.vehicles

    def getPatients(self):
        return self.patients
    
    def getRequests(self):
        for pat in self.patients:
            req = Request.Request(pat.id,pat.start,pat.destination,pat.end,pat.load,pat.rdvTime,pat.rdvDuration,pat.category,pat.srvDuration)
            self.requests.append(req)
        
    def getBestRequest(self, request, no_solutions):
        def minSlack(request):
                return (self.distMatrix[request.startPlace][request.destPlace] + self.distMatrix[request.destPlace][request.returnPlace] + 4*request.embark)*request.placesVehicle

        minSlack = minSlack(request)
        return minSlack.seconds/60 + no_solutions*10
    
    def getBestVehicle(self, request):
        max_weight = 0
        weight = 0
        timeToDeliver = 0
        best_vehicle = None
        for vehicle in self.vehicles:
            if request.category in vehicle.canTake:
                timeToArriveToPatient = self.distMatrix[vehicle.history[-1][0]][request.startPlace]
                timeOfArrivalToPatient = vehicle.history[-1][1] + timeToArriveToPatient
                if vehicle.capacity >= request.placesVehicle:
                    if vehicle.max_capacity > vehicle.capacity:
                        cantDeliver = False
                        for patient in vehicle.patients_list:
                            pass
                        weight += 10 * (vehicle.max_capacity - vehicle.capacity)

    # def getBestVeh(self,inst,reqID):
    #     start = inst.requests[reqID].serviceBegin
    #     start -= inst.requests[reqID].embark * 2
    #     start -= self.distMatrix[inst.requests[reqID].startPlace][inst.requests[reqID].destPlace]
    #     minTime = datetime.timedelta(hours=60)
    #     minId = -1
    #     for v in range(len(inst.vehicles)):
    #         if self.setActivityForward(inst,v,reqID):
    #             if self.distMatrix[inst.requests[reqID].vehicles[v].getLastActivity().endPlace][inst.requests[reqID].startPlace]<minTime:
    #                 minTime=self.distMatrix[inst.requests[reqID].vehicles[v].getLastActivity().endPlace][inst.requests[reqID].startPlace]
    #                 minId=v
    #     if minId==-1:
    #         return None
    #     else:
    #         return minId

    def orderReq(self):
        for i in range(len(self.requests)):
            for j in range(len(self.requests)):
                if self.requests[i].serviceBegin < self.requests[j].serviceBegin:
                    a = self.requests[i]
                    self.requests[i] = self.requests[j]
                    self.requests[j] = a
        # return self.requests
    
    def getSiblingActivities(self, activity, history):
        ret_list = list()
        for act in history:
            if len(ret_list) == 3:
                break
            if act.requestID == activity.requestID:
                ret_list.append(act)
        ret_list.sort(key=lambda act: act.time)

        return ret_list

    # TODO Dragos
    # def setActivityForward(self,inst,vehInd):
    #     if inst.requsts[reqInd].category not in inst.vehicles[vehInd].canTake:
    #         return False
    #     vehAct = inst.vehicles[vehInd].getLastActivity()
    #     if inst.requests[reqInd].placesVehicle > inst.vehicles[vehInd].capacity - vehAct.load:
    #         return False
    #     total_time = self.distMatrix[vehAct.endPlace][inst.requests[reqInd].startPlace]
    #     total_time += inst.requests[reqInd].embark*2
    #     total_time += self.distMatrix[inst.requests[reqInd].startPlace][inst.requests[reqInd].destPlace]
    #     if vehAct.endTime+total_time > inst[vehInd].getTimeWindow()[1]:
    #         return False
    #     if inst.requests[reqInd].serviceBegin-total_time<inst.vehicles[vehInd].getTimeWindow()[0]:
    #         return False
    #     return True
    # TODO Dragos
    # def setActivityBackward(self,inst,vehInd,reqInd):
    #     if inst.requsts[reqInd].category not in inst.vehicles[vehInd].canTake:
    #         return False
    #     vehAct = inst.vehicles[vehInd].getLastActivity()
    #     if inst.requests[reqInd].placesVehicle > inst.vehicles[vehInd].capacity - vehAct.load:
    #         return False
    #     total_time = self.distMatrix[vehAct.endPlace][inst.requests[reqInd].destPlace]
    #     total_time += inst.requests[reqInd].embark*2
    #     total_time += self.distMatrix[inst.requests[reqInd].destPlace][inst.requests[reqInd].endPlace]
    #     if vehAct.endTime+total_time > inst[vehInd].getTimeWindow()[1]:
    #         return False
    #     if inst.requests[reqInd].serviceBegin+inst.requests[reqInd].serviceDuration<inst.vehicles[vehInd].getTimeWindow()[0]:
    #         return False
    #     return True

    def subsearch(self,inst,initDepth,layersLeft):
        minH = 1000
        if layersLeft==0:
            pass
            # compare heuristic(inst,initDepth,slected=0) and heuristic(inst,initDepth,slected=1) and return min
            # insert here heuristic returning int
        else:
            pass
            # m1 = heuristic(inst,initDepth,slected=0)
            # m2 = heuristic(inst,initDepth,slected=1)
            # if m1<m2
            #   return m1
            # else
            #   return m2

    def search(self,depth):
        self.getRequests()
        self.orderReq()
        initInst = Instance.Instance(self)
        # to be completed using subsearch

    # TODO Alex
    def insertForward(self, inst, reqID, vehID):
        veh = inst.getVehbyID(vehID)
        req = inst.getReqbyID(reqID)
        pacient_time = req.serviceBegin - (req.embark + self.distMatrix[req.startPlace][req.destPlace])
        # starting_time = req.serviceBegin - (self.distMatrix[veh.getLastAct().place][req.startPlace] + self.distMatrix[req.embark]*2 + self.distMatrix[req.startPlace][req.destPlace])
        beforeAct = veh.getLastAct(pacient_time)
        starting_time = pacient_time-self.distMatrix[beforeAct.place][req.startPlace]-req.embark
        beforeAct = veh.getLastAct(starting_time)
        if beforeAct != veh.getLastAct(pacient_time):
            return False
        # startTime = inst.request[reqID].serviceBegin - (self.distMatrix[veh.getLastAct().place][inst.requests[reqID].startPlace] + self.distMatrix[inst.request[reqID].embark]*2 + self.distMatrix[inst.request[reqID].startPlace][inst.request[reqID].destPlace])
        startAct = Activity.Activity(beforeAct.place,starting_time,req.idReq,beforeAct.load,beforeAct.load)
        vehicleLoad = beforeAct.load+req.placesVehicle
        midAct = Activity.Activity(req.startPlace,pacient_time,req.idReq,vehicleLoad,beforeAct.load)
        beforeAct = veh.getLastAct(req.serviceBegin)
        endAct = Activity.Activity(req.destPlace,req.serviceBegin,req.idReq,beforeAct.load,vehicleLoad)        
        return True

    def insertBackward(self, inst, reqID, vehID):
        veh = inst.getVehbyID(vehID)
        req = inst.getReqbyID(reqID)
        pacient_time = req.serviceBegin + req.serviceDuration + req.embark
        # starting_time = req.serviceBegin - (self.distMatrix[veh.getLastAct().place][req.startPlace] + self.distMatrix[req.embark]*2 + self.distMatrix[req.startPlace][req.destPlace])
        beforeAct = veh.getLastAct(pacient_time)
        starting_time = pacient_time-self.distMatrix[beforeAct.place][req.startPlace]-req.embark
        beforeAct = veh.getLastAct(starting_time)
        if beforeAct != veh.getLastAct(pacient_time):
            return False
        # startTime = inst.request[reqID].serviceBegin - (self.distMatrix[veh.getLastAct().place][inst.requests[reqID].startPlace] + self.distMatrix[inst.request[reqID].embark]*2 + self.distMatrix[inst.request[reqID].startPlace][inst.request[reqID].destPlace])
        startAct = Activity.Activity(beforeAct.place,starting_time,req.idReq,beforeAct.load,beforeAct.load)
        vehicleLoad = beforeAct.load+req.placesVehicle
        midAct = Activity.Activity(req.destPlace,pacient_time,req.idReq,vehicleLoad,beforeAct.load)
        endTime = pacient_time + self.distMatrix[req.destPlace][req.returnPlace]+req.embark
        beforeAct = veh.getLastAct(endTime)
        endAct = Activity.Activity(req.returnPlace,endTime,req.idReq,beforeAct.load-req.placesVehicle,beforeAct.load)
        return True
        

# for testing
# x = Problem('Models/easy/PTP-RAND-1_8_4_32.json')
# x.getRequests()
# y = Instance.Instance(x)
# for i in x.requests:
    # print(i.startPlace,i.destPlace,i.placesVehicle,'id=',i.idReq,i.embark)
# print(x.getBestVeh(y,0))