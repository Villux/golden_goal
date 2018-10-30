import json
import glob
from fuzzywuzzy import fuzz

from db import player_table as pt
from db import player_identity_table as pit
from db import match_table as mt
from db import lineup_table as lt
from db.interface import open_connection, close_connection
from logger import logging
from utils import remove_extra_keys, unicode_to_ascii

conn = open_connection()

def get_players_for_team(team, date):
    return pt.players_between_dates_for_team(team, date, 1, conn=conn)

def get_goalcom_lastname(name):
    name = name.strip()
    if " " in name:
        _, last_name = name.rsplit(' ', 1)
        return last_name
    return name

def merge_goalcom_and_fifa(player_dict, goalcom_data):
    player_dict["goalcom_url"] = goalcom_data["url_id"]
    player_dict["goalcom_name"] = goalcom_data["name"]
    player_dict["lineup_type"] = goalcom_data["lineup_type"]
    return player_dict

def get_partial_fuzzy_score(value, name):
    return fuzz.partial_ratio(name, value)

def get_fuzzy_score(value, name):
    return fuzz.ratio(name, value)

def update_pit_and_get_lineup_data(player):
    fifa_id = player["fifa_id"]
    player.pop('fifa_id', None)
    pit.update_by_fifa_id(fifa_id, conn, **remove_extra_keys(player, pit.VALID_KEYS))
    pit_df = pit.get_by_fifa_id(fifa_id, conn=conn)
    player_dict = pit_df.iloc[0, :].to_dict()
    return {"lineup_type": player["lineup_type"], "id": player_dict["id"]}

def map_players_for_team(player_df, lineup_players):
    player_df["name"] = player_df["name"].apply(unicode_to_ascii)
    players_dirty = [map_goalcom_to_fifa(player_df, lineup_player) for lineup_player in lineup_players]
    players = [player for player in players_dirty if player]

    return [update_pit_and_get_lineup_data(player) for player in players]

def map_goalcom_to_fifa(player_df, player):
    player_name = unicode_to_ascii(player["name"])
    last_name = get_goalcom_lastname(player_name)
    player_df["partial_score"] = player_df["name"].apply(get_partial_fuzzy_score, args=(last_name,))
    player_df["score"] = player_df["name"].apply(get_fuzzy_score, args=(player_name,))

    valid_players = player_df[player_df["partial_score"] > 55]
    if valid_players.shape[0] == 0:
        logging.warning(f'No match for name {player["name"]}')
        return None

    max_score = max(valid_players["partial_score"].values)
    maximum_score_df = player_df[player_df["partial_score"] == max_score]

    return merge_goalcom_and_fifa(maximum_score_df.loc[maximum_score_df["score"].idxmax()].to_dict(), player)

def map_lineup_with_player_data(lineup):
    date = lineup["date"]
    home_team = lineup["home_team"]
    ht_df = get_players_for_team(home_team, date)
    home_team_players = map_players_for_team(ht_df, lineup["home_team_players"])

    away_team = lineup["away_team"]
    at_df = get_players_for_team(away_team, date)
    away_team_players = map_players_for_team(at_df, lineup["away_team_players"])

    match_id_tuple = mt.get_id_for_game(home_team, away_team, date, conn=conn)

    store_lineups(match_id_tuple[0], home_team_players, away_team_players)

def store_lineups(match_id, home_team_players, away_team_players):
    ht_open = [player["id"] for player in home_team_players if player["lineup_type"] == "lineup"]
    ht_subs = [player["id"] for player in home_team_players if player["lineup_type"] == "substitutes"]

    at_open = [player["id"] for player in away_team_players if player["lineup_type"] == "lineup"]
    at_subs = [player["id"] for player in away_team_players if player["lineup_type"] == "substitutes"]

    lineup = lt.get_by_match_id(match_id, conn=conn)
    if lineup:
        lt.update(match_id, [ht_open, ht_subs, at_open, at_subs], conn)
    else:
        lt.insert_player_for_match([ht_open, ht_subs, at_open, at_subs], match_id, conn=conn)
    conn.commit()

def handle_lineupdate(lineup_data):
    for match_lineup in lineup_data:
        map_lineup_with_player_data(match_lineup)

def run(path="lineups/*.json"):
    lineup_files = glob.glob(path)
    for lineup_file in lineup_files:
        with open(lineup_file, "rb") as lf:
            for line in lf.readlines():
                lineup_data = json.loads(line)
                handle_lineupdate(lineup_data)

if __name__ == '__main__':
    run()
    close_connection(conn)
