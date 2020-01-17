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
    maxWaitTime = None

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
    
    def getBestVehicle(self, request, inst):
        max_weight_forward = 0
        max_weight_backward = 0
        best_vehicle_forward = None
        best_vehicle_backward = None
        for vehicle in self.vehicles:
            # forward
            weight = 0
            test_instance = Instance.Instance(inst)
            isInsertValid = self.insertForward(test_instance, request.idReq, vehicle.id)
            isVehicleValid = self.checkVehicle(test_instance, vehicle.id)
            pacient_time = request.serviceBegin - (request.embark + self.distMatrix[request.startPlace][request.destPlace])
            # starting_time = req.serviceBegin - (self.distMatrix[veh.getLastAct().place][req.startPlace] + self.distMatrix[req.embark]*2 + self.distMatrix[req.startPlace][req.destPlace])
            beforeAct = vehicle.getLastAct(pacient_time)
            if isInsertValid and isVehicleValid:
                weight += 10 * (vehicle.max_capacity - beforeAct.load)
                # vehicleLastLocation = vehicle.getLastAct(request.serviceBegin).place
                timeToDeliver = self.reqTime(test_instance, vehicle.id, request.idReq, 0)
                weight += timeToDeliver.seconds/60

                if weight > max_weight_forward:
                    max_weight_forward = weight
                    best_vehicle_forward = vehicle

            # backward
            weight = 0
            test_instance = Instance.Instance(inst)
            isInsertValid = self.insertBackward(test_instance, request.idReq, vehicle.id)
            isVehicleValid = self.checkVehicle(test_instance, vehicle.id)
            pacient_time = request.serviceBegin + request.serviceDuration + request.embark + self.distMatrix[request.destPlace][request.returnPlace]
            # starting_time = req.serviceBegin - (self.distMatrix[veh.getLastAct().place][req.startPlace] + self.distMatrix[req.embark]*2 + self.distMatrix[req.startPlace][req.destPlace])
            beforeAct = vehicle.getLastAct(pacient_time)
            if isInsertValid and isVehicleValid:
                weight += 10 * (vehicle.max_capacity - beforeAct.load)
                # vehicleLastLocation = vehicle.getLastAct(request.serviceBegin + request.serviceDuration).place
                timeToDeliver = self.reqTime(test_instance, vehicle.id, request.idReq, 0)
                weight += timeToDeliver.seconds/60

                if weight > max_weight_backward:
                    max_weight_backward = weight
                    best_vehicle_backward = vehicle
                
        if best_vehicle_backward == None or best_vehicle_forward == None:
            return None
        return (best_vehicle_forward.id, best_vehicle_backward.id)
    
    def getSortedActivities(self, history):
        return sorted(history, key=lambda act: act.time)

    def reqTime(self, inst, vehID, reqID, f_b):
        found = 0
        searching = False
        history = self.getSortedActivities(inst.getVehbyID(vehID).history) 
        for i in range(len(history)):
            if history[i].requestID == reqID:
                found += 1
                if found == 1 and f_b == 0:
                    searching = True
                    total_time = datetime.timedelta(0)
                elif found == 3 and f_b == 0:
                    return total_time
                elif found == 4:
                    searching=True
                    total_time = datetime.timedelta(0)
                elif found == 6:
                    return total_time
            if searching == True:
                total_time += self.distMatrix[history[i].place][history[i+1].place]
                if history[i].lastLoad != history[i].load:
                    total_time += inst.getReqbyID(history[i].requestID).embark

    # TODO Dragos
    def checkVehicle(self,inst,vehID):
        vehInd = 0
        for i in range(len(inst.vehicles)):
            if inst.vehicles[i].id == vehID:
                vehInd = i
                break
        for act in inst.vehicles[vehInd].history:
            for req in inst.requests:
                if act.requestID == req.idReq:
                    if req.category not in inst.vehicles[vehInd].canTake:
                        return False
            if inst.vehicles[vehInd].max_capacity < req.placesVehicle:
                return False
        actvts = self.getSortedActivities(inst.vehicles[vehInd].history)
        for act1 in actvts:
            for act2 in actvts:
                if act1.time == act2.time and act1.place != act2.place:
                    return False
        total_time = datetime.timedelta(0)
        for i in range(1, len(actvts)):
            # print(i,self.distMatrix[actvts[i-1].place][actvts[i].place],(actvts[i].time - actvts[i-1].time))
            if self.distMatrix[actvts[i-1].place][actvts[i].place] > (actvts[i].time - actvts[i-1].time):
                return False
        d = dict()
        for i in actvts:
            if i.requestID not in d.keys():
                d[i.requestID]=1
                total_time = self.reqTime(inst,vehID,i.requestID,0)
                if self.reqTime(inst,vehID,i.requestID,0) > self.maxWaitTime:
                    return False
                checkedWindow=False
                for j in inst.getVehbyID(vehID).getTimeWindow():
                    if i.time>j[0] and i.time+total_time<j[1]:
                        checkedWindow=True
                return checkedWindow
            else:
                d[i.requestID]+=1
            if d[i.requestID]==4:
                if self.reqTime(inst,vehID,i.requestID,1) > self.maxWaitTime:
                    return False
        return True
   

    def subsearch(self,inst,initDepth,layersLeft):
        print('     ',initDepth,layersLeft)
        number_reqs = 0
        for i in inst.requests:
            if i.selected==1:
                number_reqs+=1
        if layersLeft==0:
            h1 = self.getBestRequest(inst.requests[initDepth],number_reqs) 
            copyInst = Instance.Instance(inst)
            copyInst.requests[initDepth].selected=1
            v = self.getBestVehicle(copyInst.requests[initDepth],copyInst)
            if v==None:
                return h1
            self.insertForward(copyInst,copyInst.requests[initDepth].idReq,v[0])
            self.insertBackward(copyInst,copyInst.requests[initDepth].idReq,v[1])
            h2 = self.getBestRequest(inst.requests[initDepth],number_reqs)
            return max([h1,h2])
            # compare heuristic(inst,initDepth,slected=0) and heuristic(inst,initDepth,slected=1) and return min
            # insert here heuristic returning int
        else:
            h1 = self.subsearch(inst,initDepth+1,0)
            copyInst = Instance.Instance(inst)
            copyInst.requests[initDepth].selected=1
            v = self.getBestVehicle(copyInst.requests[initDepth],copyInst)
            if v==None:
                return h1
            self.insertForward(copyInst,copyInst.requests[initDepth].idReq,v[0])
            self.insertBackward(copyInst,copyInst.requests[initDepth].idReq,v[1])
            m2 = self.subsearch(copyInst,initDepth+1,layersLeft-1)
            if h1<m2:
                return m2
            m1 = self.subsearch(inst,initDepth+1,layersLeft-1)
            return max([m1,m2])

    def search(self,depth):
        self.getRequests()
        self.requests.sort(key = lambda x: x.serviceBegin)
        initInst = Instance.Instance(self)
        initInst.requests.sort(key = lambda x: x.serviceBegin)
        for i in range(len(initInst.requests)):
            # copyInst.requests[i].selected=0
            if i+depth>len(initInst.requests)-1:
                depth = len(initInst.requests)-i-1
            print(i,'/',len(initInst.requests))
            h2 = self.subsearch(initInst,i,depth)
            copyInst = Instance.Instance(initInst)
            copyInst.requests[i].selected=1
            v = self.getBestVehicle(copyInst.requests[i],copyInst)
            if v==None:
                continue
            self.insertForward(copyInst,copyInst.requests[i].idReq,v[0])
            self.insertBackward(copyInst,copyInst.requests[i].idReq,v[1])
            h1 = self.subsearch(copyInst,i,depth)
            if h1>h2:
                initInst.copy(copyInst)
        return initInst

    def insertForward(self, inst, reqID, vehID):
        veh = inst.getVehbyID(vehID)
        req = inst.getReqbyID(reqID)
        pacient_time = req.serviceBegin - (req.embark + self.distMatrix[req.startPlace][req.destPlace])
        beforeAct1 = veh.getLastAct(pacient_time)
        starting_time = pacient_time-self.distMatrix[beforeAct1.place][req.startPlace]-req.embark
        beforeAct = veh.getLastAct(starting_time)
        if beforeAct1 != beforeAct:
            return False
        startAct = Activity.Activity(beforeAct.place,starting_time,req.idReq,beforeAct.load,beforeAct.load)
        vehicleLoad = beforeAct.load+req.placesVehicle
        midAct = Activity.Activity(req.startPlace,pacient_time,req.idReq,vehicleLoad,beforeAct.load)
        beforeAct = veh.getLastAct(req.serviceBegin)
        endAct = Activity.Activity(req.destPlace,req.serviceBegin,req.idReq,beforeAct.load,vehicleLoad)        
        inst.getVehbyID(vehID).history.append(startAct)
        inst.getVehbyID(vehID).history.append(midAct)
        inst.getVehbyID(vehID).history.append(endAct)
        return True

    def insertBackward(self, inst, reqID, vehID):
        veh = inst.getVehbyID(vehID)
        req = inst.getReqbyID(reqID)
        pacient_time = req.serviceBegin + req.serviceDuration + req.embark
        beforeAct = veh.getLastAct(pacient_time)
        starting_time = pacient_time-self.distMatrix[beforeAct.place][req.destPlace]-req.embark
        beforeAct = veh.getLastAct(starting_time)
        if beforeAct != veh.getLastAct(pacient_time):
            return False
        startAct = Activity.Activity(beforeAct.place,starting_time,req.idReq,beforeAct.load,beforeAct.load)
        vehicleLoad = beforeAct.load+req.placesVehicle
        inst.getVehbyID(vehID).history.append(startAct)
        midAct = Activity.Activity(req.destPlace,pacient_time,req.idReq,vehicleLoad,beforeAct.load)
        inst.getVehbyID(vehID).history.append(midAct)
        if req.returnPlace==-1:
            endTime = pacient_time + self.distMatrix[req.destPlace][req.destPlace]+req.embark
        else:
            endTime = pacient_time + self.distMatrix[req.destPlace][req.returnPlace]+req.embark
        beforeAct = veh.getLastAct(endTime)
        if req.returnPlace==-1:
            endAct = Activity.Activity(req.destPlace,endTime,req.idReq,beforeAct.load-req.placesVehicle,beforeAct.load)
        else:
            endAct = Activity.Activity(req.returnPlace,endTime,req.idReq,beforeAct.load-req.placesVehicle,beforeAct.load)
        inst.getVehbyID(vehID).history.append(endAct)
        return True
        

