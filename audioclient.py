import pyaudio
import socket
import sys
import threading

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 192000
CHUNK = 4096
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((input("IP:"), int(input("Port:"))))
audio = pyaudio.PyAudio()
streamsend = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, stream_callback=callback)
streamrecieve = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
class recieve(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        data = s.recv(CHUNK)
        streamrecieve.write(data)
        recieving = recieve()
        recieving.start()
def callback(in_data, frame_count, time_info, status):
    s.send(in_data)
    return (None, pyaudio.paContinue)
recieving = recieve()
recieving.start()