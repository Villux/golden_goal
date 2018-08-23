import numpy as np
from db.interface import open_connection, close_connection
from db import player_table as pt

def insert_players(df, conn):
    for idx, record in df.to_dict('index').items():
        record["fifa_id"] = idx
        pt.insert(conn=conn, **record)

def update_players(df, conn):
    for idx, record in df.to_dict('index').items():
        pt.update_by_id(idx, conn, **record)

def insert_or_update_player_data(player_data):
    conn = open_connection()

    existing_idx = pt.get_existing_indexes(player_data.index.values, conn)
    existing_df = player_data.loc[existing_idx]
    new_idx = np.setdiff1d(player_data.index.values, existing_df.index.values)
    new_df = player_data.loc[new_idx]

    insert_players(new_df, conn)
    update_players(existing_df, conn)

    close_connection(conn)
