from moviepy.editor import *
import VidMaker
import helper
from aeneas.executetask import ExecuteTask
from aeneas.task import Task
audio = r'C:\Users\fergu\Documents\PycharmProjects\Tiktok Bot\reddit_posts\tifu\a99fw9.mp3'
video = r'C:\Users\fergu\Documents\PycharmProjects\Tiktok Bot\video.mp4'
text = r'C:\Users\fergu\Documents\PycharmProjects\Tiktok Bot\reddit_posts\tifu\a99fw9.txt'
output = 'out.json'
VidMaker.get_sync(audio, text, output)
