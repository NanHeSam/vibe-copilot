# vibe-copilot

## demo/slide [link](https://docs.google.com/presentation/d/1rQnr-ek2-Bs42XQw9vbdNLd8mZwwpMPxoWHLqRhhv0w/edit#slide=id.g23bb394c330_0_100)
## How to run it
Right now there are 3 separate program that coordinate with each other via file system. There's a bit delay from the the audio input to the StyleGAN3 generated image. 
- first program will take open the speaker and record 2 seconds audio clip and store under ./output_audio `python input_output.py`
- second program will read the latest audio file generated program #1 and run it through StyleGAN3 and write the key frames under `./samples/<timestamp>/nnn.png`. `python vid_gen.py` I called it vid_gen because eventually I want it to be able to generate a live stream and feed it to the video player. 
- Last program is just a simple web server `python server/server.py` that serve html from the `./samples/*` and choose the most recent generated file to display. The html will refresh every 100ms to make it looks like a video. Eventually, we should be able to generate video endpoint directly playable from video players.


