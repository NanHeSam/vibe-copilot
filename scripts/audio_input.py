import sounddevice as sd
import numpy as np

# Define a ring buffer to hold the last N RMS values
N = 100
ring_buffer = np.zeros(N)
pointer = 0

# Noise level threshold (you may need to adjust this value)
NOISE_THRESHOLD = 25

# Callback function to calculate RMS
def audio_callback(indata, frames, time, status):
    global pointer
    volume_norm = np.linalg.norm(indata) * 10
    ring_buffer[pointer] = volume_norm
    pointer = (pointer + 1) % N
    avg_noise_level = np.mean(ring_buffer)
    if avg_noise_level > NOISE_THRESHOLD:
        print("noisy")
    else:
    	print("quiet")

# Set your microphone device ID to 0
MIC_DEVICE_ID = 0

# Open a stream with the audio input device (microphone)
with sd.InputStream(device=MIC_DEVICE_ID, channels=1, callback=audio_callback, samplerate=44100):
    print("Monitoring noise level...")
    while True:
        sd.sleep(1000)
