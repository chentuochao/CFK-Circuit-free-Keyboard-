import wave
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import librosa
import librosa.display
import os
import json
import sys
from tqdm import tqdm
import re
from scipy.fftpack import fft,ifft
import scipy.stats as stats
import seaborn as sns
import scipy
from scipy.stats import pearsonr
from python_speech_features import *

def get_mfcc(data,fs):
    wav_feature=mfcc(data,fs,nfft=1200)
    d_mfcc_feat = delta(wav_feature, 1)
    d_mfcc_feat2 = delta(wav_feature, 2)
    feature = np.hstack((wav_feature, d_mfcc_feat, d_mfcc_feat2))
    #print(type(feature))
    #print(len(feature))
    #print(feature)
    return feature

feature_path="./test_feature/"
eval_path="./eval/"
def getFirst(elem):
    return elem[0]

def get_key(wavfile):
    f=wave.open(wavfile,"rb")  
    params=f.getparams()
    #通道数、采样字节数、采样率、采样帧数
    nchannels,sampwidth,framerate,nframes=params[:4]
    voiceStrData=f.readframes(nframes)
    waveData = np.fromstring(voiceStrData,dtype=np.short)#将原始字符数据转换为整数
    #音频数据归一化
    waveData = waveData * 1.0/max(abs(waveData))
    #将音频信号规整乘每行一路通道信号的格式，即该矩阵一行为一个通道的采样点，共nchannels行
    waveData = np.reshape(waveData,[nframes,nchannels]).T # .T 表示转置
    f.close()

    data_mfcc=get_mfcc(waveData[1],48000)[0]
    tops=[]
    test_files=os.listdir(feature_path)
    for testfile in test_files:
        temp_mfcc=[]
        f=open(feature_path+testfile,"r")
        lines=f.readlines()
        for i in lines:
            temp_mfcc.append(float(i))
        f.close()
        r_row=np.corrcoef(np.array(data_mfcc),np.array(temp_mfcc))
        print(r_row)
        temp_list=[]
        temp_list.append(r_row)
        temp_list.append(testfile[:-6])
        tops.append(temp_list)
    ans_list=sorted(tops,key =getFirst,reverse=True)
    #print(ans_list)
    return ans_list

eval_list=["key_E","key_ENTER","key_Q","key_T","key_U"]
for evaldir in eval_list:
    print(evaldir)
    eval_files=os.listdir(eval_path+evaldir)
    for evalfile in eval_files:
        temp_list=get_key(eval_path+evaldir+"/"+evalfile)
        ans_list=temp_list[0:5]
        ans_list1=[]
        ans_list2=[]
        sum=0
        for each in ans_list:
            sum=sum+each[0]
        for each in ans_list:
            ans_list1.append(each[1])
            ans_list2.append(each[0]/sum)
        print(ans_list1,ans_list2)

            




