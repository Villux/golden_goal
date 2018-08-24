import pandas as pd
from db import match_table as mt
from services.odds import insert_odds_for_match

HOME = 1
AWAY = 2
HOMEAWAY = 3

def merge_dataset_get_n(home_df, away_df, N, sort_col="date", asc=False):
    matches = pd.concat([home_df, away_df], axis=0)
    matches = matches.sort_values(by=sort_col, ascending=asc)
    return matches.iloc[0:N, :]

def get_id_for_row(row):
    return mt.get_index(row['HomeTeam'], row['AwayTeam'], row["Date"])

def remove_extra_keys(record):
    new_dict = {}
    for valid_key in mt.VALID_KEYS:
        value = record.get(valid_key, None)
        if value:
            new_dict[valid_key] = value
    return new_dict

def insert_matches(df, season_id, **kwargs):
    conn = kwargs["conn"]
    for _, record in df.to_dict('index').items():
        record["season_id"] = season_id
        match_id = mt.insert(conn=conn, **remove_extra_keys(record))
        insert_odds_for_match(record, match_id, conn)

def calculate_goal_average(team, date, N, conn):
    home_matches = mt.get_n_latest_matches_before_date(team, date, N, conn, hometeam=True)[["Date", "FTHG"]]
    away_matches = mt.get_n_latest_matches_before_date(team, date, N, conn, hometeam=False)[["Date", "FTAG"]]
    column_names = ["date", "score"]
    home_matches.columns = column_names
    away_matches.columns = column_names

    matches = merge_dataset_get_n(home_matches, away_matches, N)
    return matches["score"].mean()

def calculate_xg(team, date, N, conn, combination=HOME):
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
    return matches["xg"].mean()
