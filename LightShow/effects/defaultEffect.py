import abc;
from core.effect import Effect

class DefaultEffect(Effect):

    pos = 0
    dir = 1

    def __init__(self):
        pass

    def start(self, pixels, n):
        pixels.fill((0, 255, 0))

    def render(self, pixels, n, ms_later):
        
        if self.pos >= n or self.pos < 0:
            self.dir *= -1
            self.pos += self.dir

        if self.dir == 1:
            pixels[self.pos] = (255, 0, 0)

        
        if self.dir == -1:
            pixels[self.pos] = (0, 255, 0)

        self.pos += self.dir
            
        
        