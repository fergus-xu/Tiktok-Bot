import RedditScraper
import os
import TTS_tiktok
import helper

# run experiment with tts in colab
def main():
    settings = helper.read_settings("settings.txt")
    folder_path = RedditScraper.make_reddit() # generate posts
    voice = settings.get('voice')
    # for each post, format and generate mp3
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            filepath = os.path.join(folder_path, filename)
            if os.path.isfile(filepath):
                out_file = helper.convert_to_mp3(filename)
                out_file = os.path.join(folder_path, out_file)
                TTS_tiktok.make_mp3(filepath, out_file, voice)


if __name__ == '__main__':
    main()
