import playback
import webserver.server as webserver
from multiprocessing import Process, Queue

if __name__ == '__main__':

    pqueue = Queue()

    serverProcess = Process(target=webserver.startServer, args=(pqueue,))
    serverProcess.daemon = True

    playbackProcess = Process(target=playback.run, args=(pqueue,))
    playbackProcess.daemon = True

    serverProcess.start()
    playbackProcess.start() 

    playbackProcess.join()