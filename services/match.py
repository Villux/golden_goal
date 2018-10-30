import pandas as pd
import numpy as np
from db import match_table as mt
from services.odds import insert_odds_for_match
from services.utils import map_team_names
from utils import remove_extra_keys

HOME = 1
AWAY = 2
HOMEAWAY = 3

def get_match_outcome(match):
    return np.sign(match["FTHG"] - match["FTAG"])

def merge_dataset_get_n(home_df, away_df, N, sort_col="date", asc=False):
    matches = pd.concat([home_df, away_df], axis=0)
    matches = matches.sort_values(by=sort_col, ascending=asc)
    return matches.iloc[0:N, :]

def get_id_for_row(row):
    return mt.get_index(row['HomeTeam'], row['AwayTeam'], row["Date"])

def insert_matches(df, season_id, **kwargs):
    conn = kwargs["conn"]
    for _, record in df.to_dict('index').items():
        record["season_id"] = season_id
        record["HomeTeam"] = map_team_names(record["HomeTeam"])
        record["AwayTeam"] = map_team_names(record["AwayTeam"])
        match_id = mt.insert(conn=conn, **remove_extra_keys(record, mt.VALID_KEYS))
        insert_odds_for_match(record, match_id, conn)

def calculate_goal_average(team, date, N, **kwargs):
    conn = kwargs["conn"]
    home_matches = mt.get_n_latest_matches_before_date(team, date, N, conn, hometeam=True)[["Date", "FTHG"]]
    away_matches = mt.get_n_latest_matches_before_date(team, date, N, conn, hometeam=False)[["Date", "FTAG"]]
    column_names = ["date", "score"]
    home_matches.columns = column_names
    away_matches.columns = column_names

    matches = merge_dataset_get_n(home_matches, away_matches, N)
    return matches["score"].mean()

def calculate_xg(team, date, N, combination=HOME, **kwargs):
    conn = kwargs["conn"]
    column_names = ["date", "shots_on_target", "full_time_goals"]
    if combination == HOME:
        matches = mt.get_n_latest_matches_before_date(team, date, N, conn, hometeam=True)[["Date", "HST", "FTHG"]]
        matches.columns = column_names
    elif combination == AWAY:
        matches = mt.get_n_latest_matches_before_date(team, date, N, conn, hometeam=False)[["Date", "AST", "FTAG"]]
        matches.columns = column_names
    else:
        home_matches = mt.get_n_latest_matches_before_date(team, date, N, conn, hometeam=True)[["Date", "HST", "FTHG"]]
        home_matches.columns = column_names
        away_matches = mt.get_n_latest_matches_before_date(team, date, N, conn, hometeam=False)[["Date", "AST", "FTAG"]]
        away_matches.columns = column_names


        matches = merge_dataset_get_n(home_matches, away_matches, N)

    matches["xg"] = matches["full_time_goals"] / matches["shots_on_target"]
    return matches["xg"].replace([np.inf, -np.inf], np.nan).mean()
