import pandas as pd
from db.interface import execute_statement, fetchall, fetchone
from db import helper as dbh

table_name = 'player_table'

def insert(conn, **kwargs):
    return dbh.insert(table_name, conn, **kwargs)

def update_by_fifa_id_and_date(fifa_id, date_id, conn, **kwargs):
    set_text = dbh.build_update_query_set(kwargs)
    query = f"UPDATE player_table SET {set_text} WHERE fifa_id={fifa_id} AND date='{date_id}';"
    execute_statement((query, dbh.get_value_tuple(kwargs)), conn)

def get_existing_indexes(indexes, date_id, conn):
    id_list = ','.join(str(x) for x in indexes)
    query = f"select fifa_id from player_table where fifa_id in ({id_list}) and date='{date_id}';"
    existing_idx = fetchall(query, conn)
    return [idx[0] for idx in existing_idx]

def get_last_data_date(date, **kwargs):
    query = f"select date from player_table where date <= '{date}' order by date desc;"
    return fetchone(query, kwargs["conn"])

def get_data_for_team(team, date, **kwargs):
    query = f"select * from player_table where date='{date}' and club='{team}';"
    return pd.read_sql(query, kwargs["conn"])

def get_latest_by_fifa_id(fifa_id, **kwargs):
    query = f"select * from player_table where fifa_id='{fifa_id}' order by date desc limit 1;"
    return pd.read_sql(query, kwargs["conn"])

def players_between_dates_for_team(team, date, year_lag, **kwargs):
    query = f"select * from player_table where date > date('{date}','-{year_lag} year') and date <= '{date}' and club='{team}' group by name;"
    return pd.read_sql(query, kwargs["conn"])
