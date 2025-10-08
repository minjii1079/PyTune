# Author: Kevin Karunaratna
# Inspired by chcicken's "Programming a Guitar Tuner with Python"
# A guitar tuner script that worksy by continuously recording audio from the microphone and
# processing it in real-time to detect the closest note using DFT.

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

# Note detection params
CONCERT_PITCH = 440.0   # Frequency of A4 as equal temperament standard
ALL_NOTES = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]

# Function to get the closest note to a given frequency
def get_closest_note(frequency):
    i = int(np.round(12 * np.log2(frequency / CONCERT_PITCH)))  # Number of half steps from A4 (inverse equal temperament formula)
    closest_note = ALL_NOTES[i % 12] + str(4 + (i + 9) // 12)   # Note name with octave
    closest_pitch = CONCERT_PITCH * 2**(i / 12) # Equal temperament formula
    return closest_note, closest_pitch

audio = pyaudio.PyAudio()

# Open the stream
stream = audio.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=SAMPLE_FREQUENCY,
                    input=True,
                    frames_per_buffer=WINDOW_STEP)

print("Recording started. Press 'q' to stop.")

frames = []

# Continuously records audido until 'q' is pressed
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

