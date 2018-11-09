import json
import glob

from db import player_identity_table as pit
from db import match_table as mt
from db import lineup_table as lt
from db.interface import open_connection, close_connection
from logger import logging

conn = open_connection()

def attach_ids_to_players(players):
    valid_players = []
    for player in players:
        ret = pit.get_id_by_goalcom_url(player["url_id"], conn=conn)
        if ret:
            player["id"] = ret[0]
            valid_players.append(player)
        else:
            logging.warning(f"No player for goalcom player url {player['url_id']}")
    return valid_players

def map_lineup_with_player_data(lineup):
    home_team_players = attach_ids_to_players(lineup["home_team_players"])
    away_team_players = attach_ids_to_players(lineup["away_team_players"])

    home_team = lineup["home_team"]
    away_team = lineup["away_team"]
    date = lineup["date"]
    match_id_tuple = mt.get_id_for_game(home_team, away_team, date, conn=conn)

    if not match_id_tuple:
        logging.warning(f'No match for {lineup["home_team"]} vs. {lineup["away_team"]} {date}')
    else:
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
    number_of_lineups = len(lineup_files)
    for idx, lineup_file in enumerate(lineup_files):
        logging.info(f"PROCESSING LINEUP {idx+1}/{number_of_lineups}")
        with open(lineup_file, "rb") as lf:
            for line in lf.readlines():
                lineup_data = json.loads(line)
                handle_lineupdate(lineup_data)

if __name__ == '__main__':
    run()
    close_connection(conn)
