import pyaudio
import collections
import thread
from socket import *

'''
ZombieComm radio server
'''

__author__ = "Walker Pollard, Jay Batavia"
__version__ = "6.6.6"



sound_frames = collections.deque()
HOST = '10.0.0.54'
PORT = 62400
CHUNK = 1024



def broadCastHandler(connectionSocket, addr):
    
    '''
    Sends chunks from queue through sockets
    '''
    
    global sound_frames

    while True:
        try:
            if len(sound_frames) > 0 and len(sound_frames)<=20: 
                connectionSocket.send(sound_frames.popleft())
            elif len(sound_frames)>20:
                sound_frames.popleft()
        except:
            pass
	connectionSocket.close()


def record():
    
    '''
    Records audio from mic in kb chunks
    '''

    global sound_frames

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 10000
    p = pyaudio.PyAudio()
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    while True:
        data = stream.read(CHUNK)
        sound_frames.append(data)



if __name__ == '__main__':
    
    '''
    Main method handles sockets and 
    calls record, broadcast
    '''
    
    serverPort = PORT
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind((HOST,serverPort))
    serverSocket.listen(1)
    
    print 'Server is recording'
    thread.start_new_thread(record, ())
   
    while 1:
        try:
            connectionSocket, addr = serverSocket.accept()
            print "Creating new thread"
            thread.start_new_thread(broadCastHandler, (connectionSocket, addr)) 
        except:
            print "Cannot initialize socket..."
            break
