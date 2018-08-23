import pandas as pd
from db.interface import open_connection, close_connection
from db import match_table as mt

HOME = 1
AWAY = 2
HOMEAWAY = 3

def get_id_for_row(row):
    return mt.get_index(row['HomeTeam'], row['AwayTeam'], row["Date"])

def insert(df, conn):
    for _, record in df.to_dict('index').items():
        mt.insert(conn=conn, **record)

def insert_matches(df):
    conn = open_connection()
    insert(df, conn)
    close_connection(conn)

def calculate_xg(team, date, N, combination=HOME):
    conn = open_connection()

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


        matches = pd.concat([home_matches, away_matches], axis=0)
        matches = matches.sort_values(by='date', ascending=False)
        matches = matches.iloc[0:N, :]

    matches["xg"] = matches["full_time_goals"] / matches["shots_on_target"]
    return matches["xg"].mean()
