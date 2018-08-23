from db.interface import open_connection, close_connection
from db import match_table as mt

def get_id_for_row(row):
    return mt.get_index(row['HomeTeam'], row['AwayTeam'], row["Date"])

def insert(df, conn):
    for _, record in df.to_dict('index').items():
        mt.insert(conn=conn, **record)

def insert_matches(df):
    conn = open_connection()
    insert(df, conn)
    close_connection(conn)
