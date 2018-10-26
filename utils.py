import json

def write_as_json(data, filename):
    with open(f'{filename}.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)
