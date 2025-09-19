import pyaudio
import wave
import keyboard

# Audio params
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
WAVE_OUTPUT_FILENAME = "continuous_recording.wav"

audio = pyaudio.PyAudio()

# Open the stream
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

print("Recording started. Press 'q' to stop.")

frames = []

# Record until 'q' is pressed (allows for continuous recording)
while True:
        data = stream.read(CHUNK)
        frames.append(data)
        if keyboard.is_pressed('q'): # Stop when 'q' is pressed
            print("Stopping recording.")
            break

# Stop and close the stream
stream.stop_stream()
stream.close()
audio.terminate()

# Save the recorded data as a WAV file
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

print(f"Recording saved to {WAVE_OUTPUT_FILENAME}")