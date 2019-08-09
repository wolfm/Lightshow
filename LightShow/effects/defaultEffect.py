import abc;
from core.effect import Effect

class DefaultEffect(Effect):

    i = 0

    def __init__(self):
        i = 0

    def start(self, pixels, n):
        pixels.fill((0, 255, 0))

    def render(self, pixels, n, ms_later):
        
        if self.i < n:
            pixels[self.i] = (255, 0, 0)
            self.i += 1
        else:
            pixels.fill((0, 255, 0))
            self.i = 0