import pandas as pd
from db.interface import execute_statement, fetchone
from db import helper as dbh

table_name = 'player_identity_table'

VALID_KEYS = ["fifa_id", "fifa_name", "goalcom_url", "goalcom_name"]

def insert(conn, **kwargs):
    return dbh.insert(table_name, conn, **kwargs)

def update_by_fifa_id(fifa_id, data, **kwargs):
    set_text = dbh.build_update_query_set(data)
    query = f"UPDATE player_identity_table SET {set_text} WHERE fifa_id={fifa_id};"
    execute_statement((query, dbh.get_value_tuple(data)), kwargs["conn"])

def get_id_by_goalcom_url(url, **kwargs):
    query = f"select fifa_id from player_identity_table where goalcom_url='{url}'"
    return fetchone(query, kwargs["conn"])

def get_by_fifa_id(fifa_id, **kwargs):
    query = f"SELECT * from player_identity_table WHERE fifa_id={fifa_id};"
    return pd.read_sql(query, kwargs["conn"])
