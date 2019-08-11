from core.effect import Effect
import time

class EmptyEffect(Effect):

    def __init__(self):
        pass

    def start(self, pixels, num_pixels):
        pass

    def render(self, pixels, num_pixels, ms_later):
        pass

class DefaultEffect(Effect):

    pos = 0
    dir = 1

    def __init__(self):
        pass

    def start(self, pixels, num_pixels):
        pixels.fill((0, 255, 0))

    def render(self, pixels, num_pixels, ms_later):
        
        if self.pos >= num_pixels or self.pos < 0:
            self.dir *= -1
            self.pos += self.dir

        if self.dir == 1:
            pixels[self.pos] = (255, 0, 0)

        
        if self.dir == -1:
            pixels[self.pos] = (0, 255, 0)

        self.pos += self.dir

class AlternatingSolidEffect(Effect):

    color_time = 0.5 # seconds

    colors = [(0, 0, 255), (255, 255, 0)]

    def __init__(self):
        pass

    def start(self, pixels, num_pixels):
        self.startTime = time.time()
        self.currentColorIndex = 0
        pixels.fill(self.colors[self.currentColorIndex])

    def render(self, pixels, num_pixels, ms_later):
        currentTime = time.time()
        if currentTime - self.startTime > self.color_time:
            self.alternateColor(pixels)
            self.startTime = currentTime

    def alternateColor(self, pixels):
        if(self.currentColorIndex == 0): self.currentColorIndex = 1
        elif(self.currentColorIndex == 1): self.currentColorIndex = 0

        pixels.fill(self.colors[self.currentColorIndex])
