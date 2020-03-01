from Microphone import Phone, STATE_IDLE, STATE_DETECT, STATE_RECORD, STATE_RECOGNITION
import numpy as np 
import argparse
import time
# from evdev import InputDevice
from select import select
import wave
import matplotlib.pyplot as plt
import position
from keyboard_map import map_all
import os
from pathlib import Path


key_name = 0

# def detectInputKey():
#     global key_name
#     dev = InputDevice('/dev/input/event4')
#     while True:
#         select([dev], [], [])
#         for event in dev.read():
#             if event.value == 1:
#                 key_name  = event.code
#                 #print(key_name)

parser = argparse.ArgumentParser()

parser.add_argument("-d", "--device", type = int, default = 8, help="decice index of microphone")
parser.add_argument("-r", "--rate", type = int, default = 48000, help="sampling rate of microphone")
parser.add_argument("-c", "--channel", type = int, default = 6, help="the number of channels")
parser.add_argument("-w", "--width", type = int, default = 2, help="the size of a single data (Bytes)")
parser.add_argument("-l", "--length", type = int, default = 5120, help="The length of chunk")
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
mode = 3 # mode = 1 real-time, mode = 2 save file, mode = 3 test using recorded wav.
# 如果选择了模式3，想要测试的音频的路径可以在position.py的17行更改
index = 0
TEST_WAVE = '.\\ppp.wav'

def save_keystroke(channel, rate, width, data):
    global index
    mydir = Path('./key_' + keyname) 
    if not mydir.exists():
        os.mkdir(mydir)
    wf = wave.open('./key_' + keyname + '/key_'+str(index)+'.wav', 'wb')
    wf.setnchannels(channel)
    wf.setsampwidth(width)
    wf.setframerate(rate)
    filedata = b''.join(data)
    #print(type(data[0]), len(filedata),  KEYSTROKE_LEN*RESPEAKER_WIDTH*RESPEAKER_CHANNELS)
    assert(len(filedata) == KEYSTROKE_LEN*RESPEAKER_WIDTH*RESPEAKER_CHANNELS)
    wf.writeframes(filedata)
    wf.close()

def init_for_DTOA():
    return map_all()

def Find_position(wave):
    # the function for position
    global key_dic
    angle = position.give_angle(wave)[0]
    angle = position.angle_normalized(angle)
    return position.find_top5_key(key_dic,angle)

def Pattern(raw_data):
    # the function to extract feature to recognize the keystroke
    return

def Systhesize(pos, pat):
    para_pos = 0.5
    para_pat = 0.5
    result_pos = pos[0]
    odd_pos = [para_pos * x for x in pos[1]]
    result_pat = pat[0]
    odd_pat = [para_pat * x for x in pat[1]]
    result = result_pat + result_pos
    odd1 = odd_pat + odd_pos
    key1 = []
    odd2 = []
    for i in range(0, len(result)):
        tmp_key = result[i]
        tmp_odd = odd1[i]
        flag = 0
        for j in range(0,len(key1)):
            if key1[j] == tmp_key:
                odd2 += odd1[i]
                flag = 1
                break
        if flag == 0:
            key1.append(tmp_key)
            odd2.append(tmp_odd)
    max_odd = max(odd2)
    print(key1[odd2.index(max_odd)])

key_dic = init_for_DTOA()


if mode == 3:
    print('---开启了对于已经录制的音频的测试模式---')
    [_, wave, _] = position.wavread(TEST_WAVE)
    probility = Find_position(wave)
    position_set = position.set_return(probility)
    position.give_set_excel(position_set,'helloworld.csv')

elif mode == 2 or mode ==1:
    microphone = Phone(RESPEAKER_RATE, RESPEAKER_CHANNELS,RESPEAKER_WIDTH,RESPEAKER_INDEX,CHUNK, mode, KEYSTROKE_LEN, WINDOW, STEP)
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
                        if raw_data == None:
                            [_, wave, _] = position.wavread(raw_data)
                        position_top5 = Find_position(wave)
                        #Pattern(raw_data)
                        t = np.arange(0, KEYSTROKE_LEN) / RESPEAKER_RATE
                        plt.plot(t, raw_data[0], color = 'green') 
                        plt.show()
                    break
        microphone.close()
    except KeyboardInterrupt:
        microphone.close()