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

import pickle

def prcoessMessage(msg):
    if msg['msg'] == 'abortShow':
        print("Aborting Show -- TODO implement this")

def run(queue):

    global NUM_PIXELS
    NUM_PIXELS = 0
    LOOP_TIME = 4  # in ms
    update_queue = None


    with open('data.dat', 'rb') as show_file:
        data = pickle.load(show_file)
        NUM_PIXELS = data['num_pixels']
        update_queue = data['data']
        print(data)

    # Initialize neopixel or simulator
    # Pixels = neopixel.NeoPixel(pixel_pin, NUM_PIXELS, brightness=0.2, auto_write=False, pixel_order=ORDER)
    global pixels
    print("NUM_PIXELS: " + str(NUM_PIXELS))
    pixels = Simulator(NUM_PIXELS)

    LOOP_TIME /= 1000  # convert from ms to s for time.sleep() function

    showStartTime = time.time()
    time.sleep(LOOP_TIME)

    if len(update_queue) <= 0:
        print("Show Concluded")
        time.sleep(2)
        return

    nextElement = update_queue.popleft()

    pixels.fill((0,0,0))

    while True:
        msg = None
        if(not queue.empty()):
            msg = queue.get()
            prcoessMessage(msg)

        currentTime = time.time()
        ms_since_start = (currentTime - showStartTime) * 1000

        while(ms_since_start > nextElement[0]): #If true, then this update is ready to fire
            pixels[nextElement[1]] = nextElement[2]
            try:
                nextElement = update_queue.popleft()
            except IndexError:
                pixels.show()
                print("Show Concluded")
                time.sleep(2)
                return
            
        pixels.show()
        time.sleep(LOOP_TIME)
