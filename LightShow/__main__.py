import passive_playback, rendered_playback
import webserver.server as webserver
from multiprocessing import Process, Queue
from enums import PlaybackMode

config = {
    "num_pixels" : 300,
    "brightness" : 0.35,
    "simulate" : True,
    "target" : passive_playback.run,
    "passive_bpm": 120,
    "passive_looptime_ms" : 4,
    "rendered_looptime_ms" : 4
}

target = config['target']

if __name__ == '__main__':

    pqueue = Queue()

    serverProcess = Process(target=webserver.startServer, args=(pqueue, ))
    serverProcess.daemon = True
    serverProcess.start()

    while True:

        playbackProcess = Process(target=target, args=(pqueue, config,))
        playbackProcess.daemon = True
        playbackProcess.start()
        playbackProcess.join()

        if not pqueue.empty() :
            item = pqueue.get()
            if item['msg'] == "newMode_internal":
                if item['newMode'] == PlaybackMode.PASSIVE:
                    target = passive_playback.run
                elif item['newMode'] == PlaybackMode.RENDERED:
                    target = rendered_playback.run
