from moviepy.editor import *
import VidMaker
import helper
import math
from aeneas.executetask import ExecuteTask
from aeneas.task import Task
import random
audio_clip = r'C:\Users\fergu\Documents\PycharmProjects\Tiktok Bot\reddit_posts\tifu\a99fw9.mp3'
video_clip = r'C:\Users\fergu\Documents\PycharmProjects\Tiktok Bot\video.mp4'
text = r'C:\Users\fergu\Documents\PycharmProjects\Tiktok Bot\reddit_posts\tifu\a99fw9.txt'
output = 'out.json'
output_clip = 'clip.mp4'
audio = AudioFileClip(audio_clip)
video = VideoFileClip(video_clip)
if audio is None:
    print("Audio problem")
if video is None:
    print("Video problem")
audio_duration = math.ceil(audio.duration)
print(audio_duration)
video_duration = math.floor(video.duration)
print(video_duration)
start_time = random.randint(0, video_duration - audio_duration)
print("Starting at " + str(start_time) + " lasting " + str(audio_duration))
print("Generating subclip")
subclip = video.subclip(60, 70)
print("Writing video")
subclip.write_videofile(output_clip)
video.close()
audio.close()
