import wave
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import os
import json
import sys
from tqdm import tqdm
import re
#传入wav格式文件和对应键盘的key，输出fft后结果和key
#<script type="text/javascript" src="/eel.js"></script>
#  <script type="text/javascript">
#      eel.dealwith(test.wav,test.txt);  // 调用Python函数
#</script>
#@eel.expose  #Expose this function to js
'''
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
'''
def deal(wave_file,key_file,result_file):
    f=open(key_file,"r",encoding="utf-8")
    line=f.readline()
    
    if line.startswith(u'\ufeff'):
       line = line.encode('utf8')[3:].decode('utf8')
    line=line.replace("'",'"')
    line=line.replace("\\","")
    #print(line)
    keys=json.loads(line)
    #print(keys)
    line=f.readline()
    key_time=json.loads(line)
    f.close()
    temp=len(key_time)
    for i in range(temp-1,0,-1):
        key_time[i]=key_time[i]-key_time[0]
    key_time[0]=0
    print(key_time)
    wavdata,wavtime=wavread(wave_file)
    a=wavdata[0]
    b=len(a)
    index=0
    temp=0
    plt.figure()
    #print(wavtime)
    plt.plot(wavtime, wavdata[0],color = 'green')
    time0 = -1
    for i in range(0 ,b, 50):
        sum=0
        for j in range(i,i+180):
            sum=sum+(a[j]/1000)**2
        if sum>=100:
            time0 = i - 1280
            break

    if time0 == -1:
        f.close()
        print("error!")
        return
    print("right")
    write_file = "keyboard1\n"
    for i in range(1, len(key_time)):
        x_index = (key_time[i] - key_time[1])/1000 + time0/48000
        plt.vlines(x_index, -35000,35000,color = 'blue' )
        x_index = round(x_index * 48000)
        if keys[i-1]=="r":
            keys[i-1]="enter"
        if keys[i-1]==" ":
            keys[i-1]="space"
        if keys[i-1]=="space" or keys[i-1]=="enter" or (keys[i-1]>="A" and keys[i-1]<="Z"):
            write_file = write_file + str(x_index)+","+keys[i - 1]+"\n"
            #f.write(str(round(i/48,2))+","+keys[index]+"\n")
        else:
            write_file = write_file + str(x_index)+",other\n"
            #f.write(str(round(i/48,2))+",other\n")
    '''
    for i in range(0,b,240):#5ms
        
        sum=0
        for j in range(i,i+240):
            sum=sum+(a[i]/1000)**2
        if index<len(keys) and sum>=40 and i-temp>=240*48:
            #f.write(str(round(i/48,2))+","+str(sum)+"\n")
            if keys[index]=="r":
                keys[index]="enter"
            if keys[index]==" ":
                keys[index]="space"
            if keys[index]=="space" or keys[index]=="enter" or (keys[index]>="A" and keys[index]<="Z"):
                f.write(str(round(i/48,2))+","+keys[index]+"\n")
            else:
                f.write(str(round(i/48,2))+",other\n")
            plt.vlines(i/48000,-35000,35000)
            index+=1
            temp=i
    '''
    print(index, len(keys))
    plt.show()
    a = input("enter")
    plt.close()
    if a == 'y':
        f=open(result_file,"w",encoding="utf-8")
        f.write(write_file)
        f.close()

def wavread(wave_file):
    wavfile =  wave.open(wave_file,"rb")
    params = wavfile.getparams()
    #print(params[:4])
    framesra,frameswav= params[2],params[3]
    datawav = wavfile.readframes(frameswav)
    wavfile.close()
    datause = np.fromstring(datawav,dtype = np.int16)
    datause.shape = -1,6
    datause = datause.T
    time = np.arange(0, frameswav) * (1.0/framesra)
    return datause,time

def deal_all(path):
    filelist=os.listdir(path)
    wavlist=[]
    for filename in filelist:
        filepath=os.path.join(path,filename)
        if (re.match(".*.wav",filename))!=None:
            #print(filename)
            wavlist.append(filepath)
    for wavfile in tqdm(wavlist):
        #print(wavfile)
        m=re.findall(r'(.+?)\.',wavfile)
        txtfile=m[0]+".txt"
        resultfile=m[0]+"result.txt"
        deal(wavfile,txtfile,resultfile)


def test(video_file,key_file):
    y=wave.open(video_file)
    print(y.getnchannels())

#dealwith("./test.wav",'./test.txt')
#video_file=sys.argv[1]
#key_file=sys.argv[2]
#test(video_file,key_file)
#deal(video_file,key_file)
path=sys.argv[1]
deal_all(path)
