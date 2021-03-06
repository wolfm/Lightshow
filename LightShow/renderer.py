#TODO:
# - Work out blending of colors between layers
# - Make more effects and make first actual light show!
# - Make the GUI for controlling passive effects at least usable
# - Wire up the device
# - Move the actual creating of the pixels object to the __main__ (so that it exists outside the thread, isn't recreated with each thread)
# - Convert deques to queues
# - Make it so that each json file does not have to specify "effects." for each effect name

from collections import deque
from queue import Queue
import pickle
import json
import pkgutil
from importlib import import_module
from pathlib import Path
from core.effect import Effect
from layer import Layer

MS_STEP = 25

def beatsToMs(bpm, beats):
    return (beats - 1) / bpm * 60000

def msToBeats(bpm, ms):
    return ((ms / 60000) * bpm) + 1

# take show input file, convert to a show in memory
with open('shows/EverytimeWeTouch.json') as json_file:
    showInput = json.load(json_file)

title = showInput['title']
version = showInput['version']
bpm = showInput['bpm']
ms_length = beatsToMs(bpm, showInput['totalBeats'])
num_pixels = showInput['num_pixels']
effectsQueue = deque(showInput['effects'])

# Dynamically import all effects
for (_, mod_name, _) in pkgutil.iter_modules([Path(__file__).parent / "effects"]):

    import_module('effects.' + mod_name, package=__name__)

global all_effects
all_effects = {a.__module__ + '.' + a.__name__: a for a in Effect.__subclasses__()}


effectsList = []

#instantiate effects, add to list of effect info dictionaries
while len(effectsQueue) > 0:
    effect = effectsQueue.popleft()
    startTime = beatsToMs(bpm, effect['startBeat'])
    endTime = beatsToMs(bpm, effect['endBeat'])
    layer = effect['layer']
    effectObject = all_effects["effects." + effect['effect']](startTime, bpm, effect['properties'])
    effectsList.append({
        "startTime" : startTime,
        "endTime": endTime,
        "layer" : layer,
        "effectObject": effectObject
    })

print(effectsList)


#render loop setup

ms_elapsed = 0
showData = []
layers = []
nextEventIndex = 0

#render loop
while ms_elapsed < ms_length:
    #check to see if any new events have started
    while nextEventIndex < len(effectsList) and effectsList[nextEventIndex]["startTime"] <= ms_elapsed:

        index = 0
        #Add the effect in the proper layer
        for index in range(0, len(layers)):
            if effectsList[nextEventIndex]["layer"] < layers[index].getLayerLevel():
                break
            else:
                index += 1
        
        nextEffect = effectsList[nextEventIndex]
        #print("inserting effect: " + str(nextEffect["effectObject"].colors))
        layers.insert(index, Layer(num_pixels, nextEffect["effectObject"], nextEffect["layer"], nextEffect["endTime"]))
        layers[index].start()

        #print("New effect started with properties" + str(effectsList[nextEventIndex]['properties']))
        nextEventIndex += 1

    
    #Call render or end on all layers and get set of pixels that need to be 
    update_set = set()
    for i in range(len(layers) - 1, -1, -1):
        if ms_elapsed >= layers[i].end_time:
            layers.pop(i)
            print("Layer " + str(i) + " finished")
            update_set = update_set.union(set(range(0,num_pixels)))

        else:
            returned_set = layers[i].update_layer(ms_elapsed)
            #print("layers[i].update_layer(ms_elapsed) returns " + str(returned_set))
            update_set = update_set.union(returned_set)
            layers[i].clear_update_set()
            #print("Update set is now: " + str(update_set))

    #print("Update set size " + str(len(update_set)))

    #Iterate through each of the pixels in the set, mixing layers to get the output pixel color
        #For each, add an entry to the showData deque (ms_elapsed, pixelId, (r,g,b))
    update_list = []
    for pixel_id in update_set:
        #mix all layers at this pixel ID above a (0,0,0) base layer
        pixel = [0,0,0]
        for layer in layers:
            '''
            pixel[0] = layer[pixel_id][0]
            pixel[1] = layer[pixel_id][1]
            pixel[2] = layer[pixel_id][2]
            '''
            pixel[0] = int((layer[pixel_id][0] * layer[pixel_id][3]) + (pixel[0] * (1.0 - layer[pixel_id][3])))
            pixel[1] = int((layer[pixel_id][1] * layer[pixel_id][3]) + (pixel[1] * (1.0 - layer[pixel_id][3])))
            pixel[2] = int((layer[pixel_id][2] * layer[pixel_id][3]) + (pixel[2] * (1.0 - layer[pixel_id][3])))

        update_list.append((pixel_id, tuple(pixel)))
    update_set.clear()
    if len(update_list) > 0:
        showData.append((ms_elapsed, update_list))
    ms_elapsed += MS_STEP

print('Rendering complete')

#convert the show in memory to a deque of pixel changes
## format is (ms since start, pixel id, new pixel color tuple (r,g,b))

#save show as a binary

show = {"name": "Test Show", 
        "num_pixels": num_pixels,
        "data": showData
        }

print("showData")
print(showData)

with open('rendered_shows/data.dat', 'wb') as outfile:
    pickle.dump(show, outfile)
