import argparse
from multiprocessing import Pool, cpu_count
import pandas as pd

from services import match, elo, player
from db.interface import open_connection, close_connection
from db import match_table as mt
from db import season_table as st

parser = argparse.ArgumentParser()
parser.add_argument('-d', type=int)
parser.add_argument('-f', type=str)
args = parser.parse_args()

def get_match_datapoints(match_obj):
    conn = open_connection()
    date = match_obj["Date"]
    season_id = match_obj["season_id"]
    N = 20

    home_team = match_obj["HomeTeam"]
    match_obj["home_xg"] = match.calculate_xg(home_team, date, N, combination=match.HOMEAWAY, conn=conn)
    match_obj["home_goal_mean"] = match.calculate_goal_average(home_team, date, N, conn=conn)
    match_obj["home_elo"] = elo.get_elo_and_id(home_team, date, season_id, conn=conn)

    away_team = match_obj["AwayTeam"]
    match_obj["away_xg"] = match.calculate_xg(away_team, date, N, combination=match.HOMEAWAY, conn=conn)
    match_obj["away_goal_mean"] = match.calculate_goal_average(away_team, date, N, conn=conn)
    match_obj["away_elo"] = elo.get_elo_and_id(away_team, date, season_id, conn=conn)

    home, away = player.get_team_features_for_matches(home_team, away_team, date, conn=conn)

    close_connection(conn)
    return {**match, **home, **away}

def get_data_for_matches(matches):
    func_args = [record for _, record in matches.to_dict('index').items()]
    pool = Pool(cpu_count())
    data_list = pool.map(get_match_datapoints, func_args)
    return pd.DataFrame(data_list)

if __name__ == "__main__":
    connection = open_connection()
    if args.d:
        season_tuples = st.get_seasons_for_division(args.d)
        season_ids = [season[0] for season in season_tuples]
    else:
        season_ids = None

    all_matches = mt.get_matches_for_seasons(season_ids, conn=connection)
    close_connection(connection)

    results = get_data_for_matches(all_matches)
    results.to_csv(args.f)
