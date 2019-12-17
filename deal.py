import wave
import numpy as np
import matplotlib.pyplot as plt
import os


#传入wav格式文件和对应键盘的key，输出fft后结果和key
#<script type="text/javascript" src="/eel.js"></script>
#  <script type="text/javascript">
#      eel.dealwith(test.wav,'F');  // 调用Python函数
#</script>
@eel.expose  #Expose this function to js
def dealwith(video_file_path,key):
    f=wave.open(video_file_path,"rb")  
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
    hz_axis=np.arange(0,len(fftdata))
    plt.figure()
    plt.plot(hz_axis,fftdata,c='b')
    plt.xlabel('hz')
    plt.ylabel('am')
    plt.show()


