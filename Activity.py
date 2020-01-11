class Activity:
    class Variable:
        start=0.0
        end=0.1
        duration = 0.1
        execute = 0
        # The domain of the vehicle's selection variables
        vehicle = 0
        def set(self,s,e,x,v):
            self.start=s
            self.end=e
            self.duration=self.start-self.end
            self.execute=x
            self.vehicle=v
    forward = Variable()
    backward = Variable()
    def buildActivity(self,s1,e1,x1,v1,s2,e2,x2,v2):
        self.forward.set(s1,e1,x1,v1)
        self.backward.set(s2,e2,x2,v2)
            