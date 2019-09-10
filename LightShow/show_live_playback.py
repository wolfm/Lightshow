# Simple test for NeoPixels on Raspberry Pi
import time
#import board
#import neopixel
from simulator import Simulator
import enum
import pkgutil
from importlib import import_module
from pathlib import Path
import sys
import inspect
from core.effect import Effect
import webserver.server as webserver
from show import Show

def prcoessMessage(msg):
    if msg['msg'] == 'changeEffect':
        print("Changing effect to: " + msg['newEffect'])
        global currentEffect
        global all_effects
        currentEffect = all_effects["effects." + msg['newEffect']]()
        currentEffect.start(pixels, NUM_PIXELS)

def run(queue):

    global NUM_PIXELS
    NUM_PIXELS = 100
    LOOP_TIME = 4  # in ms

    # Dynamically import all effects
    for (_, mod_name, _) in pkgutil.iter_modules([Path(__file__).parent / "effects"]):

        import_module('effects.' + mod_name, package=__name__)
    
    global all_effects
    all_effects = {a.__module__ + '.' + a.__name__: a for a in Effect.__subclasses__()}

    print("Listing all effects: ")
    print(all_effects)
    global currentEffect
    currentEffect = all_effects["effects.defaultEffects.DefaultEffect"]()

    # Initialize neopixel or simulator
    # Pixels = neopixel.NeoPixel(pixel_pin, NUM_PIXELS, brightness=0.2, auto_write=False, pixel_order=ORDER)
    global pixels
    pixels = Simulator(NUM_PIXELS)

    class PlaybackMode(enum.Enum):
        PASSIVE = 0
        SYNCED = 1
        RENDERED = 2

    mode = PlaybackMode.SYNCED

    LOOP_TIME /= 1000  # convert from ms to s for time.sleep() function

    prevTime = time.time()

    currentShow = Show()
    currentShow.start(pixels, NUM_PIXELS)
    time.sleep(LOOP_TIME)

    show = Show()

    while True:
        msg = None
        if(not queue.empty()):
            msg = queue.get()
            prcoessMessage(msg)
            #TODO: switch statement through possible types of events, process event data and take action based on it

        currentTime = time.time()
        ms_later = (currentTime - prevTime) * 1000
        prevTime = currentTime

        currentShow.render(pixels, NUM_PIXELS, ms_later)
        pixels.show()
        time.sleep(LOOP_TIME)