# -*- coding: utf-8 -*-
# @Author: Walker Pollard, Jay Batavia, Evan Mega
# @Date:   2014-10-19 21:20:00
# @Last Modified by:   evanmega
# @Last Modified time: 2014-10-19 21:58:07

import pyaudio, os
from socket import *

'''
ZombieComm radio server
'''

__version__ = "6.6.6"



CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 10000
RECORD_SECONDS = 5
p = pyaudio.PyAudio()
serverName = ''
serverPort = 62400
clientSocket = socket(AF_INET, SOCK_STREAM)

'''
Opens socket to zombie radio server and waits for sound
'''

try:
        clientSocket.connect((serverName,serverPort))
        print "Successfully connected"
except:
        print "Cannot connnect to server..."
        os._exit(1)

stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, output = True)
data = clientSocket.recv(CHUNK)

while data != ' ':
    i = raw_input('[q] to terminate client\n')
    if i == 'q':
        clientSocket.close()
        os._exit(1)
	stream.write(data)
	data = clientSocket.recv(CHUNK)

clientSocket.close()
