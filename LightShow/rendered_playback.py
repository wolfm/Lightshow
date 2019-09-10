
from simulator import Simulator
#import board
#import neopixel

import time
import enum
import pkgutil
from importlib import import_module
from pathlib import Path
import sys
import inspect
from core.effect import Effect
import webserver.server as webserver
from enums import PlaybackMode
import pickle

def run(queue, config):
    player = RenderedPlayer(queue, config)
    player.run()

    #Automatically switch back to passive playback on show completion

    #empty the queue
    while(not queue.empty()):
        queue.get()
    
    #put the new target in the queue
    queue.put({
        "msg" : "newMode_internal",
        "newMode" : PlaybackMode.PASSIVE
    })

class RenderedPlayer:

    def __init__(self, queue, config):

        print("Starting Rendered Player")

        #Set configuration variables
        self.BPM = config['passive_bpm']
        self.LOOP_TIME = config['rendered_looptime_ms']
        self.NUM_PIXELS = config['num_pixels']
        self.BRIGHTNESS = config['brightness']
        self.queue = queue

        # convert loop time from ms to s for time.sleep() function
        self.LOOP_TIME /= 1000  

        # Initialize neopixel or simulator
        self.pixels = Simulator(self.NUM_PIXELS)
        #self.pixels = neopixel.NeoPixel(board.D18, self.NUM_PIXELS, brightness=self.BRIGHTNESS, auto_write=False)

        #Open show
        with open('rendered_shows/data.dat', 'rb') as show_file:
            data = pickle.load(show_file)
            if data["num_pixels"] != self.NUM_PIXELS:
                print("number of pixels configured (" + str(self.NUM_PIXELS) + ") differs from number of pixels specified in show (" + str(data['num_pixels']) + "). Unpredictable behavior may occur.") 
            self.prcoessMessageNUM_PIXELS = data['num_pixels']
            self.update_queue = data['data']
        
        self.terminate = False

    def prcoessMessage(self, msg):
        if msg['msg'] == 'abortShow':
            self.terminate = True
            print("Show aborted")


        elif msg['msg'] == 'changeMode' and msg['newMode'] != "RENDERED":
            print("Changing mode to: " + msg['newMode'])
            self.terminate = True

            #empty the queue
            while(not self.queue.empty()):
                self.queue.get()
            
            #put the new target in the queue
            if msg['newMode'] == "PASSIVE":
                newMode = PlaybackMode.PASSIVE

            self.queue.put({
                "msg" : "newMode_internal",
                "newMode" : newMode
            })
            
    def run(self):

        self.showStartTime = time.time()
        time.sleep(self.LOOP_TIME)

        if len(self.update_queue) <= 0:
            print("Show Concluded")
            time.sleep(2)
            return

        nextUpdate = self.update_queue.popleft()

        print("Update queue: " + str(self.update_queue))

        self.pixels.fill((0,0,0))

        while not self.terminate:
            loopStart = time.time()

            msg = None
            if(not self.queue.empty()):
                msg = self.queue.get()
                self.prcoessMessage(msg)

            currentTime = time.time()
            ms_since_start = (currentTime - self.showStartTime) * 1000
            
            index = 0 #debug 
            while(ms_since_start > nextUpdate[0]): #If true, then this update is ready to fire

                for pixel_update in nextUpdate[1]:
                    self.pixels[pixel_update[0]] = pixel_update[1]

                    index += 1 #debug

                if self.update_queue:
                    #start = time.time()
                    nextUpdate = self.update_queue.popleft()
                    #print(time.time() - start)


                else:
                    self.pixels.show()
                    print("Update queue end reached - Show Concluded")
                    time.sleep(2)
                    return
                
            self.pixels.show()
            time.sleep(self.LOOP_TIME)
