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
import scipy
from scipy.stats import pearsonr
import scipy.stats as stats
import seaborn as sns
from python_speech_features import *

def do(x,y):
    if x-y>0.075:
        return x
    else:
        return 0
def get_mfcc(data,fs):
    wav_feature=mfcc(data,fs,nfft=1200)
    #print(wav_feature)
    d_mfcc_feat = delta(wav_feature, 1)
    d_mfcc_feat2 = delta(wav_feature, 2)
    feature = np.hstack((wav_feature, d_mfcc_feat, d_mfcc_feat2))
    print(type(feature))
    #print(len(feature))
    #print(feature)
    return feature
key_list=["key_Q","key_QQ","key_W","key_WW"]
data_path="./test/"
feature_path="./test_feature/"
dict={}
keynames=os.listdir(data_path)
for keyname in keynames:
#keyname="key_Q"
    temp_path=data_path+keyname+"/"
    file_names=os.listdir(temp_path)
    key=keyname[4:]
    cnt=0
    #plt.title("Q_frequency_field")
    for filename in file_names:

        #print(filename)
        f=wave.open(temp_path+filename,"rb")

        params=f.getparams()
        #通道数、采样字节数、采样率、采样帧数
        nchannels,sampwidth,framerate,nframes=params[:4]
        #print(nchannels)
        voiceStrData=f.readframes(nframes)
        waveData = np.fromstring(voiceStrData,dtype=np.short)#将原始字符数据转换为整数
        #音频数据归一化
        waveData = waveData * 1.0/max(abs(waveData))
        #将音频信号规整乘每行一路通道信号的格式，即该矩阵一行为一个通道的采样点，共nchannels行
        waveData = np.reshape(waveData,[nframes,nchannels]).T # .T 表示转置
        f.close()
        '''
        plt.title("6 channels")
        plt.subplot(321)
        plt.plot(len(waveData[0]),waveData[0])
        plt.subplot(322)
        plt.plot(len(waveData[1]),waveData[1])
        plt.subplot(323)
        plt.plot(len(waveData[2]),waveData[2])
        plt.subplot(324)
        plt.plot(len(waveData[3]),waveData[3])
        plt.subplot(325)
        plt.plot(len(waveData[4]),waveData[4])
        plt.subplot(326)
        plt.plot(len(waveData[5]),waveData[5])
        plt.show()
        '''
        fftdata=np.fft.fft(waveData[1,:])
        fftdata=abs(fftdata)
        
        for i in range(len(fftdata)):
            #fftdata[i]=fftdata[i]-fftdata[449]
            if fftdata[i]<1:
                fftdata[i]=0
        #print(type(fftdata))
        
        '''
        hz_axis=48000*np.arange(500,500+len(fftdata))/len(fftdata)
        temp=420+cnt+1
        plt.subplot(temp)
        plt.plot(hz_axis,fftdata,c='b')
        plt.xlabel('hz')
        plt.ylabel('am')
        '''
        cnt=cnt+1
        data_mfcc=get_mfcc(waveData[1],48000)[0]
        #dict[key+str(cnt)]=fftdata
        dict[key+str(cnt)]=get_mfcc(waveData[1],48000)[0]
        '''
        f1=open(feature_path+key+str(cnt)+"f.txt","w")
        for i in fftdata:
            f1.write(str(i)+"\n")
        f1.close()
        '''
        f2=open(feature_path+key+str(cnt)+"m.txt","w")
        for j in data_mfcc:
            f2.write(str(j)+"\n")
        f2.close()
    plt.show()
df=pd.DataFrame(dict)
print(df)
df2=df.corr()
sns.heatmap(df2,cmap="Greys")
plt.show()

