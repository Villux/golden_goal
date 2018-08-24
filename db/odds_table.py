from db import helper as dbh

table_name = 'odds_table'

def insert(conn, **kwargs):
    return dbh.insert(table_name, conn, **kwargs)
