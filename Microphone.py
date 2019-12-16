import pyaudio
import wave
import numpy as np
import time

class Phone(object):
    def __init__(self, RESPEAKER_RATE, RESPEAKER_CHANNELS,RESPEAKER_WIDTH,RESPEAKER_INDEX,CHUNK,CALLBACK): 
        self.frame = []
        self.raw_data =[np.array([], dtype = np.int16),np.array([], dtype = np.int16),np.array([], dtype = np.int16),np.array([], dtype = np.int16)]
        self.new_data = np.array([], dtype = np.int16)
        self.recording = 0
        self.rate = RESPEAKER_RATE
        self.channel = RESPEAKER_CHANNELS
        self.chunk = CHUNK
        p = pyaudio.PyAudio()
        self.aud = p 
        self.SampleWidth = p.get_sample_size(p.get_format_from_width(RESPEAKER_WIDTH))
        if CALLBACK:
            self.stream = p.open(
                rate=RESPEAKER_RATE,
                format=p.get_format_from_width(RESPEAKER_WIDTH),
                channels=RESPEAKER_CHANNELS,
                frames_per_buffer=CHUNK,
                input=True,
                input_device_index=RESPEAKER_INDEX,
                stream_callback=self.callback)
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
        if self.recording: 
            self.frame.append(in_data)
            print(status)
        return (in_data, pyaudio.paContinue)

    def begin(self):
        self.recording = 1
    
    def end(self):
        self.recording = 0

    def clear_frames(self):
        self.frame = []
        
    def clear_data(self):
        self.raw_data =[np.array([], dtype = np.int16),np.array([], dtype = np.int16),np.array([], dtype = np.int16),np.array([], dtype = np.int16)]
        self.new_data = np.array([], dtype = np.int16)

    def decode(self, data):  # return four channel
        w0 = np.fromstring(data,dtype=np.int16)[0::6]
        new_data = np.append(new_data, wo)
        for i in range(0,4):
            w = np.fromstring(data,dtype=np.int16)[(i+1)::6]
            raw_data[i] = np.append(raw_date[i], w)

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
    WAVE_OUTPUT_FILENAME = r"./raw/Key"+str(time.time())+".wav"
    #WAVE_OUTPUT_FILENAME = WAVE_OUTPUT_FILENAME.replace('.','_')
    save_file(WAVE_OUTPUT_FILENAME, frame)

if __name__ == '__main__':
    main()

