#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyaudio
import wave
from scipy import signal
import numpy as np

class Record:
    def __init__(self):
        self.isVoice = False
        self.isQuite = False
        self.isDone = False
        self.threshold = 500
        # Frame to write video
        self.frames = []  # Initialize array to store frames

        self.chunk = 1024  # Record in chunks of 1024 samples
        self.sample_format = pyaudio.paInt16  # 16 bits per sample
        self.channels = 2
        self.fs = 44100  # Record at 44100 samples per second
        self.seconds = 7
        self.filename = "/home/user/sounds_homecredit/record.wav"
        self.p = pyaudio.PyAudio()  # Create an interface to PortAudio

    def detect_voice(self):

        print('Recording')
        stream = self.p.open(format=self.sample_format,
                        channels=self.channels,
                        rate=self.fs,
                        frames_per_buffer=self.chunk,
                        input=True)

        # Frame to detect voice only
        frames_path = np.array([])
        frames_temp = []
        count = 0
        for i in range(self.fs/self.chunk * self.seconds):
            data = stream.read(self.chunk)
            #frames_temp.append(data)
            
            if self.isVoice and not self.isQuite:
                self.frames.append(data)

            data_str = np.fromstring(data, dtype=np.int16)
            # print(data_str)
            # print(len(data_str))
            frames_path = np.append(frames_path, data_str)

            # 0.02s
            if frames_path.size >= int(self.fs / 50):
                f, t, Sxx = signal.spectrogram(frames_path, fs=self.fs)

                # spectrum, freqs, t, img = plt.specgram(frames_path, Fs=self.fs)
                # # print(spectrum.shape)
                #
                avg_amplitude = np.mean(Sxx)
                #print("average amplitude: ", avg_amplitude)
                if avg_amplitude > self.threshold:
                    self.isVoice = True
                    #self.frames += frames_temp
                    #print("voice")
                
                if avg_amplitude < 200 and self.isVoice:
                    count += 1
                
                if count >= 100:
                    self.isQuite = True

                if self.isVoice and self.isQuite:
                    break
                
                #frames_temp = []
                # recreate window to detect voice
                frames_path = np.array([])


        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        self.p.terminate()
        self.isDone = True
        #print("done record")

    # Save the recorded data as a WAV file
    def save_wav(self):
        if self.isVoice:
            wf = wave.open(self.filename, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.sample_format))
            wf.setframerate(self.fs)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            #print('Saved')


# r = Record()
# r.detect_voice()
# if(r.isVoice):
#     print("voice detected")
#     r.save_wav()

