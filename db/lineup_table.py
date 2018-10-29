import pandas as pd
from db.interface import execute_statement
from db import helper as dbh

table_name = 'lineup_table'

def insert(conn, **kwargs):
    return dbh.insert(table_name, conn, **kwargs)
