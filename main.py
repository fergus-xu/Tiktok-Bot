import RedditScraper
import os
import TTS_tiktok
import helper
import VidMaker

# run experiment with tts in colab
def main():
    settings = helper.read_settings("settings.txt")
    folder_path = RedditScraper.make_reddit()  # generate posts
    voice = settings.get('voice')
    video = settings.get('video_path')
    # for each post, format and generate mp3

    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            filepath = os.path.join(folder_path, filename)
            if os.path.isfile(filepath):
                # Create MP3 File
                mp3_file = helper.convert_to_mp3(filename)
                mp3_file = os.path.join(folder_path, mp3_file)
                TTS_tiktok.make_mp3(filepath, mp3_file, voice)

                output_path = helper.convert_to_mp4(filename)
                output_path = os.path.join(folder_path, output_path)
                VidMaker.make_vid(mp3_file, video, output_path, filename)
if __name__ == '__main__':
    main()
