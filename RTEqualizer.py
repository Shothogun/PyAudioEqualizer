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
                             QSplitter, QSlider)
from PyQt5.QtGui import QIcon
from pathlib import Path
from equalizer_bar import EqualizerBar
from scipy import signal

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
        self.equalizer = EqualizerBar(self.equalize_width, [
            '#0C0786', '#40039C', '#6A00A7', '#8F0DA3', '#B02A8F', '#CA4678',
            '#E06461', '#F1824C', '#FCA635', '#FCCC25', '#EFF821', '#EFF821',
            '#EFF821', '#EFF821', '#EFF821', '#EFF821', '#EFF821', '#EFF821',
            '#EFF821', '#EFF821', '#EFF821', '#EFF821', '#EFF821', '#EFF821'
        ])

        self.setCentralWidget(self.equalizer)

        sld_base_position = 10

        sld_32Hz = QSlider(Qt.Horizontal, self)
        sld_32Hz.setFocusPolicy(Qt.NoFocus)
        sld_32Hz.setGeometry(sld_base_position, 40, 150, 30)
        sld_32Hz.setValue(50)
        sld_32Hz.setTickInterval(10)
        sld_32Hz.setSingleStep(10)
        sld_32Hz.valueChanged[int].connect(self.changeValue)
        sld_32Hz.setTickPosition(QSlider.TicksBelow)


        sld_65Hz = QSlider(Qt.Horizontal, self)
        sld_65Hz.setFocusPolicy(Qt.NoFocus)
        sld_65Hz.setGeometry(sld_base_position+200, 40, 150, 30)
        sld_65Hz.setValue(50)
        sld_65Hz.setTickInterval(10)
        sld_65Hz.setSingleStep(10)
        sld_65Hz.valueChanged[int].connect(self.changeValue)
        sld_65Hz.setTickPosition(QSlider.TicksBelow)

        sld_125Hz = QSlider(Qt.Horizontal, self)
        sld_125Hz.setFocusPolicy(Qt.NoFocus)
        sld_125Hz.setGeometry(sld_base_position+400, 40, 150, 30)
        sld_125Hz.setValue(50)
        sld_125Hz.setTickInterval(10)
        sld_125Hz.setSingleStep(10)
        sld_125Hz.valueChanged[int].connect(self.changeValue)
        sld_125Hz.setTickPosition(QSlider.TicksBelow)

        sld_250Hz = QSlider(Qt.Horizontal, self)
        sld_250Hz.setFocusPolicy(Qt.NoFocus)
        sld_250Hz.setGeometry(sld_base_position+600, 40, 150, 30)
        sld_250Hz.setValue(50)
        sld_250Hz.setTickInterval(10)
        sld_250Hz.setSingleStep(10)
        sld_250Hz.valueChanged[int].connect(self.changeValue)
        sld_250Hz.setTickPosition(QSlider.TicksBelow)

        sld_500Hz = QSlider(Qt.Horizontal, self)
        sld_500Hz.setFocusPolicy(Qt.NoFocus)
        sld_500Hz.setGeometry(sld_base_position+800, 40, 150, 30)
        sld_500Hz.setValue(50)
        sld_500Hz.setTickInterval(10)
        sld_500Hz.setSingleStep(10)
        sld_500Hz.valueChanged[int].connect(self.changeValue)
        sld_500Hz.setTickPosition(QSlider.TicksBelow)

        sld_1kHz = QSlider(Qt.Horizontal, self)
        sld_1kHz.setFocusPolicy(Qt.NoFocus)
        sld_1kHz.setGeometry(sld_base_position, 100, 150, 30)
        sld_1kHz.setValue(50)
        sld_1kHz.setTickInterval(10)
        sld_1kHz.setSingleStep(10)
        sld_1kHz.valueChanged[int].connect(self.changeValue)
        sld_1kHz.setTickPosition(QSlider.TicksBelow)

        sld_2kHz = QSlider(Qt.Horizontal, self)
        sld_2kHz.setFocusPolicy(Qt.NoFocus)
        sld_2kHz.setGeometry(sld_base_position+200, 100, 150, 30)
        sld_2kHz.setValue(50)
        sld_2kHz.setTickInterval(10)
        sld_2kHz.setSingleStep(10)
        sld_2kHz.valueChanged[int].connect(self.changeValue)
        sld_2kHz.setTickPosition(QSlider.TicksBelow)

        sld_4kHz = QSlider(Qt.Horizontal, self)
        sld_4kHz.setFocusPolicy(Qt.NoFocus)
        sld_4kHz.setGeometry(sld_base_position+400, 100, 150, 30)
        sld_4kHz.setValue(50)
        sld_4kHz.setTickInterval(10)
        sld_4kHz.setSingleStep(10)
        sld_4kHz.valueChanged[int].connect(self.changeValue)
        sld_4kHz.setTickPosition(QSlider.TicksBelow)

        sld_8kHz = QSlider(Qt.Horizontal, self)
        sld_8kHz.setFocusPolicy(Qt.NoFocus)
        sld_8kHz.setGeometry(sld_base_position+600, 100, 150, 30)
        sld_8kHz.setValue(50)
        sld_8kHz.setTickInterval(10)
        sld_8kHz.setSingleStep(10)
        sld_8kHz.valueChanged[int].connect(self.changeValue)
        sld_8kHz.setTickPosition(QSlider.TicksBelow)

        sld_16kHz = QSlider(Qt.Horizontal, self)
        sld_16kHz.setFocusPolicy(Qt.NoFocus)
        sld_16kHz.setGeometry(sld_base_position+800, 100, 150, 30)
        sld_16kHz.setValue(50)
        sld_16kHz.setTickInterval(10)
        sld_16kHz.setSingleStep(10)
        sld_16kHz.valueChanged[int].connect(self.changeValue)
        sld_16kHz.setTickPosition(QSlider.TicksBelow)

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

            # Filter window
            win = signal.blackman(50)

            # Audio Chunck byte->int16
            # and interpolation constants
            # sampling
            data_int = np.frombuffer(self.data, dtype='<i2').astype(float)
            self.min_val= data_int.min()
            self.max_val = data_int.max()

            # Apllying Filter
            data_int = np.convolve(win, data_int)

            # Audio interpolation and 
            # reconstruction to int 16
            data_int = np.interp(
                data_int, (data_int.min(), data_int.max()), 
                (self.min_val, self.max_val)).astype(np.int16)[0:self.CHUNK]
                
            # Converts audio int->byte sequence
            in_byte_data = data_int.tobytes()
            self.data = in_byte_data
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
            fft_data = np.abs(fft(data_int_16)[0:self.CHUNK // 2]) / (
                (self.CHUNK // 4) * self.CHUNK)
            au = fft_data[:(self.CHUNK // 4):(self.CHUNK // 4) //
                          self.equalize_width]
            au = [i * 100 for i in au]
            au = list(map(lambda i: 100 if i > 100 else i, au))
            self.equalizer.setValues([v for v in au])

    def changeValue(self, value):
        print(value)
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

    def set_plotdata(self, name, data_x, data_y):
        print("Heelo")

    def close(self):
        if not self.stream == None:
            self.stream.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    audio_app = AudioStream()
    audio_app.animation()
    audio_app.close()
    sys.exit(app.exec_())
