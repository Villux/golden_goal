import hashlib
import pandas as pd

from db import helper as dbh

table_name = 'match_table'

VALID_KEYS = ["id","Div","Date","HomeTeam","AwayTeam","FTHG","FTAG","FTR","HTHG","HTAG",
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
