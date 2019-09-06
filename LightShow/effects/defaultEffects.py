from core.effect import Effect, EffectRes
import time

class EmptyEffect(Effect):

    def __init__(self, startTime, bpm, properties = {}):
        pass

    def start(self, pixels, num_pixels):
        pass

    def render(self, pixels, num_pixels, currentTIme):
        pass

class DefaultEffect(Effect):

    pos = 0
    colorList = [
        (255, 0, 0, 1.0),
        (0, 255, 0, 1.0),
        (0, 0, 255, 1.0)
    ]
    colorIndex = 0
    ms_per_wipe = 1000

    def __init__(self, startTime, bpm, properties = {}):
        self.startTime = startTime

    def start(self, pixels, num_pixels):
        self.ms_per_pixel = self.ms_per_wipe / num_pixels
        pass

    def render(self, pixels, num_pixels, currentTime):
        end_pos = ((currentTime - self.startTime) // self.ms_per_pixel) % (num_pixels * 3)
        while(self.pos != end_pos):
            self.pos += 1
            if(self.pos >= num_pixels):
                self.pos = 0
            pixels[self.pos % num_pixels] = self.colorList[self.pos // num_pixels]
        

class AlternatingSolidEffect(Effect):


    def __init__(self, startTime, bpm, properties = {}):
        self.startTime = startTime
        self.color_time = 500
        self.colors = [[255, 255, 255, 1.0],[0, 0, 0, 1.0]]

        if "color1" in properties:
            self.colors[0] = properties["color1"]
        else:
            self.colors[0] = [0, 0, 255, 1.0]
        if "color2" in properties:
            self.colors[1] = properties["color2"]
        else:
            self.colors[1] = [255, 255, 0, 1.0]
        
    def start(self, pixels, num_pixels):
        print("effect started with colors: " + str(self.colors))
        self.currentColorIndex = 0
        pixels.fill(self.colors[self.currentColorIndex])

    def render(self, pixels, num_pixels, currentTime):
        if currentTime - self.startTime >= self.color_time:
            self.alternateColor(pixels)
            self.startTime = currentTime

    def alternateColor(self, pixels):
        if(self.currentColorIndex == 0): self.currentColorIndex = 1
        elif(self.currentColorIndex == 1): self.currentColorIndex = 0

        pixels.fill(self.colors[self.currentColorIndex])

class SolidEffect(Effect):

    def __init__(self, startTime, bpm, properties = {}):
        self.startTime = startTime
        self.color = [255,0,0,1.0]
        if "color" in properties:
            self.color = properties["color"]

    def start(self, pixels, num_pixels):
        self.currentColorIndex = 0
        pixels.fill(self.color)

    def render(self, pixels, num_pixels, currentTime):
        pass


class MovingPixel(Effect):

    def __init__(self, startTime, bpm, properties = {}):
        self.startTime = startTime
        self.color = [0,0,0,1.0]
        self.pos = 0
        self.skip = 16
        if "color" in properties:
            self.color = properties["color"]

    def start(self, pixels, num_pixels):
        self.currentColorIndex = 0

    def render(self, pixels, num_pixels, currentTime):
        if self.skip > 0:
            self.skip -= 1
            return
        
        self.skip = 16
        pixels[self.pos] = [0,0,0, 0.0]
        self.pos += 1
        if self.pos >= num_pixels:
            self.pos = 0
        pixels[self.pos] = self.color

class Pulse(Effect):

    def __init__(self, startTime, bpm, properties = {}):
        self.startTime = startTime
        self.pulsesPerBeat = 1
        self.colors = [[255, 0, 255, 1.0],[0, 50, 200, 1.0]]
        self.bpm = bpm
        self.symmetric = True

        if "color1" in properties:
            self.colors[0] = properties["color1"]
        if "color2" in properties:
            self.colors[1] = properties["color2"]
        if "pulsesPerBeat" in  properties:
            self.pulsesPerBeat = properties["pulsesPerBeat"]
        if "symmetric" in properties:
            self.symmetric = properties["symmetric"]
        
        if self.symmetric:
            self.pulsesPerBeat *= 2

        self.ms_per_transition = 1 / ((self.pulsesPerBeat) * bpm / 60000)
        
    def start(self, pixels, num_pixels):
        self.currentColorIndex = 0
        pixels.fill(self.colors[0])

    def render(self, pixels, num_pixels, currentTime):
        pixel = [0,0,0,1.0]
        instant = (currentTime-self.startTime)
        progress = (instant %  self.ms_per_transition) / (self.ms_per_transition)
        if self.symmetric == True:
            if instant // self.ms_per_transition % 2 == 0:
                for i in range(0,3):
                    pixel[i] = EffectRes.lerp(self.colors[0][i], self.colors[1][i], progress)
            else:
                for i in range(0,3):
                    pixel[i] = EffectRes.lerp(self.colors[1][i], self.colors[0][i], progress)

        else:
            for i in range(0,3):
                pixel[i] = EffectRes.lerp(self.colors[0][i], self.colors[1][i], progress)

        pixels.fill(pixel)