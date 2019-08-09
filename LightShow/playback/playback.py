# Simple test for NeoPixels on Raspberry Pi
import time
#import board
#import neopixel
from .simulator import Simulator
import enum
from effects.defaultEffects import *


def run():

    NUM_PIXELS = 100
    LOOP_TIME = 4 # in ms

    currentEffect = AlternatingSolidEffect()

    #Initialize neopixel or simulator
    #pixels = neopixel.NeoPixel(pixel_pin, NUM_PIXELS, brightness=0.2, auto_write=False, pixel_order=ORDER)
    pixels = Simulator(NUM_PIXELS)

    class PlaybackMode(enum.Enum):
        PASSIVE = 0
        SYNCED = 1
        RENDERED = 2

    mode = PlaybackMode.PASSIVE

    LOOP_TIME /= 1000 #convert from ms to s for time.sleep() function

    prevTime = time.time()
    currentEffect.start(pixels, NUM_PIXELS)
    time.sleep(LOOP_TIME)

    while True:
        currentTime = time.time()
        ms_later = (currentTime - prevTime) * 1000
        prevTime = currentTime

        currentEffect.render(pixels, NUM_PIXELS, ms_later)
        pixels.show()
        time.sleep(LOOP_TIME)
    

''' test 
while True:

    for i in range(0, NUM_PIXELS):
        pixels[i] = (0,255,0)

    pixels.show()
    time.sleep(0.01)
    
    for i in range(0, NUM_PIXELS):
        pixels[i] = (255, 0, 0)
        pixels.show()
        time.sleep(0.01)

'''
