import sounddevice as sd
import numpy as np
import wavio

# Sampling frequency
fs = 44100  

# Duration of recording
duration = 2  # 2 seconds

# Number of channels (1 for mono, 2 for stereo)
channels = 1

# Define a callback function to record the audio in chunks
def callback(indata, frames, time, status):
    filename = "audio_segment.wav"
    wavio.write(filename, indata, fs, sampwidth=3)

# Create an input stream with the callback
with sd.InputStream(device=0, callback=callback, channels=channels, samplerate=fs) as stream:
    print("Recording for {} seconds...".format(duration))
    sd.sleep(duration * 1000)

print("Recording complete!")


