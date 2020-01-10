#!/usr/bin/env python
#coding: utf-8
from Microphone import Phone, STATE_IDLE, STATE_DETECT, STATE_RECORD, STATE_RECOGNITION
import numpy as np 
import argparse
import time
from evdev import InputDevice
from select import select
import wave
import matplotlib.pyplot as plt

key_name = 0

def detectInputKey():
    global key_name
    dev = InputDevice('/dev/input/event4')
    while True:
        select([dev], [], [])
        for event in dev.read():
            if event.value == 1:
                key_name  = event.code
                #print(key_name)

parser = argparse.ArgumentParser()

parser.add_argument("-d", "--device", type = int, default = 8, help="decice index of microphone")
parser.add_argument("-r", "--rate", type = int, default = 48000, help="sampling rate of microphone")
parser.add_argument("-c", "--channel", type = int, default = 6, help="the number of channels")
parser.add_argument("-w", "--width", type = int, default = 2, help="the size of a single data (Bytes)")
parser.add_argument("-l", "--length", type = int, default = 5120, help="The lenght of chunk")
parser.add_argument("-k", "--key", type = str, default = 'A', help="The name of keystroke")

args = parser.parse_args()
RESPEAKER_RATE = args.rate
RESPEAKER_CHANNELS = args.channel
RESPEAKER_WIDTH = args.width # run getDeviceInfo.py to get index
RESPEAKER_INDEX = args.device  # refer to input device id
keyname = args.key
CHUNK = args.length
KEYSTROKE_LEN = 2048
WINDOW = 100
STEP = 20
RECORD_SECONDS = 5
mode = 2 # mode = 1 real-time, mode = 2 save file
microphone = Phone(RESPEAKER_RATE, RESPEAKER_CHANNELS,RESPEAKER_WIDTH,RESPEAKER_INDEX,CHUNK, mode, KEYSTROKE_LEN, WINDOW, STEP)
index = 0

def save_keystroke(channel, rate, width, data):
    global index
    wf = wave.open('./key_' + keyname + '/key_'+str(index)+'.wav', 'wb')
    wf.setnchannels(channel)
    wf.setsampwidth(width)
    wf.setframerate(rate)
    filedata = b''.join(data)
    #print(type(data[0]), len(filedata),  KEYSTROKE_LEN*RESPEAKER_WIDTH*RESPEAKER_CHANNELS)
    assert(len(filedata) == KEYSTROKE_LEN*RESPEAKER_WIDTH*RESPEAKER_CHANNELS)
    wf.writeframes(filedata)
    wf.close()

def Find_position(raw_data):
    # the function for position
    return

def Pattern(raw_data):
    # the function to extract feature to recognize the keystroke
    return

try:
    microphone.begin()
    while 1:
        microphone.detect_reset()
        while 1:
            if microphone.get_state() == STATE_RECOGNITION:
                index = index + 1    
                print("Begin recognition!\n")
                if mode == 2:
                    raw_frame = microphone.get_file_data()
                    save_keystroke(RESPEAKER_CHANNELS, RESPEAKER_RATE,RESPEAKER_WIDTH,raw_frame )
                elif mode == 1:
                    #print(type(raw_frame), len(raw_frame), len(raw_frame[0])+len(raw_frame[1]))
                    raw_data = microphone.get_raw_data() # the raw_data is a 4*10000 numpy for 4 channels with 10000 points in each channel
                    #print(raw_data[0].shape)
                    #Find_position(raw_data)
                    #Pattern(raw_data)
                    t = np.arange(0, KEYSTROKE_LEN) / RESPEAKER_RATE
                    plt.plot(t, raw_data[0], color = 'green') 
                    plt.show()
                break
    microphone.close()
except KeyboardInterrupt:
    microphone.close()