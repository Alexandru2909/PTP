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
    def __init__(self,start1,end1,execute1,vehicle1,start2,end2,execute2,vehicle2):
        self.forward.set(start1,end1,execute1,vehicle1)
        self.backward.set(start2,end2,execute2,vehicle2)
            