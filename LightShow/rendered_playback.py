import time
from simulator import Simulator
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
#import board
#import neopixel

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
        ### self.pixels = neopixel.NeoPixel(board.D18, self.NUM_PIXELS, brightness=self.BRIGHTNESS, auto_write=False)

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

        nextElement = self.update_queue.popleft()

        self.pixels.fill((0,0,0))

        while not self.terminate:
            msg = None
            if(not self.queue.empty()):
                msg = self.queue.get()
                self.prcoessMessage(msg)

            currentTime = time.time()
            ms_since_start = (currentTime - self.showStartTime) * 1000

            while(ms_since_start > nextElement[0]): #If true, then this update is ready to fire
                self.pixels[nextElement[1]] = nextElement[2]
                try:
                    nextElement = self.update_queue.popleft()
                except IndexError:
                    self.pixels.show()
                    print("Show Concluded")
                    time.sleep(2)
                    return
                
            self.pixels.show()
            time.sleep(self.LOOP_TIME)
