import json
import unicodedata

def write_as_json(data, filename):
    with open(f'{filename}.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

def remove_extra_keys(record, valid_keys):
    new_dict = {}
    for valid_key in valid_keys:
        value = record.get(valid_key, None)
        if value:
            new_dict[valid_key] = value
    return new_dict

def unicode_to_ascii(value):
    return unicodedata.normalize('NFD', value).encode('ascii', 'ignore').decode('ascii')
