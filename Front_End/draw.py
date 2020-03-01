import wave as we
import numpy as np
import matplotlib.pyplot as plt
import argparse

#copy from tuochao
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", default = "output.wav", help="The path of wav file")
args = parser.parse_args()
fd = args.file


def wavread():
    wavfile =  we.open(fd,"rb")
    params = wavfile.getparams()
    print(params[:4])
    framesra,frameswav= params[2],params[3]
    datawav = wavfile.readframes(frameswav)
    wavfile.close()
    datause = np.fromstring(datawav,dtype = np.int16)
    datause.shape = -1,6
    datause = datause.T
    time = np.arange(0, frameswav) * (1.0/framesra)
    return datause,time

def main():
    wavdata,wavtime = wavread()
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
    
main()
