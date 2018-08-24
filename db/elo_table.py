from db.interface import execute_statement, fetchone
from db import helper as dbh

table_name = "elo_table"

def insert(conn, **kwargs):
    return dbh.insert(table_name, conn, **kwargs)

def select_latest_for_team(team, date, season_id, **kwargs):
    query = 'SELECT elo, id FROM elo_table WHERE team=? AND date < ? AND season_id=? ORDER BY date DESC;'
    return fetchone((query, (team, date, season_id)), kwargs["conn"])

def select_latest_for_season(season_id, **kwargs):
    asc = kwargs.get("asc", True)
    query = f"SELECT elo, id FROM elo_table WHERE season_id=? ORDER BY elo {'asc' if asc else 'desc'};"
    return fetchone((query, (season_id,)), kwargs["conn"])

def attach_match_to_elo(match_id, id_a, id_b, **kwargs):
    conn = kwargs["conn"]
    query = f"update elo_table set match_id=? where id=?;"
    execute_statement((query, (match_id, id_a)), conn)
    execute_statement((query, (match_id, id_b)), conn)
