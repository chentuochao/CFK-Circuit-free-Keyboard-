import wave
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import os
import json
import sys
from tqdm import tqdm
#传入wav格式文件和对应键盘的key，输出fft后结果和key
#<script type="text/javascript" src="/eel.js"></script>
#  <script type="text/javascript">
#      eel.dealwith(test.wav,test.txt);  // 调用Python函数
#</script>
#@eel.expose  #Expose this function to js
def dealwith(video_file,key_file):
    f=wave.open(video_file,"rb")  
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

    time=np.arange(0,nframes)*(1.0/framerate)
    plt.plot(time,waveData[0,:],c='b')
    plt.xlabel('time')
    plt.ylabel('am')
    plt.show()

    fftdata=np.fft.fft(waveData[0,:])
    fftdata=abs(fftdata)
    print(type(fftdata))
    hz_axis=np.arange(0,len(fftdata))
    plt.figure()
    plt.plot(hz_axis,fftdata,c='b')
    plt.xlabel('hz')
    plt.ylabel('am')
    plt.show()

def deal(wave_file,key_file):
    f=open(key_file,"r");
    line=f.readline()
    keys=json.loads(line)
    print(keys)
    line=f.readline()
    key_time=json.loads(line)
    f.close()
    temp=len(key_time)
    for i in range(temp-1,0,-1):
        key_time[i]=key_time[i]-key_time[0]
    key_time[0]=0
    print(key_time)
    y,sr=librosa.load(video_file,sr=None)
    a=y.tolist()
    b=len(a)
    f=open("./temp.txt","w")
    index=1
    temp=0
    for i in range(1,b,240):#5ms
        '''
        if index<len(key_time) and a[i]-a[i-1]>=0.005 and abs(i/48-key_time[index])<400:
            print(key_time[index])
            f.write(str(i)+","+keys[index-1]+"\n")
            index=index+1
        '''
        sum=0
        for j in range(i,i+240):
            sum=sum+a[i]**2
        if index<len(key_time) and sum>=0.01 and i-temp>=300*48:
            #f.write(str(round(i/48,2))+","+str(sum)+"\n")
            f.write(str(i)+","+keys[index-1]+"\n")
            index+=1
            temp=i
    f.close()











def test(video_file,key_file):
    y,sr=librosa.load(video_file,sr=None)
    #S=np.abs(librosa.stft(y))
    plt.figure()
    librosa.display.waveplot(y,sr)
    #plt.colorbar()
    plt.show()


#dealwith("./test.wav",'./test.txt')
video_file=sys.argv[1]
key_file=sys.argv[2]
#test(video_file,key_file)
deal(video_file,key_file)
