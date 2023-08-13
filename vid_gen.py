import requests
import pickle
import torch
import os
import numpy as np
# import matplotlib.pyplot as plt
from subprocess import Popen, PIPE
import glob
import librosa
from scipy.io import wavfile

import time
import torchvision.transforms.functional as TF

from PIL import Image

# assume there's a model model.pkl
model_file = './model_flower.pkl'
device = torch.device('mps')
seed =  42
truncation_psi = 0.5
effect_strength =  1
interp_frames =  4
freqs = 'all'

audio_file = './audio_2s.wav'
AUDIO_PATH = '/Users/samhe/projects/agi_house_imagen/vibe-copilot/output_audio/*.wav'

def load_model():
    with open(model_file, 'rb') as f:
        G = pickle.load(f)['G_ema'].to(device)
    zs = torch.randn([10000, G.mapping.z_dim], device=device)
    w_stds = G.mapping(zs, None).std(0)
    return zs, w_stds, G

def load_audio_feature(G):
    audios = glob.glob(AUDIO_PATH)
    latest_audio = max(audios, key=lambda f: os.path.getctime(f))
    
    arr, fr = librosa.load(latest_audio)
    stft=librosa.feature.melspectrogram(y=arr,
                               sr=fr,
                               n_fft=2048,
                               hop_length=G.mapping.z_dim*4,
                               n_mels=G.mapping.z_dim)
    # print(stft.shape)
    
    stft = torch.tensor(stft - stft.min())/(stft.max()-stft.min())
    # stft = torch.log(torch.tensor(stft).abs())
    return stft


def generate_frames(stft, G):
    zq = []
    with torch.no_grad():
        timestring = time.strftime('%Y%m%d%H%M%S')

        # create key frames 
        for i in range(stft.size(-1)):
            frame = stft[:,i].T.to(device)
            z = torch.mean(G.mapping(frame.unsqueeze(0), None, truncation_psi=truncation_psi), dim=0)
            zq.append(z.unsqueeze(0)*effect_strength)

        count = 0
        # loops keyframe and interpolate keyframes
        for k in range(len(zq)-1):
            i_val = torch.linspace(0,1,interp_frames).to(device)
            for interpolation in i_val:
                interp = torch.lerp(zq[k], zq[k+1], interpolation)
                images = G.synthesis(interp)
                images = ((images + 1)/2).clamp(0,1)
                pil_image = TF.to_pil_image(images[0].cpu())


                os.makedirs(f'samples/{timestring}', exist_ok=True)
                pil_image.save(f'samples/{timestring}/{count:04}.png')
                count+=1
    return timestring

def produce_video(timestring, fps=5):
    frames = []

    for i in sorted(os.listdir(f'samples/{timestring}')): #
        frames.append(Image.open(f"samples/{timestring}/{i}"))
    p = Popen(['ffmpeg', '-y', '-f', 'image2pipe', '-vcodec', 'png', '-r', str(fps), '-i', '-', '-vcodec', 'libx264', '-r', str(fps), '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'veryslow', 'video.mp4'], stdin=PIPE)
    for im in frames:
        im.save(p.stdin, 'PNG')
    p.stdin.close()
    p.wait()


if __name__ == "__main__":
    zs, w_stds, G = load_model()
    while True:
        stft = load_audio_feature(G)
        timestring = generate_frames(stft, G)
        # video =  produce_video(timestring)
