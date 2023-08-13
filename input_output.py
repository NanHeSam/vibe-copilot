import sounddevice as sd
import numpy as np
import wavio
import time

# Sampling frequency
fs = 44100  

# Duration of recording
duration = 2  # 2 seconds

# Number of channels (1 for mono, 2 for stereo)
channels = 1


# Define a callback function to record the audio in chunks
def callback(indata):
    filename = "audio_segment.wav"
    wavio.write(filename, indata, fs, sampwidth=3)



def record_audio(duration, samplerate=44100):
    """Record audio for a given duration and samplerate."""
    print("Recording...")
    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()  # Wait until recording is finished
    timestring = time.strftime('%H:%M:%S')
    filename = f"output_audio/audio_segment{timestring}.wav"
    wavio.write(filename, audio_data, fs, sampwidth=3)
    print("Recording finished!")
    return audio_data

def playback_audio(audio_data, samplerate=44100):
    """Playback recorded audio data."""
    print("Playing back...")
    sd.play(audio_data, samplerate=samplerate)
    sd.wait()  # Wait until audio playback is finished
    print("Playback finished!")

if __name__ == "__main__":
    # Record for 5 seconds
    while True:
        recorded_data = record_audio(1)
    
    # Playback the recorded data
    # playback_audio(recorded_data)






# # Create an input stream with the callback
# with sd.InputStream(device=0, callback=callback, channels=channels, samplerate=fs) as stream:
#     print("Recording for {} seconds...".format(duration))
#     sd.sleep(duration * 1000)

# print("Recording complete!")


