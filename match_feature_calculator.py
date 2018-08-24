from services import match, elo
from db.interface import open_connection, close_connection
from db import match_table as mt

def calculate_elo_for_matches():
    conn = open_connection()
    matches = mt.get_matches(conn)
    for _, record in matches.to_dict('index').items():
        home_elo, home_elo_id = elo.get_elo_and_id(record["HomeTeam"], record["Date"], record["season_id"], conn=conn)
        away_elo, away_elo_id = elo.get_elo_and_id(record["AwayTeam"], record["Date"], record["season_id"], conn=conn)
        elo.attach_elo_to_match(record["id"], home_elo_id, away_elo_id, conn=conn)

        new_home_elo, new_away_elo = elo.get_elo_from_result(home_elo, away_elo, record["FTHG"], record["FTAG"])
        elo.insert(record["HomeTeam"], record["season_id"], record["Date"], new_home_elo, conn=conn)
        elo.insert(record["AwayTeam"], record["season_id"], record["Date"], new_away_elo, conn=conn)
        conn.commit()

    close_connection(conn)

if __name__ == "__main__":
    calculate_elo_for_matches()
