import json
import os

from GI_code import GenshinCode
from GI_reward import GenshinReward


def serialization_json(relative_path, file, data):
    # if no empty parameter
    if relative_path and file and data:
        # Open file to write
        with open(f'{relative_path}{file}.json', 'w+') as write:
            json.dump(data, write, indent=4)
        write.close()


def deserialization_json(relative_path, file):
    try:
        data = {}
        # if no empty parameter
        if relative_path and file and os.path.exists(f'{relative_path}{file}.json'):
            # Open JSON file
            json_file = open(f'{relative_path}{file}.json', )
        # JSON object as a dictionary
            data = json.load(json_file)

        # Closing the JSON file
            json_file.close()

        return data

    except json.JSONDecodeError:

        return {}


def genshin_codes_to_json(relative_path, file, data):

    try:
        # if no empty parameter
        if relative_path and file and data['codes']:
            data['codes'] = [code.asdict() for code in data['codes']]
            if relative_path and file and data:
                # Open file to write
                with open(f'{relative_path}{file}.json', 'w+') as write:
                    json.dump(data, write, indent=4)
                write.close()
    except json.JSONDecodeError:

        return {}


def json_to_genshin_codes(relative_path, file):
    try:
        data = {}
        # if no empty parameter adn file exists
        if relative_path and file and os.path.exists(f'{relative_path}{file}.json'):
            # Open JSON file
            json_file = open(f'{relative_path}{file}.json', )
        # JSON object as a dictionary
            data = json.load(json_file)

        # Closing the JSON file
            json_file.close()
            codes = []
            for code in data['codes']:
                codes.append(GenshinCode(
                    code['promotional_code'],
                    code['external_link'],
                    code['server'],
                    [GenshinReward(reward['item_name'], reward['quantity']) for reward in code['rewards']],
                    code['status'],
                    code['start'],
                    code['end']
                ))

            data['codes'] = codes

        return data

    except json.JSONDecodeError:

        return {}
