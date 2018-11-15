import json
import unicodedata

def write_as_json(data, filename):
    with open(f'{filename}.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

def remove_extra_keys(record, valid_keys):
    new_dict = {}
    for valid_key in valid_keys:
        if valid_key in record:
            new_dict[valid_key] = record[valid_key]
    return new_dict

def unicode_to_ascii(value):
    return unicodedata.normalize('NFD', value).encode('ascii', 'ignore').decode('ascii')

def get_goalcom_lastname(name):
    name = name.strip()
    if " " in name:
        _, last_name = name.rsplit(' ', 1)
        return last_name
    return name
