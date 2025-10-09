# Author: Kevin Karunaratna
# Inspired by chcicken's "Programming a Guitar Tuner with Python"
# A guitar tuner script that worksy by continuously recording audio from the microphone and
# processing it in real-time to detect the closest note using DFT.

import pyaudio
import os
import numpy as np
import scipy.fftpack
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
WINDOW_T_LENGTH = WINDOW_SIZE / SAMPLE_FREQUENCY # Window period (s)
SAMPLE_T_LENGTH = 1 / SAMPLE_FREQUENCY # Period of sample (s)
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

def callback(in_data, frame_count, time_info, status):
    global window_samples
    if status:
        print(status)
    indata = np.frombuffer(in_data, dtype=np.float32)
    if any(indata):
        window_samples = np.concatenate((window_samples, indata)) # Append new samples to the window
        window_samples = window_samples[len(indata):] # Remove old samples to maintain window size 
        magnitudes = abs(scipy.fftpack.fft(window_samples)[:len(window_samples)//2]) # Compute the FFT and take the magnitude. Only the first half since the other half is irrelevant

        for i in range(int(62/(SAMPLE_FREQUENCY/WINDOW_SIZE))): # Remove mains hum which is less than 62 Hz
            magnitudes[i] = 0

        max_index = np.argmax(magnitudes) # Max magnitude index
        max_frequency = max_index * (SAMPLE_FREQUENCY / WINDOW_SIZE) # Convert index to frequency
        closest_note, closest_pitch = get_closest_note(max_frequency) # Find the closest note and pitch from the max frequency

        os.system('cls' if os.name == 'nt' else 'clear') # Clear console
        print(f"Closest Note: {closest_note} {max_frequency:.1f}/{closest_pitch:.1f}") # Print the closest note and its frequency
    
    else:
        print("No input")
    return (None, pyaudio.paContinue)

audio = pyaudio.PyAudio()

# Open the stream
stream = audio.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=SAMPLE_FREQUENCY,
                    input=True,
                    frames_per_buffer=WINDOW_STEP,
                    stream_callback=callback)
# Start the stream
try:
    stream.start_stream()
    while True:
        pass
except KeyboardInterrupt:
    pass
except Exception as e:
    print(e)

    
'''
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
'''
