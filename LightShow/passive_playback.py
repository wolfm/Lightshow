import time
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
from enums import PlaybackMode
#import board
#import neopixel

#TODO
# - Rewrite to avoid all these globals vars
# - Add the ability to change effect parameters on the fly



def run(queue, config):
    player = PassivePlayer(queue, config)
    player.run()


class PassivePlayer:

    def __init__(self, queue, config):

        print("Starting PassivePlayer")

        #Set configuration variables
        self.BPM = config['passive_bpm']
        self.LOOP_TIME = config['passive_looptime_ms']
        self.NUM_PIXELS = config['num_pixels']
        self.BRIGHTNESS = config['brightness']
        self.queue = queue

        # convert loop time from ms to s for time.sleep() function
        self.LOOP_TIME /= 1000  

        # Dynamically import all effects
        for (_, mod_name, _) in pkgutil.iter_modules([Path(__file__).parent / "effects"]):

            import_module('effects.' + mod_name, package=__name__)
        
        self.all_effects = {a.__module__ + '.' + a.__name__: a for a in Effect.__subclasses__()}
        
        #Set initial effect to empty effect
        self.currentEffect = self.all_effects["effects.defaultEffects.EmptyEffect"](0, self.BPM)

        # Initialize neopixel or simulator
        self.pixels = Simulator(self.NUM_PIXELS)
        ### self.pixels = neopixel.NeoPixel(board.D18, self.NUM_PIXELS, brightness=self.BRIGHTNESS, auto_write=False)


        #Create effect layer, which will be rendered over black background
        self.layer = Layer(self.NUM_PIXELS, self.currentEffect, 1, None)
        self.layer.start()

        #Set up time variables
        self.startTime = time.time()
        self.ms_elapsed = time.time() - self.startTime
        
        #Create set to store pixel updates
        self.update_set = set()

        #Initialize thread termination boolean to false
        self.terminate = False

    def prcoessMessage(self, msg):
        if msg['msg'] == 'changeEffect':
            print("Changing effect to: " + msg['newEffect'])
            currentEffect = self.all_effects["effects." + msg['newEffect']](self.ms_elapsed, self.BPM)
            self.layer = Layer(self.NUM_PIXELS, currentEffect, 1, None)
            self.layer.start()

        elif msg['msg'] == 'changeMode' and msg['newMode'] != "PASSIVE":
            print("Changing mode to: " + msg['newMode'])
            self.terminate = True

            #empty the queue
            while(not self.queue.empty()):
                self.queue.get()
            
            #put the new target in the queue
            if msg['newMode'] == "RENDERED":
                newMode = PlaybackMode.RENDERED

            self.queue.put({
                "msg" : "newMode_internal",
                "newMode" : newMode
            })


    def run(self):
        while not self.terminate:
            msg = None
            if(not self.queue.empty()):
                msg = self.queue.get()
                self.prcoessMessage(msg)
                #TODO: switch statement through possible types of events, process event data and take action based on it

            currentTime = time.time()
            self.ms_elapsed = (currentTime - self.startTime) * 1000
            returned_set = self.layer.update_layer(self.ms_elapsed)
            update_set = self.update_set.union(returned_set)
            self.layer.clear_update_set()


            for pixel_id in update_set:
                #mix all layers at this pixel ID above a (0,0,0) base layer
                pixel = [0,0,0]
                pixel[0] = int((self.layer[pixel_id][0] * self.layer[pixel_id][3]) + (pixel[0] * (1.0 - self.layer[pixel_id][3])))
                pixel[1] = int((self.layer[pixel_id][1] * self.layer[pixel_id][3]) + (pixel[1] * (1.0 - self.layer[pixel_id][3])))
                pixel[2] = int((self.layer[pixel_id][2] * self.layer[pixel_id][3]) + (pixel[2] * (1.0 - self.layer[pixel_id][3])))

                self.pixels[pixel_id] = tuple(pixel)

            self.update_set.clear()
            
            self.pixels.show()
            time.sleep(self.LOOP_TIME)
