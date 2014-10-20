import pyaudio
import collections
import threading

'''
ZombieComm radio server
'''

sound_frames = collections.deque()


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
        data = stream.read(CHUNK)
        sound_frames.append(data)


if __name__ == '__main__':
    '''
   main method simply prints recorded data right now
   '''

    t = threading.Thread(target=record)
    t.start()
    while True:
        try:
            if len(sound_frames) > 0:
                print (sound_frames.popleft())
        except:
            pass




