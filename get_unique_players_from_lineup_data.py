import glob
import json
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz

from logger import logging
from db import player_table as pt
from db import player_identity_table as pit
from db.interface import open_connection, close_connection
from utils import remove_extra_keys, get_goalcom_lastname
from map_players_manually import map_player_manually

conn = open_connection()

def get_players_for_team(team, date):
    return pt.players_between_dates_for_team(team, date, 1, conn=conn)

def get_partial_fuzzy_score(value, name):
    return fuzz.partial_ratio(name, value)

def get_fuzzy_score(value, name):
    return fuzz.ratio(name, value)

def get_players_from_file(path="missing_players.csv"):
    data = pd.read_csv(path)
    return [record for (_, record) in data.to_dict('index').items()]

def match_player_to_fifa(player):
    player_df =  get_players_for_team(player["team"], player["date"])
    last_name = get_goalcom_lastname(player["name"])
    player_df["partial_score"] = player_df["name"].apply(get_partial_fuzzy_score, args=(last_name,))
    player_df["score"] = player_df["name"].apply(get_fuzzy_score, args=(player["team"],))
    player_df = player_df.sort_values(by=['partial_score'], ascending=False)

    if player_df.shape[0] == 0:
        return player

    if pit.get_id_by_goalcom_url(player["url_id"], conn=conn):
        return player

    first_score = player_df["partial_score"].values[0]
    second_score = player_df["partial_score"].values[1]

    player_object = {}
    if first_score > 80 and first_score - second_score >= 20:
        player_object["fifa_id"] = player_df.iloc[0, :]["id"].item()
        player_object["goalcom_url"] = player["url_id"]
        player_object["goalcom_name"] = player["name"]
    else:
        player_object = map_player_manually(player, last_name, conn)

    if player_object.get("fifa_id"):
        fifa_id = player_object.pop('fifa_id')
        pit.update_by_fifa_id(fifa_id, remove_extra_keys(player_object, pit.VALID_KEYS), conn=conn)
        conn.commit()

    return player_object

def run():
    players = get_players_from_file()
    for player in players:
        match_player_to_fifa(player)

if __name__ == '__main__':
    run()
    close_connection(conn)
