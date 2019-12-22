import wave as we
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
import re
from tqdm import tqdm
import json
import sys

def deal(wavfile, txtfile):
    global mode
    wavfile =  we.open(wavfile,"rb")
    params = wavfile.getparams()
    #print(params[:4])
    framesra,frameswav= params[2],params[3]
    datawav = wavfile.readframes(frameswav)
    wavfile.close()
    datause = np.fromstring(datawav,dtype = np.int16)
    datause.shape = -1,6
    datause = datause.T
    time = np.arange(0, frameswav) * (1.0/framesra)
    #return datause,time
    plt.plot(time, datause[0],color = 'green')
    a = datause[0]
    txt = open(txtfile,"r",encoding="utf-8")
    line = txt.readline() # 整行读取数据
    keys = json.loads(line)
    #print(keys)
    line = txt.readline() # 整行读取数据
    keytime = json.loads(line)
    wavfile.close()
    txt.close()

    #print(keytime)
    calibration = 0
    begin = keytime[0] * 48
    #plt.vlines((begin-1000)/48000, -35000,35000,color = 'black' )
    #plt.vlines((begin + 4800)/48000, -35000,35000,color = 'black' )

    for i in range(begin-1000, begin + 4800, 10):
        sum1=0
        for j in range(i - 50 , i):
            sum1=sum1+(a[j]/500)**2
        sum2=0
        for j in range(i , i + 50):
            sum2=sum2+(a[j]/500)**2
        #print(sum1, sum2)
        if sum2 - sum1 > 100:
            calibration = - keytime[0] + (i - 1300) / 48
            break
    print(calibration)
    if mode == '1':
        keytime2 = [round(i+calibration) for i in keytime]
        txt = open(txtfile,"w",encoding="utf-8")
        txt.write(str(keys)+'\n')
        txt.write(str(keytime2)+'\n')
        txt.close()
    else: keytime2 = keytime
    for i in range(0, len(keytime2)):
        x_index = (keytime2[i] )/1000
        plt.vlines(x_index, -35000,35000,color = 'blue' )
    plt.show()

def main():
    path = "./raw"
    filelist=os.listdir(path)
    wavlist=[]
    for filename in filelist:
        filepath=os.path.join(path,filename)
        if (re.match(".*.wav",filename))!=None:
            #print(filename)
            wavlist.append(filepath)
    for wavfile in tqdm(wavlist):
        print(wavfile)
        m=re.findall(r'(.+?)\.',wavfile)
        txtfile=m[0]+".txt"
        deal(wavfile,txtfile)
        input("next->")

mode = sys.argv[1]
if mode == '1':
    print("update mode")
else: print("only viwe mode")
main()
