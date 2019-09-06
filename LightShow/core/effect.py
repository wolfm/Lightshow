import abc

class Effect:

    # a superclass for all effects

    @abc.abstractmethod
    def __init__(self, startTime, bpm, properties = {}):
        pass

    @abc.abstractmethod
    def start(self, pixels, num_pixels):
        #set the initial frame of the effect
        pass

    @abc.abstractmethod
    def render(self, pixels, num_pixels, currentTime):
        #render the effect some number of ms after it was rendered before
        #alternatively, effects could keep track of the time themselves, but this would limit the ability to change the speed of effects externally
        pass

class EffectRes:
    @staticmethod
    def lerp(start, finish, progress):
        return start + (progress * (finish - start))