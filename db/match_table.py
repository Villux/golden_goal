import hashlib
import pandas as pd

from db import helper as dbh
from db.interface import fetchall, fetchone

table_name = 'match_table'

VALID_KEYS = ["id", "season_id", "Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG",
              "HTR","Referee","Home_Team_Shots","Away_Team_Shots","HST","AST","HF","AF",
              "HC","AC","HY","AY","HR","AR","Attendance","HHW","AHW","HO","AO","HBP","ABP"]

def get_index(home_team, away_team, date):
    id_string = f"{home_team}{away_team}{date}".encode()
    return hashlib.md5(id_string).hexdigest()

def get_matches_between_dates(team, start, end, conn):
    query = f"select * \
        from match_table \
        where Date > '{start}' AND Date < '{end}' AND \
        (HomeTeam='{team}' OR AwayTeam='{team}');"

    return pd.read_sql(query, conn)

def get_n_latest_matches_before_date(team, date, N, conn, hometeam=True):
    if hometeam:
        column = "HomeTeam"
    else:
        column = "AwayTeam"
    query = f"select * from match_table where Date < '{date}' AND {column}='{team}' order by Date desc limit {N};"
    return pd.read_sql(query, conn)

def insert(conn, **kwargs):
    return dbh.insert(table_name, conn, **kwargs)

def get_teams(division, conn):
    query = f"SELECT DISTINCT HomeTeam, AwayTeam FROM match_table where Div='{division}';"
    result = fetchall(query, conn)
    return [r[0] for r in result]

def get_matches(asc=True, **kwargs):
    query = f"SELECT * FROM match_table order by date {'asc' if asc else 'desc'};"
    return pd.read_sql(query, kwargs["conn"])

def get_matches_for_seasons(seasons, **kwargs):
    query = f"SELECT * FROM match_table where season_id IN ({','.join(str(idd) for idd in seasons)});"
    return pd.read_sql(query, kwargs["conn"])

def get_teams_for_season(season_id, **kwargs):
    query = f"select distinct(HomeTeam) from match_table where season_id={season_id};"
    return fetchall(query, conn=kwargs["conn"])

def get_id_for_game(home_team, away_team, date, **kwargs):
    query = f"select id from match_table where HomeTeam='{home_team}' and AwayTeam='{away_team}' and Date='{date}';"
    return fetchone(query, kwargs["conn"])

