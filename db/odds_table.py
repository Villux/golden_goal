from db import helper as dbh
from db.interface import fetchone

table_name = 'odds_table'

def insert(conn, **kwargs):
    return dbh.insert(table_name, conn, **kwargs)

def get_for_match(match_id, description, **kwargs):
    query = f"select home_win, draw, away_win from odds_table where match_id={match_id} and description='{description}'"
    return fetchone(query, kwargs["conn"])
