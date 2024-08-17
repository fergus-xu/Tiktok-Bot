# from mp3 file clip random of same length then combine and dub over
# need to align text from txt file with captions
# uses aeneas for forced alignment
from moviepy.editor import *
import random
from aeneas.executetask import ExecuteTask
from aeneas.task import Task
import math
import helper
import json


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
    print("Starting at " + str(start_time) + " lasting " + str(audio_duration))
    print("Generating subclip")
    subclip = video.subclip(start_time, start_time + audio_duration)
    print("Writing video")
    subclip.write_videofile(output_path)
    video.close()
    audio.close()


# swaps the audio of the clip to the voice-over
def swap_audio(clip_path: str, audio_path: str, output_path: str):
    video_clip = VideoFileClip(clip_path)
    audio_clip = AudioFileClip(audio_path)
    video_clip = video_clip.set_audio(audio_clip)
    video_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
    audio_clip.close()


def get_sync(audio, transcript, output):
    settings = helper.read_settings("settings.txt")
    word_count = settings.get('word_count')
    helper.txt_format(transcript, int(word_count))
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
    with open(sync_map, "r") as file:
        data = json.load(file)
    fragments = data.get("fragments", [])
    for fragment in fragments:
        start_time = fragment.get("begin")
        end_time = fragment.get("end")
        text = fragment.get("lines", [])[0]
        duration = float(end_time) - float(start_time)
        caption_clip = TextClip(text, fontsize=24, color='white', bg_color='black').set_position(
            ('center', 'bottom')).set_duration(duration)
        caption_clip = caption_clip.set_start(start_time)
        caption_clips.append(caption_clip)

    final_clip = CompositeVideoClip([video_clip.set_duration(video_clip.duration), *caption_clips])
    final_clip.write_videofile(output_vid, codec='libx264', audio_codec='aac')

    video_clip.close()
    for clip in caption_clips:
        clip.close()


def crop(clip, x1=None, y1=None, x2=None, y2=None, width=None, height=None, x_center=None, y_center=None):

    if width and x1 is not None:
        x2 = x1 + width
    elif width and x2 is not None:
        x1 = x2 - width

    if height and y1 is not None:
        y2 = y1 + height
    elif height and y2 is not None:
        y1 = y2 - height

    if x_center:
        x1, x2 = x_center - width / 2, x_center + width / 2

    if y_center:
        y1, y2 = y_center - height / 2, y_center + height / 2

    x1 = x1 or 0
    y1 = y1 or 0
    x2 = x2 or clip.size[0]
    y2 = y2 or clip.size[1]

    return clip.fl_image(lambda pic: pic[int(y1): int(y2), int(x1): int(x2)], apply_to=["mask"])


def clip_size(video_file, output_path):
    video_clip = VideoFileClip(video_file)
    width, height = video_clip.size

    crop_width = height * 9/16
    x1, x2 = (width - crop_width) // 2, (width + crop_width) // 2
    y1, y2 = 0, height
    cropped_clip = crop(video_clip, x1=x1, y1=y1, x2=x2, y2=y2)

    cropped_clip.write_videofile(output_path)


def make_vid(audio_path, video_path, output_path, transcript):
    # Generate intermediate filepaths
    folder_path = os.path.dirname(audio_path)
    subclip_path = os.path.join(folder_path, 'subclip.mp4')
    dub_path = os.path.join(folder_path, 'dub.mp4')
    subtitle_path = os.path.join(folder_path, 'subtitle.mp4')

    get_subclip(video_path, audio_path, subclip_path)
    print("Subclip successfully created")
    swap_audio(subclip_path, audio_path, dub_path)
    print("Audio swapped")
    json = helper.convert_to_json(audio_path)
    get_sync(audio_path, transcript, json)
    print("Sync map created")
    subtitle(dub_path, json, subtitle_path)
    print("Subtitles added")
    clip_size(subtitle_path, output_path)
    print("Clipped to size")
    # add cleanup for intermediates
    for file_path in [subclip_path, dub_path, subtitle_path]:
        try:
            os.remove(file_path)
            print(f"File '{file_path}' has been deleted.")
        except FileNotFoundError:
            print(f"File '{file_path}' does not exist.")
        except PermissionError:
            print(f"Permission denied: cannot delete '{file_path}'.")
        except OSError as e:
            print(f"Error deleting file '{file_path}': {e}")
