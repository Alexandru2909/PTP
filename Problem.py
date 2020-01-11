import json
import Place, Vehicle, Patient, Request, Activity

class Problem:
    places = list()
    vehicles = list()
    patients = list()
    activities = list()
    requests = list()
    def __init__(self, jsonFile):
        print("Json file is : " + jsonFile.split("/")[-1])
        with open(jsonFile) as json_file:
            data = json.load(json_file)
            self.maxWaitTime = data['maxWaitTime']
            self.sameVehicleBackWard = bool(data['sameVehicleBackward'])
            self.distMatrix = data['distMatrix']

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

