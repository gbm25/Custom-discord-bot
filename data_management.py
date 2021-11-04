import json
import os
from datetime import datetime

from Games.Genshin_Impact.GI_code import GenshinCode
from Games.Genshin_Impact.GI_reward import GenshinReward
from Games.Genshin_Impact.GI_banner import GenshinBanner
from Games.Genshin_Impact.GI_servertime import GenshinImpactServerTime
from config import bot_root_dir


def serialization_json(relative_path, file, data):
    # if no empty parameter
    if relative_path and file and data:
        # Open file to write
        with open(f'{bot_root_dir}/{relative_path}{file}.json', 'w+') as write:
            json.dump(data, write, indent=4)


def deserialization_json(relative_path, file):
    try:
        data = {}
        # if no empty parameter
        if relative_path and file and os.path.exists(f'{bot_root_dir}/{relative_path}{file}.json'):
            # Open JSON file
            json_file = open(f'{bot_root_dir}/{relative_path}{file}.json', )
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
            temp_dict = {'codes': [code.asdict() for code in data['codes']]}

            # Open file to write
            with open(f'{bot_root_dir}/{relative_path}{file}.json', 'w+') as write:
                json.dump(temp_dict, write, indent=4)

    except json.JSONDecodeError:

        return {}


def json_to_genshin_codes(relative_path, file):
    try:
        data = {}
        # if no empty parameter adn file exists
        if relative_path and file and os.path.exists(f'{bot_root_dir}/{relative_path}{file}.json'):
            # Open JSON file
            json_file = open(f'{bot_root_dir}/{relative_path}{file}.json', )
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


def genshin_banners_to_json(relative_path, file, data):
    try:
        # if no empty parameter
        if relative_path and file and data['banners']:
            temp_dict = {'banners': [banner.asdict() for banner in data['banners']]}

            # Open file to write
            with open(f'{bot_root_dir}/{relative_path}{file}.json', 'w+') as write:
                json.dump(temp_dict, write, indent=4)

    except json.JSONDecodeError:

        return {}


def json_to_genshin_banners(relative_path, file):
    try:
        data = {}
        # if no empty parameter adn file exists
        if relative_path and file and os.path.exists(f'{bot_root_dir}/{relative_path}{file}.json'):
            # Open JSON file
            json_file = open(f'{bot_root_dir}/{relative_path}{file}.json', )
            # JSON object as a dictionary
            data = json.load(json_file)

            # Closing the JSON file
            json_file.close()
            banners = []

            for banner in data['banners']:
                banners.append(GenshinBanner(
                    name=banner['name'],
                    url_fandom=banner['url_fandom'],
                    url_official=banner['url_official'],
                    wish_type=banner['wish_type'],
                    image=banner['image'],
                    status=banner['status'],

                    start=[
                        GenshinImpactServerTime(gi_datetime["region"], datetime.fromisoformat(gi_datetime["datetime"]))
                        for gi_datetime in banner['start']],
                    end=[GenshinImpactServerTime(gi_datetime["region"], datetime.fromisoformat(gi_datetime["datetime"]))
                         for gi_datetime in banner['end']]
                ))

            data['banners'] = banners

        return data

    except json.JSONDecodeError:

        return {}
