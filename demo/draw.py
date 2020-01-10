import wave as we
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
import re
from tqdm import tqdm
import json
import sys

#copy from tuochao
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default = "./key_Q", help="The path of wav file")
args = parser.parse_args()
path = args.file


def wavread(wavfile):
    wavfile =  we.open(wavfile,"rb")
    params = wavfile.getparams()
    print(params[:4])
    framesra,frameswav= params[2],params[3]
    datawav = wavfile.readframes(frameswav)
    wavfile.close()
    datause = np.fromstring(datawav,dtype = np.int16)
    datause.shape = -1,6
    datause = datause.T
    print(datause.shape)
    time = np.arange(0, frameswav) * (1.0/framesra)
    return datause,time

def deal(wavfile):
    wavdata,wavtime = wavread(wavfile)
    plt.title("Night.wav's Frames")
    plt.subplot(321)
    plt.plot(wavtime, wavdata[0],color = 'green')
    plt.subplot(322)
    plt.plot(wavtime, wavdata[1])
    plt.subplot(323)
    plt.plot(wavtime, wavdata[2])
    plt.subplot(324)
    plt.plot(wavtime, wavdata[3])
    plt.subplot(325)
    plt.plot(wavtime, wavdata[4])
    plt.subplot(326)
    plt.plot(wavtime, wavdata[5])
    plt.show()


filelist=os.listdir(path)
wavlist=[]
for filename in filelist:
    filepath=os.path.join(path,filename)
    if (re.match(".*.wav",filename))!=None:
        #print(filename)
        wavlist.append(filepath)
for wavfile in tqdm(wavlist):
    print(wavfile)
    deal(wavfile)