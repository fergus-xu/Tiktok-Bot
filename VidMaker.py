# from mp3 file clip random of same length then combine and dub over
# need to align text from txt file with captions
# uses aeneas for forced alignment
from moviepy.editor import *
import random
from aeneas.executetask import ExecuteTask
from aeneas.task import Task
import math
from moviepy.video.fx.all import crop

import helper


# generates a random subclip
def get_subclip(video_clip: str, audio_clip: str, output_path: str):
    audio = AudioFileClip(audio_clip)
    video = VideoFileClip(video_clip)
    if audio is None:
        print("Audio problem")
        return
    if video is None:
        print("Video problem")
        return
    audio_duration = math.ceil(audio.duration)
    video_duration = math.floor(video.duration)
    start_time = random.randint(0, video_duration - audio_duration)
    subclip = video.subclip(start_time, start_time + audio_duration)
    subclip.write_videofile(output_path)
    subclip.close()
    video.close()
    audio.close()


# swaps the audio of the clip to the voice over
def swap_audio(clip_path: str, audio_path: str, output_path: str):
    video_clip = VideoFileClip(clip_path)
    audio_clip = AudioFileClip(audio_path)
    video_clip = video_clip.set_audio(audio_clip)
    video_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
    video_clip.close()
    audio_clip.close()


def get_sync(audio, transcript, output):
    config_string = u"task_language=eng|is_text_type=plain|os_task_file_format=json"
    task = Task(config_string=config_string)
    task.audio_file_path_absolute = audio
    task.text_file_path_absolute = transcript
    task.sync_map_file_path_absolute = output

    ExecuteTask(task).execute()
    task.output_sync_map_file()


# adds subtitles using forced alignment
def subtitle(video_file, sync_map, output_vid):
    video_clip = VideoFileClip(video_file)
    caption_clips = []

    for fragment in sync_map:
        start_time = fragment.begin
        end_time = fragment.end
        text = fragment.annotation.text
        duration = end_time - start_time
        caption_clip = TextClip(text, fontsize=24, color='white', bg_color='black').set_position(
            ('center', 'bottom')).set_duration(duration)
        caption_clip = caption_clip.set_start(start_time)
        caption_clips.append(caption_clip)

    final_clip = CompositeVideoClip([video_clip.set_duration(video_clip.duration), *caption_clips])
    final_clip.write_videofile(output_vid, codec='libx264', audio_codec='aac')

    video_clip.close()
    for clip in caption_clips:
        clip.close()


def clip_size(video_file, output_path):
    video_clip = VideoFileClip(video_file)
    width, height = video_clip.size

    crop_width = height * 9/16
    x1, x2 = (width - crop_width) // 2, (width + crop_width) // 2
    y1, y2 = 0, height
    cropped_clip = crop(video_clip, x1=x1, y1=y1, x2=x2, y2=y2)

    cropped_clip.write_videofile(output_path)


def make_vid(audio_path, video_path, output_path, transcript):
    get_subclip(video_path, audio_path, output_path)
    swap_audio(output_path, audio_path, output_path)
    json = helper.convert_to_json(audio_path)
    get_sync(audio_path, transcript, json)
    subtitle(output_path, json, output_path)
    clip_size(output_path, output_path)