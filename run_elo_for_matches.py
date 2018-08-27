from db.interface import open_connection, close_connection
from db import match_table as mt
from services import elo

if __name__ == "__main__":
    connection = open_connection()
    all_matches = mt.get_matches(conn=connection)
    elo.calculate_elo_for_matches(all_matches, conn=connection)
    close_connection(connection)
