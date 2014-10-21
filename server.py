# @Project: ZombieComm
# @Author: Walker Pollard, Jay Batavia, Evan Mega
# @Date:   2014-10-19 21:20:00
# @Last Modified by:   evanmega
# @Last Modified time: 2014-10-21 08:22:37

import pyaudio, collections, thread, os
from socket import *

sound_frames = collections.deque()
HOST = ''
PORT = 62400
CHUNK = 1024

'''
Sends chunks from queue through sockets
'''
def broadCastHandler(connectionSocket, addr):

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


'''
Records audio from mic in kb chunks
'''
def record():

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
        i = raw_input('[q] to terminate stream\n')
        if i == 'q':
            stream.close()
            os._exit(1)

        data = stream.read(CHUNK)
        sound_frames.append(data)



'''
Main method handles sockets and
calls record, broadcast
'''
if __name__ == '__main__':

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
            os._exit(1)
            print "Cannot initialize socket..."

