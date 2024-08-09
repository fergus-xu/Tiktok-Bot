import os
import shutil


def convert_to_mp3(filename):
    base_name, extension = filename.rsplit(".", 1)
    new_filename = f"{base_name}.mp3"
    return new_filename


def convert_to_json(filename):
    base_name, extension = filename.rsplit(".", 1)
    new_filename = f"{base_name}.json"
    return new_filename


def convert_to_webm(filename):
    base_name, extension = filename.rsplit(".", 1)
    new_filename = f"{base_name}.webm"
    return new_filename


def convert_to_mp4(filename):
    base_name, extension = filename.rsplit(".", 1)
    new_filename = f"{base_name}.mp4"
    return new_filename


def read_settings(file_path):
    settings = {}

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                key, value = line.split(':')
                settings[key.strip()] = value.strip()

    return settings


def clean(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path):
        # Check if the folder is not empty
        if os.listdir(folder_path):
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                try:
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        os.unlink(item_path)  # Delete file or symbolic link
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)  # Delete directory and all its contents
                except Exception as e:
                    print(f'Failed to delete {item_path}. Reason: {e}')


def txt_format(file_path, word_count):
    if word_count is None:
        word_count = 3
    with open(file_path, 'r') as file:
        text = file.read()
    words = text.split()
    lines = []
    for i in range(0, len(words), word_count):
        line = ' '.join(words[i:i + word_count])
        lines.append(line)
    with open(file_path, 'w') as file:
        for line in lines:
            file.write(line + '\n')