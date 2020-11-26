"""
Project: Python Basic Audio Equalizer

Python 3.8.3

@author: shothogun
"""
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QMessageBox,
                             QMainWindow, QAction, qApp, QApplication, QMenu,
                             QTextEdit, QFileDialog, QHBoxLayout, QFrame,
                             QSplitter)
from PyQt5.QtGui import QIcon
from pathlib import Path
from equalizer_bar import EqualizerBar

import numpy as np
import wave
from pydub import AudioSegment
import struct
import pyaudio
from scipy.fftpack import rfft, fft

import sys
import time

import filters

class AudioStream(QMainWindow):
    def __init__(self):
        # Initialize variables
        self.fileOpened = False
        self.streaming = True
        self.stream = None

        # Init App Widget
        super().__init__()
        self.equalize_width = 512
        self.equalizer = EqualizerBar(self.equalize_width, ['#0C0786', '#40039C', '#6A00A7', '#8F0DA3', '#B02A8F', '#CA4678', '#E06461',
                                          '#F1824C', '#FCA635', '#FCCC25', '#EFF821', '#EFF821','#EFF821','#EFF821','#EFF821','#EFF821','#EFF821',
                                          '#EFF821','#EFF821','#EFF821','#EFF821','#EFF821','#EFF821', '#EFF821'])

        self.setCentralWidget(self.equalizer)

        playBtn = QPushButton('Play', self)
        playBtn.clicked.connect(self.startStream)
        playBtn.resize(playBtn.sizeHint())
        playBtn.move(400, 600)

        pauseBtn = QPushButton('Stop', self)
        pauseBtn.clicked.connect(self.stopStream)
        pauseBtn.resize(pauseBtn.sizeHint())
        pauseBtn.move(500, 600)

        # Application Menubar
        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.openFileDialog)

        exitAct = QAction('Exit', self)
        exitAct.setShortcut('ESC')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.close)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(exitAct)

        # Status Bar below
        self.statusBar().showMessage('Idle')

        self.setGeometry(200, 300, 1000, 1000)
        self.setWindowTitle('PyEqualizer')
        self.show()

        sys.exit(app.exec_())

    def startStream(self):
        if not self.fileOpened:
            QMessageBox.question(self, 'Warning!', "Please, choose a file",
                                 QMessageBox.Yes)
            return

        if self.stream != None and self.stream.is_active():
            return

        print("Start streaming")

        self.equalizer.setDecayFrequencyMs(100)
        self._timer = QtCore.QTimer()
        self._timer.setInterval(100)
        self._timer.timeout.connect(self.update_values)
        self._timer.start()

        self.streaming = True
        # PyAudio Setting
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024 * 2

        # Play audio on-the-fly
        def callback(in_data, frame_count, time_info, status):
            self.data = self.wf.readframes(frame_count)
            self.frame_count = frame_count
            return (self.data, pyaudio.paContinue)

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  output=True,
                                  stream_callback=callback,
                                  frames_per_buffer=self.CHUNK)

        self.stream.start_stream()
        #self.plot_audio()

    def stopStream(self):
        print("Stop Streaming")
        if self.stream == None:
            return

        self.stream.stop_stream()

    def update_values(self):
        if self.stream.is_active():
            byte_data = self.data
            data_int_16 = np.frombuffer(byte_data, dtype='<i2')
            data_int_16 = data_int_16 * np.hamming(len(data_int_16))
            fft_data = np.abs(fft(data_int_16)[0:self.CHUNK//2])/((self.CHUNK//4)*self.CHUNK)
            au = fft_data[:(self.CHUNK//4):(self.CHUNK//4)//self.equalize_width]
            au = [i*100 for i in au]
            au = list(map(lambda i: 100 if i > 100 else i, au))
            self.equalizer.setValues([
                v for v in au
                ])

    def plotAudio(self):
        print("Plotting Audio")

    def openFileDialog(self):
        home_dir = str(Path.home())
        fname = QFileDialog.getOpenFileName(self, 'Open file', home_dir)

        if fname[0]:
            self.music_sample_file = fname[0]
            self.wf = wave.open(fname[0], 'rb')
            self.fileOpened = True

            if self.wf.getnchannels() > 1:
                print("File is stereo. Converting...")
                sound = AudioSegment.from_wav(self.music_sample_file)
                sound = sound.set_channels(1)
                sound.export(self.music_sample_file, format="wav")
                self.wf.close()
                self.wf = wave.open(self.music_sample_file, "rb")

            print("Music file: " + self.music_sample_file)

    def closeEvent(self, event):
        print("Are you sure?")
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def start(self):
        self.timer = QtCore.QTimer()
        print("Hello")

    def set_plotdata(self, name, data_x, data_y):
        print("Heelo")

    def update(self):
        self.stream.write(self.data)
        print("Heelo")

    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(20)
        self.start()

    def close(self):
        if not self.stream == None:
            self.stream.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    audio_app = AudioStream()
    audio_app.animation()
    audio_app.close()
    sys.exit(app.exec_())
