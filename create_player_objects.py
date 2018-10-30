import pandas as pd

from db.interface import open_connection, close_connection
from db.player_table import get_latest_by_fifa_id
from db.player_identity_table import insert
from logger import logging

def main(conn):
    fifa_ids = pd.read_csv("fifa_ids.csv")["fifa_id"].values
    logging.info(f"Inserting {len(fifa_ids)} players")
    for fifa_id in fifa_ids:
        player_obj = {}
        player_df = get_latest_by_fifa_id(fifa_id, conn=conn)
        if player_df.shape[0] == 0:
            logging.warning(f"No player found for fifa id {fifa_id}")

        player_obj["fifa_name"] = player_df["name"].item()
        player_obj["fifa_id"] = fifa_id
        insert(conn, **player_obj)
        conn.commit()

if __name__ == '__main__':
    conn = open_connection()
    main(conn)
    close_connection(conn)
