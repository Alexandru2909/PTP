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
    
    def getSortedActivities(self, history):
        ret_list = list()
        for act in history:
            ret_list.append(act)
        ret_list.sort(key=lambda act: act.time)
        return ret_list

    def reqTime(self, inst, vehID, reqID, f_b):
        found = 0
        searching = False
        history = getSortedActivities(inst.vehicles[vehID].history) 
        for i in history:
            if searching == True:
                total_time += self.distMatrix[history[i].place][history[i+1].place]
                if history[i].lastLoad != history[i].load:
                    total_time += inst.requests[history[i].requestID].embark
            if i.requestID == reqID:
                found += 1
                if found == 1 and f_b == 0:
                    searching = True
                    total_time = self.distMatrix[history[i].place][history[i+1].place]
                elif found == 3 and f_b == 0:
                    return total_time
                elif found == 4:
                    searching=True
                    total_time = self.distMatrix[history[i].place][history[i+1].place]
                elif found == 6:
                    return total_time

    # TODO Dragos
    def checkVehicle(self,inst,vehID):
        total_load = 0
        vehInd = 0
        for i in range(len(inst.vehicles)):
            if inst.vehicles[i].id == vehInd:
                vehInd = i
                break
        for act in inst.vehicles[vehInd].history:
            for req in inst.requests:
                if act.requestID == req.idReq:
                    if req.category not in inst.vehicles[vehInd].canTake:
                        return False
                    total_load += act.load
        if inst.vehicles[vehInd].canTake * 3 < total_load:
            return False
        actvts = self.getSortedActivities(init.vehicles[vehInd].history)
        for act1 in actvts:
            for act2 in actvts:
                if act1.time == act2.time and act1.place != act2.place:
                    return False
        total_time = datetime.timedelta(0)
        for i in range(1, len(actvts)):
            if self.distMatrix[actvts[i-1]][actvts[i]] > actvts[i].time - actvts[i-1].time:
                return False
            if actvts[i].load != actvts[i].lastLoad:
                for j in range(len(inst.requests)):
                    if req.idReq == actvts[j].requestID:
                        total_time += inst.requests[j].embark
                        break
            total_time += self.distMatrix[actvts[i-1]][actvts[i]]
        if total_time > inst.vehicles[vehInd].getTimeWindow()[1] - inst.vehicles[vehInd].getTimeWindow()[0]:
            return False
        
        d = dict()
        for i in actvts:
            if i.requestID not in d.keys():
                d[i.requestID]=0
                if self.reqTime(inst,vehID,i.requestId,0) > self.maxWaitTime:
                    return False
            else:
                d[i.requestID]+=1
            if d[i.requestID]==4:
                if self.reqTime(inst,vehID,i.requestId,1) > self.maxWaitTime:
                    return False
        return True
   

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
    # def insertForward(self, inst, reqID, vehID):
    #     start = Activity.Activity(inst.vehicle[vehID].history[-1][0])
    #     startPlace = inst.vehicle[vehID].history[-1][0]
    #     startTime = inst.request[reqID].serviceBegin - (self.distMatrix[startPlace][inst.requests[reqID].startPlace] + self.distMatrix[inst.request[reqID].embark]*2 + self.distMatrix[inst.request[reqID].startPlace][inst.request[reqID].destPlace])
    #     midPlace = inst.request[reqID].startPlace
    #     midTime = inst.request[reqID].serviceBegin - (self.distMatrix[inst.request[reqID].embark]*2 + self.distMatrix[inst.request[reqID].startPlace][inst.request[reqID].destPlace])
    #     endPlace = inst.request[reqID].destPlace
    #     endTime = inst.request[reqID].serviceBegin
    #     timeleft = inst.request[reqID].serviceBegin - endTime
    #     requestIndex = reqID
    #     load = inst.request[reqID].placesVehicle
    #     timeSurplus = self.maxWaitTime - (inst.requests[reqID].serviceBegin - startTime)
        
    #     act = Activity.Activity(startPlace, startTime, midPlace, midTime, endPlace, endTime, timeleft, requestIndex, load)
    #     inst.vehicle[vehID].setActivity(act)
        
    #     return inst

    # def insertBackward(self, inst, reqID, vehID):
    #     startPlace = inst.vehicle[vehID].history[-1][0]
    #     startTime = (inst.request[reqID].serviceBegin + inst.request[reqID].serviceDuration) - self.distMatrix[inst.vehicle[vehID].history[-1][0]][inst.request[reqID].destPlace]
    #     midPlace = inst.request[reqID].destPlace
    #     midTime = inst.request[reqID].serviceBegin + inst.request[reqID].serviceDuration + inst.request[reqID].embark*2
    #     endPlace = inst.request[reqID].returnPlace
    #     endTime = inst.request[reqID].serviceDuration + self.distMatrix[inst.request[reqID].destPlace][inst.request[reqID].startPlace]
    #     timeleft = midTime - endTime
    #     requestIndex = reqID
    #     load = inst.request[reqID].placesVehicle
    #     timeSurplus = self.maxWaitTime - (inst.requests[reqID].serviceBegin - startTime)
        
        
    #     act = Activity.Activity(startPlace, startTime, midPlace, midTime, endPlace, endTime, timeleft, requestIndex, load)
    #     inst.vehicle[vehID].setActivity(act)
    #     return inst

# for testing
# x = Problem('Models/easy/PTP-RAND-1_8_4_32.json')
# x.getRequests()
# y = Instance.Instance(x)
# for i in x.requests:
    # print(i.startPlace,i.destPlace,i.placesVehicle,'id=',i.idReq,i.embark)
# print(x.getBestVeh(y,0))