import numpy as np
from db import player_table as pt

def insert_players(df, conn):
    for idx, record in df.to_dict('index').items():
        record["fifa_id"] = idx
        pt.insert(conn=conn, **record)

def update_players_by_fifa_id_and_date(df, date_id, conn):
    for idx, record in df.to_dict('index').items():
        pt.update_by_fifa_id_and_date(idx, date_id, conn, **record)

def insert_or_update_player_data(player_data, date, **kwargs):
    conn = kwargs["conn"]
    existing_idx = pt.get_existing_indexes(player_data.index.values, date, conn)
    existing_df = player_data.loc[existing_idx]
    new_idx = np.setdiff1d(player_data.index.values, existing_df.index.values)
    new_df = player_data.loc[new_idx]

    insert_players(new_df, conn)
    update_players_by_fifa_id_and_date(existing_df, date, conn)
