# -*- coding: utf-8 -*-
# @Author: Walker Pollard, Jay Batavia, Evan Mega
# @Date:   2014-10-19 21:20:00
# @Last Modified by:   evanmega
# @Last Modified time: 2014-10-19 22:10:20

import pyaudio, collections, thread, os
from socket import *

'''
ZombieComm radio server
'''

__version__ = "6.6.6"



sound_frames = collections.deque()
HOST = ''
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
        i = raw_input('[q] to terminate stream\n')
        if i == 'q':
            stream.close()
            os._exit(1)

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
            os._exit(1)
            print "Cannot initialize socket..."

