import wave as we
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
import re
from tqdm import tqdm
import json
import sys
import random
import pickle
from pathlib import Path

sliced_data = []

def deal(wavfile, keystroke):  # 读取对应的txt, wav的文件
    wavfile = we.open(wavfile, "rb")
    params = wavfile.getparams()
    framesra, frameswav = params[2], params[3]  # 参数
    datawav = wavfile.readframes(frameswav)
    wavfile.close()
    datause = np.fromstring(datawav, dtype=np.int16)
    datause.shape = -1, 6
    datause = datause.T  # 6 channel, channel 1 -> after demoise, channel 4 -> no data, other four channels are the raw data from four microphones
    input = datause[1:5, :]
    output = np.zeros(26)
    index = ord(keystroke) - 65
    #print(keystroke, index)
    output[index] = 1
    global sliced_data
    sliced_data += [(input, index)]

def print_sliced_data(index):
    key_input, output = sliced_data[index]
    time = np.arange(0, len(key_input[0])) * (1.0 / 48000)
    plt.plot(time, key_input[0], color='green')
    plt.show()


if __name__ == '__main__':  # 枚举path路劲下的所有wav和txt文件
    for key in range(0, 26):
        keystroke = chr(ord('A') + key)
        my_dir = Path('./key_' + keystroke) 
        if my_dir.exists():
            print('deal with key_' + keystroke)
            filelist = os.listdir(my_dir)
            wavlist = []
            for filename in filelist:
                filepath = os.path.join(my_dir, filename)
                if (re.match(".*.wav", filename)) != None:
                    wavlist.append(filepath)
            for wavfile in tqdm(wavlist):
                #print(wavfile)
                deal(wavfile, keystroke)
    indexes = random.choices(range(len(sliced_data)), k=10)
    for index in indexes:
        print_sliced_data(index)
    pickle.dump(sliced_data, open("../processed_data/sliced_data.pkl", "wb"))
