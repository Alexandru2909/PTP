import json
import Place, Vehicle, Patient, Request
import datetime
import copy

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

    class Instance:
        vehicles = None
        requests = None
        def __init__(self,problem):
            self.vehicles = copy.deepcopy(problem.vehicles)
            self.requests = copy.deepcopy(problem.requests)
        def copy(self,cop):
            self.vehicles = copy.deepcopy(cop.vehicles)
            self.requests = copy.deepcopy(cop.requests)


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
                self.vehicles.append(Vehicle.Vehicle(vehicle["id"], vehicle["canTake"], vehicle["start"], vehicle["end"],
                                                vehicle["capacity"], vehicle["availability"]))
                # print( vehicle["availability"],self.vehicles[-1].availability[0])

            for patient in data['patients']:
                self.patients.append(Patient.Patient(patient["id"], patient["category"],patient["load"],  patient["start"],
                                                patient["destination"], patient["end"], patient["rdvTime"], patient["rdvDuration"], patient["srvDuration"]))
            for vh in self.vehicles:
                for i in range(len(vh.getTimeWindows())):
                    vh.history.append((vh.start, vh.getTimeWindows()[i][0]))
  

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
        
    def getBestRequest(requests):
        def minSlack(requests):
            ret_list = list()
            for request in requests:
                pass

    def orderReq(self):
        for i in range(len(self.requests)):
            for j in range(len(self.requests)):
                if self.requests[i].getReqTime() < self.requests[j].getReqTime():
                    a = self.requests[i]
                    self.requests[i] = self.requests[j]
                    self.requests[j] = a
        return self.requests
    

    # Nush ce sa fac cu astea o disparut activities Plox.
    def check_vehicles(requests,activities):
        for i in range(len(requests)):
            for j in range(len(requests)):
                if i != j:
                    if (activities[i].forward.vehicle == activities[i].backward.vehicle == activities[j].forward.vehicle == activities[j].backward.vehicle):
                        if (activities[j].forward.start - activities[i].forward.start < activities[j].forward.start - activities[i].forward.start or activities[i].forward.start - activities[j].forward.start < activities[i].forward.start - activities[j].forward.start):
                            return False
                        if (activities[j].forward.start - activities[i].backward.end < activities[j].forward.end - activities[i].forward.start or activities[i].forward.start - activities[j].backward.end < activities[i].forward.end - activities[j].forward.start):
                            return False
                        if (activities[j].backward.end - activities[i].forward.start < activities[j].forward.start - activities[i].forward.end or activities[j].backward.end - activities[i].forward.start < activities[i].forward.start - activities[j].forward.end):
                            return False
                        if (activities[j].backward.end - activities[i].backward.end < activities[j].forward.end - activities[i].forward.end or activities[j].backward.end - activities[i].backward.end < activities[i].forward.end - activities[j].forward.end):
                            return False
        return True
    
    def check_request(self, request, activity):
        if request.selected == 1:
            if activity.forward.execute != 1 and activity.backward.execute != 1:
                return False
        if (activity.forward.end > request.getReqTime()):
            return False
        if (activity.backward.start < request.getReqTime() + request.getReqDur()):
            return False
        if (request.category not in activity.forward.vehicle.canTake) or (request.category not in activity.backward.vehicle.canTake):
            return False
        return True

    # def checkReq(self,inst,reqIndex,vehicle1,vehicle2):
    #     total_time_v1 = self.distMatrix[vehicle1.][inst.requests[reqIndex].startPlace]
    #     total_time_v1 += inst.requests[reqIndex].embark
    #     total_time_v1 += self.distMatrix[inst.requests[reqIndex].start][inst.requests[reqIndex].destPlace]
    #     total_time_v1 += inst.requests[reqIndex].embark
        # window
        # for win in vehicle1.getTimeWindows():





# x = Problem('Models/hard/PTP-RAND-3_112_6_112.json')
    
    
            
        

