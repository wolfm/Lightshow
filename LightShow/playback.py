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
from layer import Layer
import webserver.server as webserver

#TODO
# - Rewrite to avoid all these globals vars
# - Add the ability to change effect parameters on the fly

def prcoessMessage(msg):
    if msg['msg'] == 'changeEffect':
        print("Changing effect to: " + msg['newEffect'])
        global all_effects
        global layer
        global NUM_PIXELS
        global ms_elapsed
        global BPM
        currentEffect = all_effects["effects." + msg['newEffect']](ms_elapsed, BPM)
        layer = Layer(NUM_PIXELS, currentEffect, 1, None)
        layer.start()

def run(queue):

    global NUM_PIXELS
    global BPM
    BPM = 120
    NUM_PIXELS = 100
    LOOP_TIME = 4  # in ms

    # Dynamically import all effects
    for (_, mod_name, _) in pkgutil.iter_modules([Path(__file__).parent / "effects"]):

        import_module('effects.' + mod_name, package=__name__)
    
    global all_effects
    all_effects = {a.__module__ + '.' + a.__name__: a for a in Effect.__subclasses__()}

    print("Listing all loaded effects: ")
    print(all_effects)

    
    startTime = time.time()

    currentEffect = all_effects["effects.defaultEffects.Pulse"](0, BPM)

    # Initialize neopixel or simulator
    # Pixels = neopixel.NeoPixel(pixel_pin, NUM_PIXELS, brightness=0.2, auto_write=False, pixel_order=ORDER)
    global pixels
    pixels = Simulator(NUM_PIXELS)

    class PlaybackMode(enum.Enum):
        PASSIVE = 0
        SYNCED = 1
        RENDERED = 2

    mode = PlaybackMode.PASSIVE

    LOOP_TIME /= 1000  # convert from ms to s for time.sleep() function

    #currentEffect.start(pixels, NUM_PIXELS)
    time.sleep(LOOP_TIME)

    global layer
    layer = Layer(NUM_PIXELS, currentEffect, 1, None)
    layer.start()
    
    update_set = set()
    global ms_elapsed

    while True:
        msg = None
        if(not queue.empty()):
            msg = queue.get()
            prcoessMessage(msg)
            #TODO: switch statement through possible types of events, process event data and take action based on it

        currentTime = time.time()
        ms_elapsed = (currentTime - startTime) * 1000
        returned_set = layer.update_layer(ms_elapsed)
        #print("Returned set: " + str(returned_set))
        update_set = update_set.union(returned_set)
        layer.clear_update_set()

        #print("Update set: " + str(update_set))

        for pixel_id in update_set:
            #mix all layers at this pixel ID above a (0,0,0) base layer
            pixel = [0,0,0]
            '''
            pixel[0] = layer[pixel_id][0]
            pixel[1] = layer[pixel_id][1]
            pixel[2] = layer[pixel_id][2]
            '''
            pixel[0] = int((layer[pixel_id][0] * layer[pixel_id][3]) + (pixel[0] * (1.0 - layer[pixel_id][3])))
            pixel[1] = int((layer[pixel_id][1] * layer[pixel_id][3]) + (pixel[1] * (1.0 - layer[pixel_id][3])))
            pixel[2] = int((layer[pixel_id][2] * layer[pixel_id][3]) + (pixel[2] * (1.0 - layer[pixel_id][3])))

            pixels[pixel_id] = tuple(pixel)

        update_set.clear()
        
        pixels.show()
        time.sleep(LOOP_TIME)
        '''
        currentEffect.render(pixels, NUM_PIXELS, ms_later)
        '''