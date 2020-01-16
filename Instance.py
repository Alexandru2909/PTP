import copy
class Instance:
    vehicles = None
    requests = None
    def __init__(self,problem):
        self.vehicles = copy.deepcopy(problem.vehicles)
        self.requests = copy.deepcopy(problem.requests)
    def copy(self,cop):
        self.vehicles = copy.deepcopy(cop.vehicles)
        self.requests = copy.deepcopy(cop.requests)
    def getReqbyID(self,reqID):
        for i in self.requests:
            if i.idReq == reqID:
                return i
    def getVehbyID(self,vehID):
        for i in self.vehicles:
            if i.id == vehID:
                return i