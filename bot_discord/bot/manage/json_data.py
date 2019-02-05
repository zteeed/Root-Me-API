import json


def read_json():
    with open("data.json", "r") as json_file:
        extract = json_file
        data = json.load(extract)
        return data


def update_json(data):
    with open("data.json", "w") as json_file:
        json.dump(data, json_file)


def default():
    return extract_default()


def is_first():
    data = read_json()
    return data['info']['first']


def update_first_time(boolean):
    data = read_json()
    data['info']['first'] = boolean
    update_json(data)


def launched():
    update_first_time(False)


