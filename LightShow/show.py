from collections import deque

class Show():

    internalTime = 0

    #Show is just a list of effects, sorted by start time
    #They can be layered as well


    currentEffects = [] #sorted by layer (AKA render order)
    upcomingEffects = deque() # sorted by start time

    def __init__(self):
        pass

    def start(self, pixels, NUM_PIXELS):
        self.internalTime = 0
        pass

    def render(self, pixels, NUM_PIXELS, ms_later):
        pass
        #if self.internalTime > upcomingEffects[0]:
            
            #append top upcoming effect to current effects in correct order
            #check again to see if any more effects have started

        #render in order of layer
            
        #a method for rendering a given moment, based on the start times, end times, and layering