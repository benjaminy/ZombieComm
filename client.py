from socket import *
import pyaudio

'''
ZombieComm radio server
'''

__author__ = "Walker Pollard, Jay Batavia"
__version__ = "6.6.6"



CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 10000
RECORD_SECONDS = 5
p = pyaudio.PyAudio()
serverName = '10.0.0.36'
serverPort = 62400
clientSocket = socket(AF_INET, SOCK_STREAM)

'''
Opens socket to zombie radio server and waits for sound
'''

try:
        clientSocket.connect((serverName,serverPort))
except:
        print "Cannot connnect to server..."
        
stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, output = True)
data = clientSocket.recv(CHUNK)

while data != ' ':
	stream.write(data)
	data = clientSocket.recv(CHUNK)
	
clientSocket.close()
