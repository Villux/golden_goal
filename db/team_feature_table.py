from db import helper as dbh

table_name = 'team_feature_table'

def insert(conn, **kwargs):
    return dbh.insert(table_name, conn, **kwargs)
