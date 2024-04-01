def convert_to_mp3(filename):
    base_name, extension = filename.rsplit(".", 1)

    new_filename = f"{base_name}.mp3"

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
