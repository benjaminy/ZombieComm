import pyaudio
import collections


'''
ZombieComm radio server
'''

sound_frames = collections.deque()


def _record():

    global sound_frames

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 10000
    RECORD_SECONDS = 5
    p = pyaudio.PyAudio()
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    while True:
        data = stream.read(CHUNK)
        sound_frames.append(data)


