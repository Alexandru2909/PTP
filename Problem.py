import json
import Place, Vehicle, Patient

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
    
    # def getRequests(self):
    #     for pat in self.patients:

