import pandas as pd
from db import helper as dbh

table_name = 'team_feature_table'

def insert(conn, **kwargs):
    return dbh.insert(table_name, conn, **kwargs)

def get_features(team, date, **kwargs):
    query = f"select * from team_feature_table where club='{team}' and date='{date}'"
    return pd.read_sql(query, kwargs["conn"])
