import glob
import json
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz

from logger import logging
from db import player_table as pt
from db import player_identity_table as pit
from db.interface import open_connection, close_connection
from utils import remove_extra_keys

conn = open_connection()

def get_players_for_team(team, date):
    return pt.players_between_dates_for_team(team, date, 1, conn=conn)

def get_partial_fuzzy_score(value, name):
    return fuzz.partial_ratio(name, value)

def get_fuzzy_score(value, name):
    return fuzz.ratio(name, value)

def get_goalcom_lastname(name):
    name = name.strip()
    if " " in name:
        _, last_name = name.rsplit(' ', 1)
        return last_name
    return name

def map_lineup_with_player_data(lineup):
    date = lineup["date"]
    home_team = lineup["home_team"]
    home_team_players = lineup["home_team_players"] + lineup["home_team_substitutes"]
    home_team_lineup_players = [dict(player, **{'date':date, "team": home_team}) for player in home_team_players]

    away_team = lineup["away_team"]
    away_team_players = lineup["away_team_players"] + lineup["away_team_substitutes"]
    away_team_lineup_players = [dict(player, **{'date':date, "team": away_team}) for player in away_team_players]

    return home_team_lineup_players + away_team_lineup_players

def get_players_from_lineups(path="lineups/*.json"):
    lineup_files = glob.glob(path)
    players = []

    for _, lineup_file in enumerate(lineup_files):
        with open(lineup_file, "rb") as lf:
            for line in lf.readlines():
                lineup_data = json.loads(line)
                flatten = [item for sublist in [map_lineup_with_player_data(match_lineup) for match_lineup in lineup_data] for item in sublist]
                players = players + flatten

    players = list({v['url_id']:v for v in players}.values())
    return players

def get_players_from_file(path="missing_substitutes.csv"):
    data = pd.read_csv(path)
    return [record for (_, record) in data.to_dict('index').items()]

def match_player_to_fifa(player, idx):
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
    if first_score > 80 and first_score - second_score >= 20:
        idx = 1
    elif first_score < 55:
        idx = 0
    else:
        print(idx)
        player_df.index = np.arange(1,len(player_df)+1)
        print(player_df[["name", "partial_score"]].head(10))
        idx = int(input(f"Matching for {player['name']} {player['url_id']}: \n"))
    if idx > 0:
        player["fifa_id"] = player_df.iloc[idx-1, :]["id"]
        player["goalcom_url"] = player["url_id"]
        update_pit(player)
        conn.commit()
    else:
        player["fifa_id"] = None

    return player

def update_pit(player):
    fifa_id = player["fifa_id"]
    player.pop('fifa_id', None)
    pit.update_by_fifa_id(fifa_id, remove_extra_keys(player, pit.VALID_KEYS), conn=conn)

def update_pits(players):
    for player in players:
        update_pit(player)

def run():
    lineup_players = get_players_from_lineups()

if __name__ == '__main__':
    run()
    close_connection(conn)
