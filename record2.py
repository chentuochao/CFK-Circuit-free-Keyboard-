import pyaudio
import wave
import numpy as np
import argparse
import time

parser = argparse.ArgumentParser()

parser.add_argument("-d", "--device", type = int, default = 8, help="decice index of microphone")
parser.add_argument("-r", "--rate", type = int, default = 48000, help="sampling rate of microphone")
parser.add_argument("-c", "--channel", type = int, default = 6, help="the number of channels")
parser.add_argument("-w", "--width", type = int, default = 2, help="the size of a single data (Bytes)")
parser.add_argument("-l", "--length", type = int, default = 1024, help="The lenght of chunk")

args = parser.parse_args()
RESPEAKER_RATE = args.rate
RESPEAKER_CHANNELS = args.channel
RESPEAKER_WIDTH = args.width # run getDeviceInfo.py to get index
RESPEAKER_INDEX = args.device  # refer to input device id
CHUNK = args.length
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()
stream = p.open(
        rate=RESPEAKER_RATE,
        format=p.get_format_from_width(RESPEAKER_WIDTH),
        channels=RESPEAKER_CHANNELS,
        frames_per_buffer=CHUNK,
        input=True,
        input_device_index=RESPEAKER_INDEX,)
stream.start_stream()
   
def save_file(path, frames):
    wf = wave.open(path, 'wb')
    wf.setnchannels(RESPEAKER_CHANNELS)
    wf.setsampwidth(p.get_sample_size(p.get_format_from_width(RESPEAKER_WIDTH)))
    wf.setframerate(RESPEAKER_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def decode(data):  # return four channel
    w1 = np.fromstring(data,dtype=np.int16)[1::6]
    w2 = np.fromstring(data,dtype=np.int16)[2::6]
    w3 = np.fromstring(data,dtype=np.int16)[3::6]
    w4 = np.fromstring(data,dtype=np.int16)[4::6]
    return [w1, w2, w3, w4]

def main():
    frame = []
    for i in range(0,500):
        data = stream.read(CHUNK)
        decode(data)
        frame.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    save_file(WAVE_OUTPUT_FILENAME, frame)

main()

