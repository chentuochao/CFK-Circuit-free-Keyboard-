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
from keyboard_map import map_all


parser = argparse.ArgumentParser()
args = parser.parse_args()
maxlen = 0

def wavread(raw_data):
    wavfile =  we.open(raw_data,"rb")
    params = wavfile.getparams()
    # print(params[:4])
    framesra,frameswav= params[2],params[3]
    datawav = wavfile.readframes(frameswav)
    wavfile.close()
    datause = np.fromstring(datawav,dtype = np.int16)
    datause.shape = -1,6
    datause = datause.T
    time = np.arange(0, frameswav) * (1.0/framesra)
    wavfile.close()
    return frameswav,datause,time


def corr(w1, w2):   # the correlation of two sequneces
    f1 = fft(w1)
    f2 = fft(w2)
    f2g = np.conjugate(f2)
    Pw = f1 * f2g
    A = 1/np.abs(Pw)
    result = np.fft.fftshift(ifft(A * Pw))
    return np.abs(result)

def distance_unit_conversion(x):
    return x*340*1000/48000

def give_angle(wave):
       # import the wav file
    leng = 2048

    #----------------------------Algorithm 1: line cross------------------------- 
    '''
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
            porpo = dis[index] * 340 *1000 /(48000*dis_ij)
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
    '''
    #----------------------------Algorithm 2: GCC-PATH------------------------- 
    '''
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

    #----------------------------Algorithm 3: Matrix-------------------------
    result = []  # buffer stores the correlation of two wave in different microphones
    dis = []    # buffer to stores the delta distance between two microphones
    #index = 0
    for i in range(2,5):
            tmp = corr(wave[i, 0:leng], wave[i-1, 0:leng])
            #plt.figure(index)
            #plt.plot(np.arange(0, leng), tmp)
            result.append(tmp)
            dis.append(np.argmax(tmp)-leng/2)
            # print(i,np.argmax(tmp))
            #index = index + 1

    pos = [[-23,23], [23,23], [23,-23], [-23, -23]]  #the position of four microphones
    M = [] #define matrix for position determinant M*d = b
    b = []
    for i in range(1,4):
        M.append([pos[i][0]-pos[i-1][0],pos[i][1]-pos[i-1][1]])

    for i in range(0,3):
        b.append(distance_unit_conversion(dis[i]))
    # print(M)
    # print(b)
    d = []
    d.append(np.linalg.solve([M[0],M[1]],[b[0],b[1]]).tolist())
    #d.append(np.linalg.solve([M[0],M[2]],[b[0],b[2]]))
    d.append(np.linalg.solve([M[1],M[2]],[b[1],b[2]]).tolist())
    #将找到的所有点画在一个园内是最小圆覆盖问题，我们需要让这个圆再大一点。因为现在的计算结果都是一个点，所以暂时不用考虑这个事情
    # print(d)
    return d

def angle_normalized(angle):    #将获得的方向向量归一化,并扭正向量方向
    if angle[1]<0:
        angle[0] = angle[0]*(-1)
        angle[1] = angle[1]*(-1)
    length = np.sqrt(angle[0]**2+angle[1]**2)
    return angle/length


def point_distance_to_line(point,angle):
    c = (point[0]*angle[0]+point[1]*angle[1])*angle
    return (point[0]-c[0])**2+(point[1]-c[1])**2

def find_top8_key(key_dic,angle):
    posibility = []
    for key in key_dic:
        point_distance = point_distance_to_line(key_dic[key],angle)
        posibility.append([int(point_distance),key])
    posibility.sort()
    return posibility[:12]


# 测试时使用的代码
[_, wave, _] = wavread('.\\key_2.wav')
key_dic = map_all()
angle = give_angle(wave)[0]
angle = angle_normalized(angle)
print(angle)

print(find_top8_key(key_dic,angle))




