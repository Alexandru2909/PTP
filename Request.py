class Request:
    # Starting place of the patient linked to request
    start = 0
    # Place where the care is delivered for the patient of request
    dest = 0
    # Return place of the patient linked to request
    ret = 0
    # Number of places taken by the patient of request
    l = 0
    # Time at which the health care service begins for request
    u = 0
    # Time needed to deliver the care for the patient of request
    d = 0
    # Maximum travel time of the patient linked to request
    p = 0
    # Category of patient of request(wheelchair, without, etc.)
    c = 0
    def set(self,s,d1,r,l,u,d2,p,c):
        self.start=s
        self.dest=d1
        self.ret=r
        self.l=l
        self.u=u
        self.d=d2
        self.p=p
        self.c=c
        