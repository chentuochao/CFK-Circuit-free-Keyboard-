import wave as we
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
import re
from tqdm import tqdm
import json
import sys
from scipy.fftpack import fft,ifft
import math
from matplotlib.patches import Ellipse, Circle


begin = 0 #210400
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default = "output.wav", help="The path of wav file")
args = parser.parse_args()
fd = args.file
maxlen = 0

def wavread():
    global begin
    wavfile =  we.open(fd,"rb")
    params = wavfile.getparams()
    print(params[:4])
    framesra,frameswav= params[2],params[3] #返回采样频率和帧数
    datawav = wavfile.readframes(frameswav) #返回相应帧数的音频字节
    wavfile.close()
    datause = np.fromstring(datawav,dtype = np.int16)
    datause.shape = -1,6
    datause = datause.T #分出六个不同声道的声音
    time = np.arange(0, frameswav) * (1.0/framesra)
    wavfile.close()

    a = datause[2, :]
    for i in range(100, frameswav - 100, 50):  #find the begin of the button strike
        sum1=0
        for j in range(i - 50 , i):
            sum1=sum1+(a[j]/500)**2
        sum2=0
        for j in range(i , i + 50):
            sum2=sum2+(a[j]/400)**2
        #print(sum1, sum2)
        if sum2 - sum1 > 30:
            begin = i - 300
            break   #用于判定是不是一个空音频

    return frameswav,datause,time


def corr(w1, w2):   # the correlation of two sequneces
    f1 = fft(w1)
    f2 = fft(w2)
    f2g = np.conjugate(f2)  #复共轭
    Pw = f1 * f2g
    A = 1/np.abs(Pw)
    result = np.fft.fftshift(ifft(A * Pw))
    return np.abs(result)

def main():
    global begin
    [maxlen, wave, time] = wavread()   # import the wav file
    if begin == 0:   
        return
    leng = 2048

    result = []  # buffer stores the correlation of two wave in different microphones
    dis = []    # buffer to stores the delta distance between two microphones
    #index = 0
    for i in range(1,5):
        for j in range(i+1,5):
            tmp = corr(wave[i, begin:begin+leng], wave[j, begin:begin+leng])
            #plt.figure(index)
            #plt.plot(np.arange(0, leng), tmp)
            result.append(tmp)
            dis.append(np.argmax(tmp)-leng/2)
            print(i , j, np.argmax(tmp))
            #index = index + 1

    #----------------------------Algorithm 1: line cross------------------------- 
    pos = [[-23,23], [23,23], [23,-23], [-23, -23]]  #the position of four microphones
    fig = plt.figure(0)
    ax = fig.add_subplot(111)
    for i in range(0, 4):
        cir1 = Circle(pos[i], radius=5, alpha=0.5)
        ax.add_patch(cir1)
    # the position of keyboard    
    rect = plt.Rectangle((-150,60),360,130)
    ax.add_patch(rect)
    x = np.arange(-400, 400, 2)
    y = np.arange(-50, 350, 2)
    x, y = np.meshgrid(x,y)
    index = -1
    color = ['black', 'red', 'blue', 'green', 'yellow', 'gray']

    for i in range(0,4):
        for j in range(i+1,4):    
            index = index + 1 
            center = ((pos[i][0] + pos[j][0])/2, (pos[i][1] + pos[j][1])/2) #the center point of microphone i and j
            if(pos[i][0] - pos[j][0] != 0): 
                angle_ij =math.atan((pos[i][1] - pos[j][1])/(pos[i][0] - pos[j][0])) + math.pi/2
            else: 
                if(pos[i][1] - pos[j][1] > 0):  angle_ij = math.pi
                else: angle_ij = 0
            dis_ij = math.sqrt((pos[i][0] - pos[j][0])**2 + (pos[i][1] - pos[j][1])**2) #the distance of microphone i and j
            porpo = dis[index] * 340 /(48*dis_ij)
            if(porpo <= 1 and porpo >= -1): delta_angle = math.asin(dis[index] * 340 /(48*dis_ij))
            elif(porpo >= 1): delta_angle = math.asin(1)
            else:  delta_angle = math.asin(-1)
            print(center, dis[index] * 340 /(48*dis_ij), delta_angle, angle_ij)
            x = np.arange(-300, 300, 2)

            if 1:
                if pos[i][0] - pos[j][0] >= 0: angel = angle_ij + delta_angle
                else: angel = angle_ij - delta_angle
                if angel != math.pi/2:
                    y = math.tan(angel)*(x-center[0]) + center[1]
                    plt.plot(x,y,color = color[index])
                else:
                    plt.hlines(center[1], -300, 300, colors = color[index])
            else:
                if pos[i][0] - pos[j][0] >= 0: angel = angle_ij - math.pi - delta_angle
                else: angel = angle_ij - math.pi + delta_angle
                if angel != math.pi/2:
                    y = math.tan(angel)*(x-center[0]) + center[1]
                    plt.plot(x,y, color = color[index])
                else:
                    plt.hlines(center[1], -300, 300, colors = color[index])
            #plt.contour(x, y, , [dis[index]])#np.sqrt((x - pos[i][0])**2 + (y - pos[i][1])**2) - np.sqrt((x - pos[j][0])**2 + (y - pos[j][1])**2), [dis[index]])
            
    ax.set_xlim(-300, 300)
    ax.set_ylim(-50, 250)
    plt.show()

 #----------------------------Algorithm 2: GCC-PATH------------------------- 
'''
    max_pos = [0 , 0]
    max_P = 0
    z1 = []

    for x in range(-400, 400, 2):
        for y in range(50, 350, 2):
                P = 0 
                index = 0
                for i in range(1,5):
                    for j in range(i+1,5):
                        delta1 = math.sqrt((x - pos[i - 1][0])**2 + (y - pos[i - 1][1])**2)
                        delta2 = math.sqrt((x - pos[j - 1][0])**2 + (y - pos[j - 1][1])**2)
                        delta = 1024 + round((delta1 - delta2) * 48 /340) 
                        mycorr = result[index]
                        P = P + mycorr[delta]
                        index = index + 1 
                if P > max_P:
                    max_P = P
                    max_pos = [x , y]
                z1.append(P)
    print(max_pos, max_P)
    z1 = np.array(z1).reshape(400,150)
    
    plt.figure(1)
    plt.subplot(211)
    plt.plot(np.arange(0, leng), (wave[2, begin:begin+leng]))
    plt.subplot(212)
    plt.plot(time, wave[2,:])

    
    result = corr(wave[2, begin:begin+leng], wave[3, begin:begin+leng])
    print(np.max(result), np.argmax(result))
    plt.subplot(311)
    plt.plot(np.arange(0, leng), result)
    plt.subplot(312)
    #plt.plot(np.arange(0, leng), w2)
    plt.subplot(313)
    #plt.plot(np.arange(0, leng), w3)
    #plt.vlines((begin)/48000, -2000,2000,color = 'black' )
    #plt.vlines((212448)/48000, -5000,5000,color = 'black' )
    

    plt.figure(2)
    plt.imshow(z1, cmap='hot', origin='low')
    plt.colorbar(shrink=.83)
    plt.show()
    '''
main()