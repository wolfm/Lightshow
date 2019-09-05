from collections import deque

class Show():

    internalTime = 0

    #Show is just a list of effects, sorted by start time
    #They can be layered as well


    currentEffects = [] #sorted by layer (AKA render order)
    upcomingEffects = deque() # sorted by start time
    activeLayers = []

    def __init__(self):
        pass

    def start(self, pixels, NUM_PIXELS):
        self.internalTime = 0
        pass

    def render(self, pixels, NUM_PIXELS, ms_later):
        
        #For all effects that are set to start now
        while self.internalTime > self.upcomingEffects[0].startTime:
            
            for i in range(0, len(self.currentEffects)):
                if self.upcomingEffects[0].layer <= self.currentEffects[i].layer:
                    self.currentEffects.insert(i+1, self.currentEffects[i])
                    break
        