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
#parser.add_argument("-f", "--file", default = ".\\eval\\key_E\\key_2.wav", help="The path of wav file")
args = parser.parse_args()
# fd = args.file
maxlen = 0

def wavread(raw_data):
    print(raw_data)
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

    leng = 2048
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
            print(i,np.argmax(tmp))
            #index = index + 1

    pos = [[-23,23], [23,23], [23,-23], [-23, -23]]  #the position of four microphones
    M = [] #define matrix for position determinant M*d = b
    b = []
    for i in range(1,4):
        M.append([pos[i][0]-pos[i-1][0],pos[i][1]-pos[i-1][1]])

    for i in range(0,3):
        b.append(distance_unit_conversion(dis[i]))
    print(M)
    print(b)
    d = []
    d.append(np.linalg.solve([M[0],M[1]],[b[0],b[1]]).tolist())
    #d.append(np.linalg.solve([M[0],M[2]],[b[0],b[2]]))
    d.append(np.linalg.solve([M[1],M[2]],[b[1],b[2]]).tolist())
    #将找到的所有点画在一个园内是最小圆覆盖问题，我们需要让这个圆再大一点。因为现在的计算结果都是一个点，所以暂时不用考虑这个事情
    print(d)
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
print(wave)
key_dic = map_all()
angle = give_angle(wave)[0]
angle = angle_normalized(angle)
print(angle)

print(find_top8_key(key_dic,angle))




