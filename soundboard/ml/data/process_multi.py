import librosa
import wave as we
import librosa.display 
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import json
import os
import re
from tqdm import tqdm
import json
import sys
import random
import pickle
from pathlib import Path



sliced_data = []

def cut(y, raw, keytime, keys):
    wide = 64
    energy = librosa.feature.rms(y, frame_length = wide, hop_length = wide, center = True)
    l = energy.shape[1]
    rms = np.zeros(l - 1)
    for i in range(0 , l-1):
        rms[i] =  energy[0][i + 1] - energy[0][i]
    plt.plot(np.array(range(0, l - 1))*wide/48000, rms, color = 'green')
    keytime2 = []
    calibration = [0]
    for key in range(0, len(keytime)):
        begin = keytime[key] * 48 + np.mean(calibration)
        begin = int(round(begin))
        for i in range(begin-2000, begin + 1000, wide):
            index = round(i / wide)
            if rms[index] > 50: #100
                calibration.append(- keytime[key] + (i - 128) / 48)
                keytime2.append((i - 128) / 48)
                break
    for i in range(0, len(keytime2)):
        x_index = (keytime2[i] )/1000
        plt.vlines(x_index, -8000,8000,color = 'black' )
        if keys[i] >= 97 and keys[i] <= 122:
            keytime_start = int((keytime2[i] ) * 48)
            keytime_end = keytime_start + 2048
            key_input = raw[1:5, keytime_start: keytime_end]
            output = keys[i] - 32
            global sliced_data
            sliced_data += [(key_input, output)]

def deal_wave(file, txtfile):
    wavfile =  we.open(file,"rb")
    params = wavfile.getparams()
    #print(params[:4])
    framesra,frameswav= params[2],params[3]
    datawav = wavfile.readframes(frameswav)
    wavfile.close()
    datause = np.fromstring(datawav,dtype = np.int16)
    datause.shape = -1,6
    datause = datause.T
    time = np.arange(0, frameswav) * (1.0/framesra)
    y = np.asfortranarray(datause[1], dtype = float)
    #print(y.shape, y.flags['F_CONTIGUOUS'])
    
    txt = open(txtfile,"r",encoding="utf-8")
    line = txt.readline() # 整行读取数据
    keys = json.loads(line)
    #print(keys)
    line = txt.readline() # 整行读取数据
    keytime = json.loads(line)
    txt.close()

    b, a = signal.butter(4, 0.1, 'highpass')  #配置滤波器 8 表示滤波器的阶数
    filtedData = signal.filtfilt(b, a, y) #data为要过滤的信号
    y = np.asfortranarray(filtedData, dtype = float)
    plt.figure(0)
    plt.plot(time,y,color = 'blue')
    raw = np.vstack((datause[1],datause[4],datause[5],datause[2]))
    cut(y, raw, keytime, keys)
    plt.show()

def print_sliced_data(index):
    key_input, output = sliced_data[index]
    time = np.arange(0, len(key_input[0])) * (1.0 / 48000)
    plt.plot(time, key_input[0], color='green')
    plt.show()


if __name__ == '__main__':  # 枚举path路劲下的所有wav和txt文件
    path = "./multi_key"
    filelist = os.listdir(path)
    wavlist = []
    for filename in filelist:
        filepath = os.path.join(path, filename)
        if (re.match(".*.wav", filename)) != None:
            # print(filename)
            wavlist.append(filepath)
    for wavfile in tqdm(wavlist):
        print(wavfile)
        txtfile = wavfile[0: -3] + "txt"
        deal_wave(wavfile, txtfile)
        # input("next->")
    indexes = random.choices(range(len(sliced_data)), k=20)
    for index in indexes:
        print_sliced_data(index)
    keys = set()
    for key_input, output in sliced_data:
        keys.add(output)
    print(keys)
    print(len(keys))
    pickle.dump(sliced_data, open("../processed_data/sliced_data.pkl", "wb"))