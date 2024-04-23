import json

import discord

rcolor = [
    discord.Colour.purple(),
    discord.Colour.orange(),
    discord.Colour.green(),
    discord.Colour.blue(),
    discord.Colour.red(),
    discord.Colour.teal(),
    discord.Colour.dark_teal(),
    discord.Colour.dark_green(),
    discord.Colour.dark_blue(),
    discord.Colour.dark_purple(),
    discord.Colour.magenta(),
    discord.Colour.dark_magenta(),
    discord.Colour.gold(),
    discord.Colour.dark_gold(),
    discord.Colour.dark_orange(),
    discord.Colour.dark_red(),
    discord.Colour.lighter_gray(),
    discord.Colour.dark_gray(),
    discord.Colour.light_gray(),
    discord.Colour.darker_gray(),
    discord.Colour.blurple(),
    discord.Colour.greyple()
]

def load_data():
    try:
        with open('database.txt', 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                print("JSON Decode Error:", e)
    except FileNotFoundError:
        pass
    return data

data = load_data()

def save_data(data):
    with open('database.txt', 'w') as file:
        json.dump(data, file)


def insert_data(key, value):
    data[key] = value
    save_data(data)


def get_data(key):
    return data.get(key)


def delete_data(key):
    if key in data:
        del data[key]
        save_data(data)


def list_all_keys():
    return list(data.keys())


def list_keys_with_prefix(prefix):
    return [key for key in data.keys() if key.startswith(prefix)]

def developer_check(id):
    devs = [
        559080343085514772,
        742079317101641778,
        886279024710656040
    ]
    for i in devs:
        if int(id) == i:
            return True
    return False
