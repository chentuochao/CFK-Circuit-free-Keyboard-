from Microphone import Phone
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


microphone = Phone(RESPEAKER_RATE, RESPEAKER_CHANNELS,RESPEAKER_WIDTH,RESPEAKER_INDEX,CHUNK, 1)
time.sleep(4)
microphone.begin()
time.sleep(5)
microphone.end()
microphone.save_file('output.wav')
microphone.close()