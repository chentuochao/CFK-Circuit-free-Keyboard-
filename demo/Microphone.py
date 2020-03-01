import pyaudio
import wave
import numpy as np
import time

STATE_IDLE = 0
STATE_DETECT = 1
STATE_RECORD = 2
STATE_RECOGNITION = 3

class Phone(object):
    def __init__(self, RESPEAKER_RATE, RESPEAKER_CHANNELS, RESPEAKER_WIDTH, RESPEAKER_INDEX, CHUNK, CALLBACK, KEYSTROKE_LEN, WINDOW, STEP): 
        self.frame = []
        self.last_data = []
        self.now_data = []
        self.slide_window = WINDOW
        self.slide_step = STEP
        self.keylength = KEYSTROKE_LEN

        self.remain_time = -1
        self.raw_data =[np.array([], dtype = np.int16),np.array([], dtype = np.int16),np.array([], dtype = np.int16),np.array([], dtype = np.int16)]
        self.new_data = np.array([], dtype = np.int16)
        self.__state = STATE_IDLE
        self.rate = RESPEAKER_RATE
        self.channel = RESPEAKER_CHANNELS
        self.chunk = CHUNK
        p = pyaudio.PyAudio()
        self.aud = p 
        self.SampleWidth = p.get_sample_size(p.get_format_from_width(RESPEAKER_WIDTH))
        if CALLBACK == 1:
            self.stream = p.open(
                rate=RESPEAKER_RATE,
                format=p.get_format_from_width(RESPEAKER_WIDTH),
                channels=RESPEAKER_CHANNELS,
                frames_per_buffer=CHUNK,
                input=True,
                input_device_index=RESPEAKER_INDEX,
                stream_callback=self.callback)
        elif CALLBACK == 2:
            self.stream = p.open(
                rate=RESPEAKER_RATE,
                format=p.get_format_from_width(RESPEAKER_WIDTH),
                channels=RESPEAKER_CHANNELS,
                frames_per_buffer=CHUNK,
                input=True,
                input_device_index=RESPEAKER_INDEX,
                stream_callback=self.callback2)
        else:
            self.stream = p.open(
                rate=RESPEAKER_RATE,
                format=p.get_format_from_width(RESPEAKER_WIDTH),
                channels=RESPEAKER_CHANNELS,
                frames_per_buffer=CHUNK,
                input=True,
                input_device_index=RESPEAKER_INDEX,)
        self.stream.start_stream()

    def callback(self, in_data, frame_count, time_info, status):
        if self.__state == STATE_DETECT:
            self.last_data = self.now_data 
            self.now_data = in_data
            self.detect_wave()
        elif self.__state == STATE_RECORD:
            self.last_data = self.now_data 
            self.now_data = in_data
            if self.remain_time > 0: 
                for i in range(0,4):
                    w = np.fromstring(in_data, dtype=np.int16)[(i+1)::6]
                    self.raw_data[i] = np.append(self.raw_data[i], w[0 : self.remain_time])
            self.__state = STATE_RECOGNITION 
        elif self.__state == STATE_RECOGNITION:
            self.last_data = self.now_data 
            self.now_data = in_data 

        #    self.frame.append(in_data)
        #    self.decode(in_data)
        if status: print("Overflow error!, please reset the parameter!")
        return (in_data, pyaudio.paContinue)

    def callback2(self, in_data, frame_count, time_info, status):
        if self.__state == STATE_DETECT:
            self.last_data = self.now_data 
            self.now_data = in_data
            self.detect_wave2()
        elif self.__state == STATE_RECORD:
            self.last_data = self.now_data 
            self.now_data = in_data
            # print(len(self.frame[0])/12, self.remain_time)
            if self.remain_time > 0: self.frame.append(in_data[0 : self.remain_time * self.channel * self.SampleWidth ])
            #print(len(self.frame))
            self.__state = STATE_RECOGNITION 
        elif self.__state == STATE_RECOGNITION:
            self.last_data = self.now_data 
            self.now_data = in_data 

        #    self.frame.append(in_data)
        #    self.decode(in_data)
        if status: print("overflow error!, please reset the parameter!")
        return (in_data, pyaudio.paContinue)

    def detect_wave(self):
        length = self.chunk
        width = self.slide_window
        step = self.slide_step
        if len(self.last_data) > 0:
            last = np.fromstring(self.last_data,dtype=np.int16)[1::6]
            now = np.fromstring(self.now_data,dtype=np.int16)[1::6]
            data = np.append(last[-2*width :], now)
            for i in range(width, length + width, step):
                sum1 = 0
                sum2 = 0
                for j in range(i , i + width):
                    sum1 = sum1 + abs(data[j - width])
                    sum2 = sum2 + abs(data[j])
                #print(sum1, sum2)
                if sum2 - sum1 > 350 * width:
                    begin = i - width - 100
                    if begin < 0: begin = 0
                    self.remain_time = self.keylength - (data.size - begin)
                    for k in range(0,4):
                        last = np.fromstring(self.last_data,dtype=np.int16)[(k+1)::6]
                        now = np.fromstring(self.now_data,dtype=np.int16)[(k+1)::6]
                        data = np.append(last[-2*width :], now)
                        if self.remain_time > 0: self.raw_data[k] = data[begin :]
                        else: self.raw_data[k] = data[begin : begin + self.keylength]
                    self.__state = STATE_RECORD
                    return 1
        return 0

    def detect_wave2(self):
        length = self.chunk
        width = self.slide_window
        step = self.slide_step
        data_size = self.channel * self.SampleWidth
        if len(self.last_data) > 0:
            last = np.fromstring(self.last_data,dtype=np.int16)[1::6]
            now = np.fromstring(self.now_data,dtype=np.int16)[1::6]
            data = np.append(last[-2*width :], now)
            data_np = self.last_data[-2*width*data_size : ] + self.now_data
            for i in range(width, length + width, step):
                sum1 = 0
                sum2 = 0
                for j in range(i , i + width):
                    sum1 = sum1 + abs(data[j - width])
                    sum2 = sum2 + abs(data[j])
                if sum2 - sum1 > 350 * width:
                    begin = i - width - 100
                    if begin < 0: begin = 0
                    #print(data.size)
                    self.remain_time = self.keylength -  (data.size - begin)
                    if self.remain_time > 0: self.frame.append(data_np[begin * data_size   : ])
                    else: self.frame.append(data_np[begin *data_size  : (begin + self.keylength) *data_size])
                    self.__state = STATE_RECORD
                    return

    def get_raw_data(self):
        return self.raw_data
    
    def get_state(self):
        return self.__state
    
    def get_processed_data(self):
        return self.new_data
    
    def get_file_data(self):
        return self.frame

    def begin(self):
        self.__state = STATE_IDLE
    
    def end(self):
        self.__state = STATE_IDLE
        self.clear_frames()
        self.clear_data()
    
    def clear_frames(self):
        self.frame = []
        
    def clear_data(self):
        self.raw_data =[np.array([], dtype = np.int16),np.array([], dtype = np.int16),np.array([], dtype = np.int16),np.array([], dtype = np.int16)]
        self.new_data = np.array([], dtype = np.int16)
    
    def detect_reset(self):
        self.remain_time = -1
        self.clear_data()
        self.clear_frames()
        self.__state = STATE_DETECT
        #self.last_data = np.array([], dtype = np.int16)
        #self.now_data = np.array([], dtype = np.int16)

    def decode(self, data):  # return four channel
        w0 = np.fromstring(data,dtype=np.int16)[0::6]
        self.new_data = np.append(self.new_data, w0)
        for i in range(0,4):
            w = np.fromstring(data,dtype=np.int16)[(i+1)::6]
            self.raw_data[i] = np.append(self.raw_data[i], w)

    def save_file(self, path):
        wf = wave.open(path, 'wb')
        wf.setnchannels(self.channel)
        wf.setsampwidth(self.SampleWidth)
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frame))
        wf.close()
    
    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.aud.terminate()

    def record_s(self, RECORD_SECONDS):
        for i in range(0, int(self.rate / self.chunk * RECORD_SECONDS)):
            data = self.stream.read(self.chunk)
            self.frame.append(data)


def main():
    print("lalalalalala")

if __name__ == '__main__':
    main()

