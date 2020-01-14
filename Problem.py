import json
import Place, Vehicle, Patient, Request, Activity
import datetime

class Problem:
    places = list()
    vehicles = list()
    patients = list()
    activities = list()
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
                for j in range(i):
                    self.distMatrix[i][j] = datetime.timedelta(minutes=self.distMatrix[i][j])

            for place in data['places']:
                self.places.append(Place.Place(place['id'], place['lat'], place['long'], place['category']))

            for vehicle in data['vehicles']:
                self.vehicles.append(Vehicle.Vehicle(vehicle["id"], vehicle["canTake"], vehicle["start"], vehicle["end"],
                                                vehicle["capacity"], vehicle["availability"]))

            for patient in data['patients']:
                self.patients.append(Patient.Patient(patient["id"], patient["category"],patient["load"],  patient["start"],
                                                patient["destination"], patient["end"], patient["rdvTime"], patient["rdvDuration"], patient["srvDuration"]))

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
    def getActivites(self):
        for p in self.patients:
            # possible bug
            addedTime=''
            for ind in range(len(p.rdvTime)):
                addedTime += str(int(p.rdvTime[ind]) + int(p.rdvDuration[ind]))
            act=Activity.Activity(p.start,p.rdvTime,0,0,addedTime,p.end,0,0)
            self.activities.append(act)
        
    
    def check_request(self, request, vehicle):
        if request.category not in vehicle.canTake:
            return False
        elif vehicle.capacity < request.load:
            return False
        for time in vehicle.getTimeWindows():
            
            
        

