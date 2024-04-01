# Generates sound files using tiktok voices
import requests
import threading
import base64
url = 'https://tiktok-tts.weilnet.workers.dev/api/generation'
VOICES = [
    # DISNEY VOICES
    'en_us_ghostface',            # Ghost Face
    'en_us_chewbacca',            # Chewbacca
    'en_us_c3po',                 # C3PO
    'en_us_stitch',               # Stitch
    'en_us_stormtrooper',         # Stormtrooper
    'en_us_rocket',               # Rocket

    # ENGLISH VOICES
    'en_au_001',                  # English AU - Female
    'en_au_002',                  # English AU - Male
    'en_uk_001',                  # English UK - Male 1
    'en_uk_003',                  # English UK - Male 2
    'en_us_001',                  # English US - Female (Int. 1)
    'en_us_002',                  # English US - Female (Int. 2)
    'en_us_006',                  # English US - Male 1
    'en_us_007',                  # English US - Male 2
    'en_us_009',                  # English US - Male 3
    'en_us_010',                  # English US - Male 4

    # EUROPE VOICES
    'fr_001',                     # French - Male 1
    'fr_002',                     # French - Male 2
    'de_001',                     # German - Female
    'de_002',                     # German - Male
    'es_002',                     # Spanish - Male

    # AMERICA VOICES
    'es_mx_002',                  # Spanish MX - Male
    'br_001',                     # Portuguese BR - Female 1
    'br_003',                     # Portuguese BR - Female 2
    'br_004',                     # Portuguese BR - Female 3
    'br_005',                     # Portuguese BR - Male

    # ASIA VOICES
    'id_001',                     # Indonesian - Female
    'jp_001',                     # Japanese - Female 1
    'jp_003',                     # Japanese - Female 2
    'jp_005',                     # Japanese - Female 3
    'jp_006',                     # Japanese - Male
    'kr_002',                     # Korean - Male 1
    'kr_003',                     # Korean - Female
    'kr_004',                     # Korean - Male 2

    # SINGING VOICES
    'en_female_f08_salut_damour',  # Alto
    'en_male_m03_lobby',           # Tenor
    'en_female_f08_warmy_breeze',  # Warmy Breeze
    'en_male_m03_sunshine_soon',   # Sunshine Soon

    # OTHER
    'en_male_narration',           # narrator
    'en_male_funny',               # wacky
    'en_female_emotional',         # peaceful
]

def get_audio(data: str, voice: str): # retrieves audio from website
    headers = {'Content-Type': 'application/json'}
    json = {'text': data, 'voice': voice}
    response = requests.post(url, headers=headers, json=json)
    with open('audio.txt', 'a') as file:
        file.write(data)
        file.write(str(response.content))
    return response.content


def base64_to_mp3(base64_string, filename):
    bytes = base64.b64decode(base64_string + '==')
    with open(filename, 'wb') as f:
        f.write(bytes)
    return


def split_string(text, max_length=299):
    chunks = []
    current_chunk = ''

    words = text.split()

    for word in words:
        if len(current_chunk) + len(word) + 1 <= max_length:
            if current_chunk:
                current_chunk += ' '
            current_chunk += word
        else:
            chunks.append(current_chunk)
            current_chunk = word

    # Add the last chunk
    if current_chunk:
        chunks.append(current_chunk)
    with open('chunks.txt', 'w') as file:
        file.write(str(chunks))
    return chunks


def get_audio_chunks(text, voice, index, split_audio):
    audio = get_audio(text, voice)
    base64_data = str(audio).split('"')[5]
    with open('chunks.txt', 'a') as file:
        file.write(text)
        file.write(str(base64_data))
    split_audio[index] = base64_data


def make_mp3(text_file, out_file, voice='en_us_006'):
    if voice == None:
        print("No voice")
        return
    if voice not in VOICES:
        print("Choose a valid voice")
        return
    with open(text_file, "r") as file:
        data = file.read()
    chunks = split_string(data, 299)
    split_audio = [None] * len(chunks)
    threads = []
    for index, text in enumerate(chunks):
        thread = threading.Thread(target=get_audio_chunks, args=(text, voice, index, split_audio))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    base64_str = "".join(split_audio)
    base64_to_mp3(base64_str, out_file)
    print("Saved mp3 to", out_file)
