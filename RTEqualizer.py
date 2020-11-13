import pyaudio
import librosa as lb
import os
import struct
import wave
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import time
from tkinter import TclError

# to display in separate Tk window


# constants
CHUNK = 1024 * 2             # samples per frame
FORMAT = pyaudio.paInt16     # audio format (bytes per sample?)
CHANNELS = 1                 # single channel for microphone
RATE = 44100                 # samples per second

# create matplotlib figure and axes
fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))

wf = wave.open('./SoundSamples/music_sample.wav', 'rb')
data=[]
# pyaudio class instance
pya = pyaudio.PyAudio()

# stream object to get data from microphone
# stream = p.open(
#     format=FORMAT,
#     channels=CHANNELS,
#     rate=RATE,
#     output=True,
#     frames_per_buffer=CHUNK
# )
# Called whenever a new data is avaiable
# def callback(in_data, frame_count, time_info, status):
#     data = wf.readframes(frame_count)
#     return (data, pyaudio.paContinue)

# Open stream using callback
stream = pya.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)

# variable for plotting
x = np.arange(0, 2 * CHUNK, 2)       # samples (waveform)
xf = np.linspace(0, RATE, CHUNK)     # frequencies (spectrum)

# create a line object with random data
line, = ax1.plot(x, np.random.rand(CHUNK), '-', lw=2)

# create semilogx line for spectrum
line_fft, = ax2.semilogx(xf, np.random.rand(CHUNK), '-', lw=2)

# format waveform axes
ax1.set_title('AUDIO WAVEFORM')
ax1.set_xlabel('samples')
ax1.set_ylabel('volume')
ax1.set_ylim(0, 255)
ax1.set_xlim(0, 2 * CHUNK)
plt.setp(ax1, xticks=[0, CHUNK, 2 * CHUNK], yticks=[0, 128, 255])

# format spectrum axes
ax2.set_xlim(20, RATE / 2)

# show the plot
plt.show(block=False)

print('stream started')

frame_count = 0
start_time = time.time()

data = wf.readframes(CHUNK)
while len(data) > 0:
    #stream.write(data)
    data = wf.readframes(CHUNK)
    
    # convert data to integers, make np array, then offset it by 127
    data_int = struct.unpack(str(2 * CHUNK) + 'H', data)
    
    # create np array and offset by 128
    data_np = np.array(data_int, dtype='b')[::2] + 128
    
    line.set_ydata(data_np)
    
    # compute FFT and update line
    yf = fft(data_int)
    line_fft.set_ydata(np.abs(yf[0:CHUNK])  / (65536 * CHUNK))
    
    # update figure canvas
    try:
        fig.canvas.draw()
        fig.canvas.flush_events()
        frame_count += 1
        
    except TclError:
        
        # calculate average frame rate
        frame_rate = frame_count / (time.time() - start_time)
        
        print('stream stopped')
        print('average frame rate = {:.0f} FPS'.format(frame_rate))
        break
    
stream.stop_stream()
stream.close()

wf.close()
pya.terminate()
