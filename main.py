import pyaudio
import os
import numpy as np
import scipy.fftpack
import wave
import keyboard

# Audio params
#FORMAT = pyaudio.paInt16
#CHANNELS = 1
#RATE = 44100
#CHUNK = 1024
#WAVE_OUTPUT_FILENAME = "continuous_recording.wav"

SAMPLE_FREQUENCY = 44100
WINDOW_SIZE = 44100 # 1 second window
WINDOW_STEP = 21050 # 0.5 second step
WINDOW_T_LENGTH = WINDOW_SIZE / SAMPLE_FREQUENCY # Period of the window in seconds
SAMPLE_T_LENGTH = 1 / SAMPLE_FREQUENCY # Period of the sample in seconds
window_samples = [0 for _ in range(WINDOW_SIZE)]



audio = pyaudio.PyAudio()

# Open the stream
stream = audio.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=SAMPLE_FREQUENCY,
                    input=True,
                    frames_per_buffer=WINDOW_STEP)

print("Recording started. Press 'q' to stop.")

frames = []

# Record until 'q' is pressed (allows for continuous recording)
while True:
        data = stream.read(WINDOW_STEP)
        frames.append(data)
        if keyboard.is_pressed('q'): # Stop when 'q' is pressed
            print("Stopping recording.")
            break

# Stop and close the stream
stream.stop_stream()
stream.close()
audio.terminate()

