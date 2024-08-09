A Python program for creating TikTok styled reddit videos using TikTok's TTS

Create a settings.txt file with the following format:
client_id: # Replace with reddit client_id
client_secret: # Replace with reddit client_secret
user_agent: # Replace with reddit username
voice: # See TTS_tiktok.py for options
folder: # Set folder that posts and videos are saved in
video_path: # File path of video from which clips are taken
word_count: # Maximum number of words per subtitle


Note: Moviepy.subclip is very slow for large chunks
