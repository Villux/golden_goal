import pandas as pd
from db.interface import execute_statement
from db import helper as dbh

table_name = 'player_identity_table'

def insert(conn, **kwargs):
    return dbh.insert(table_name, conn, **kwargs)
