from db import helper as dbh
from db.interface import fetchone, fetchall

table_name = 'odds_table'

def insert(conn, **kwargs):
    return dbh.insert(table_name, conn, **kwargs)

def get_for_match(match_id, description, **kwargs):
    query = f"select home_win, draw, away_win from odds_table where match_id={match_id} and description='{description}'"
    return fetchone(query, kwargs["conn"])

def get_best_for_match(match_id, **kwargs):
    query = f"select home_win, draw, away_win from odds_table where match_id={match_id}"
    odds_list = fetchall(query, kwargs["conn"])
    home_odd = max([odd[0] for odd in odds_list])
    draw_odd = max([odd[1] for odd in odds_list])
    away_odd = max([odd[2] for odd in odds_list])
    return home_odd, draw_odd, away_odd
