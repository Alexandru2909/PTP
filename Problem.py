import json
import Place, Vehicle, Patient, Request, Instance
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
            for vh in self.vehicles:
                # for i in range(len(vh.getTimeWindow())):
                vh.history.append((vh.start, vh.getTimeWindow()[0]))
  

    def getPlaces(self):
        return self.places

    def getVehicles(self):
        return self.vehicles

    def getPatients(self):
        return self.patients
    
    def getRequests(self):
        for pat in self.patients:
            req = Request.Request(pat.start,pat.destination,pat.end,pat.load,pat.rdvTime,pat.rdvDuration,pat.category,pat.srvDuration)
            self.requests.append(req)
        
    def getBestRequest(self, requests):
        def minSlack(requests):
            ret_list = list()
            for request in requests:
                ret_list.append((self.distMatrix[request.startPlace][request.destPlace] + self.distMatrix[request.destPlace][request.returnPlace] + 4*request.embark)*request.placesVehicle)
            return ret_list

        minSlackList = minSlack(requests)
        return max(minSlackList)
    
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

    def orderReq(self):
        for i in range(len(self.requests)):
            for j in range(len(self.requests)):
                if self.requests[i].getReqTime() < self.requests[j].getReqTime():
                    a = self.requests[i]
                    self.requests[i] = self.requests[j]
                    self.requests[j] = a
        return self.requests
    
    def setActivityForward(self,inst,vehInd,reqInd):
        if inst.requsts[reqInd].category not in inst.vehicles[vehInd].canTake:
            return False
        vehAct = inst.vehicles[vehInd].getLastActivity()
        if inst.requests[reqInd].placesVehicle > inst.vehicles[vehInd].capacity - vehAct.load:
            return False
        total_time = self.distMatrix[vehAct.endPlace][inst.requests[reqInd].startPlace]
        total_time += inst.requests[reqInd].embark*2
        total_time += self.distMatrix[inst.requests[reqInd].startPlace][inst.requests[reqInd].endPlace]
        if vehAct.endTime+total_time > inst[vehInd].getTimeWindow()[1]:
            return False
        if inst.requests[reqInd].serviceBegin-total_time<inst.vehicles[vehInd].getTimeWindow()[0]:
            return False

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
        self.orderReq()
        initInst = Instance.Instance(self)
        # to be completed using subsearch



        




    # Nush ce sa fac cu astea o disparut activities Plox.
    # def check_vehicles(requests,activities):
    #     for i in range(len(requests)):
    #         for j in range(len(requests)):
    #             if i != j:
    #                 if (activities[i].forward.vehicle == activities[i].backward.vehicle == activities[j].forward.vehicle == activities[j].backward.vehicle):
    #                     if (activities[j].forward.start - activities[i].forward.start < activities[j].forward.start - activities[i].forward.start or activities[i].forward.start - activities[j].forward.start < activities[i].forward.start - activities[j].forward.start):
    #                         return False
    #                     if (activities[j].forward.start - activities[i].backward.end < activities[j].forward.end - activities[i].forward.start or activities[i].forward.start - activities[j].backward.end < activities[i].forward.end - activities[j].forward.start):
    #                         return False
    #                     if (activities[j].backward.end - activities[i].forward.start < activities[j].forward.start - activities[i].forward.end or activities[j].backward.end - activities[i].forward.start < activities[i].forward.start - activities[j].forward.end):
    #                         return False
    #                     if (activities[j].backward.end - activities[i].backward.end < activities[j].forward.end - activities[i].forward.end or activities[j].backward.end - activities[i].backward.end < activities[i].forward.end - activities[j].forward.end):
    #                         return False
    #     return True
    
    # def check_request(self, request, activity):
    #     if request.selected == 1:
    #         if activity.forward.execute != 1 and activity.backward.execute != 1:
    #             return False
    #     if (activity.forward.end > request.getReqTime()):
    #         return False
    #     if (activity.backward.start < request.getReqTime() + request.getReqDur()):
    #         return False
    #     if (request.category not in activity.forward.vehicle.canTake) or (request.category not in activity.backward.vehicle.canTake):
    #         return False
        # return True

    # def checkReq(self,inst,reqIndex,vehicle1,vehicle2):
    #     total_time_v1 = self.distMatrix[vehicle1.][inst.requests[reqIndex].startPlace]
    #     total_time_v1 += inst.requests[reqIndex].embark
    #     total_time_v1 += self.distMatrix[inst.requests[reqIndex].start][inst.requests[reqIndex].destPlace]
    #     total_time_v1 += inst.requests[reqIndex].embark
        # window
        # for win in vehicle1.getTimeWindows():