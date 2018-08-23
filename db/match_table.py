import hashlib
import pandas as pd

from db.interface import execute_statement, fetchall
from db.helper import get_value_tuple, build_insert_query, build_update_query_set

table_name = 'match_table'

def get_index(home_team, away_team, date):
    id_string = f"{home_team}{away_team}{date}".encode()
    return hashlib.md5(id_string).hexdigest()

def insert(conn, **kwargs):
    query = build_insert_query(kwargs, table_name)
    values = get_value_tuple(kwargs)
    execute_statement((query, values), conn)
    return execute_statement("select last_insert_rowid()", conn)

def get_mutual_matches_between_dates(team, start, end, conn):
    query = f"select * \
        from match_table \
        where Date > '{start}' AND Date < '{end}' AND \
        (HomeTeam='{team}' OR AwayTeam='{team}');"

    return pd.read_sql(query, conn)
