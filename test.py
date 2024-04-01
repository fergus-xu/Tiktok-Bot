from RedditScraper import format_text
from helper import convert_to_mp3
from TTS_tiktok import make_mp3
from moviepy.editor import *
import math
import VidMaker
audio = 'reddit_posts/tifu/x35iu6.mp3'
video = r'C:\Users\fergu\Documents\PycharmProjects\Tiktok Bot\video.mp4'
VidMaker.get_sync(r'C:\Users\fergu\Documents\PycharmProjects\Tiktok Bot\reddit_posts\tifu\x35iu6.mp3', r'C:\Users\fergu\Documents\PycharmProjects\Tiktok Bot\reddit_posts\tifu\x35iu6.txt', 'out.json')