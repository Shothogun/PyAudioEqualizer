#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 11:10:05 2020

@author: shothogun
"""
import pyaudio
import wave
import time
import sys
import numpy as np
import matplotlib.pyplot as plt
# %% Read audio file

if len(sys.argv) < 2:
    print("Insert a .wav file as a argument")
    sys.exit(-1)

wf = wave.open(sys.argv[1], 'rb')

pya = pyaudio.PyAudio()

# Called whenever a new data is avaiable
def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)

# Open stream using callback
stream = pya.open(format=pya.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback)

# start the stream
stream.start_stream()

# wait for stream to finish
while stream.is_active():
    time.sleep(3)
    
# stop stream 
stream.stop_stream()
stream.close()
wf.close()

# close PyAudio
pya.terminate()