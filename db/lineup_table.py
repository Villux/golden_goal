import pandas as pd
from db.interface import execute_statement, fetchone
from db import helper as dbh

table_name = 'lineup_table'

def insert(conn, **kwargs):
    return dbh.insert(table_name, conn, **kwargs)

def build_lineup_object(player_sets, match_id):
    data = {}
    for ps_idx, player_set_prefix in enumerate(["hp", "hs", "ap", "as"]):
        for idx, player_id in enumerate(player_sets[ps_idx]):
            data[f"{player_set_prefix}{idx+1}"] = player_id
    data["match_id"] = match_id
    return data

def insert_player_for_match(player_sets, match_id, **kwargs):
    data = build_lineup_object(player_sets, match_id)
    insert(kwargs["conn"], **data)

def get_by_match_id(match_id, **kwargs):
    query = f"select * from lineup_table where match_id={match_id}"
    return pd.read_sql(query, kwargs["conn"])

def update(match_id, player_sets, conn):
    data = build_lineup_object(player_sets, match_id)
    set_text = dbh.build_update_query_set(data)
    query = f"UPDATE lineup_table SET {set_text} WHERE match_id={match_id};"
    execute_statement((query, dbh.get_value_tuple(data)), conn)
