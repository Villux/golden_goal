from db import elo_table as et, season_table as st
from db.interface import open_connection, close_connection
from logger import logging

INITIAL_ELO = 1500

def expected(A, B):
    c = 10
    d = 400
    return 1 / (1 + c ** ((B - A) / d))

def calculate_elo(old, exp, score, K):
    return old + K * (score - exp)

def get_new_elo(A, B, goals_A, goals_B, K):
    goals_diff = abs(goals_A - goals_B)
    K = K*(1+goals_diff)

    if goals_A > goals_B:
        score = 1
    elif goals_A == goals_B:
        score = 0.5
    else:
        score = 0
    return calculate_elo(A, expected(A, B), score, K)

def get_elo_from_result(elo_A, elo_B, goals_A, goals_B):
    K = 10

    new_elo_A = get_new_elo(elo_A, elo_B, goals_A, goals_B, K)
    new_elo_B = get_new_elo(elo_B, elo_A, goals_B, goals_A, K)

    return new_elo_A, new_elo_B

def insert_initial_elo(team, season_id, date, **kwargs):
    elo_id = insert(team, season_id, date, INITIAL_ELO,  **kwargs)
    kwargs["conn"].commit()
    return (INITIAL_ELO, elo_id)

def get_elo_and_id(team, date, season_id, **kwargs):
    elo = et.select_latest_for_team(team, date, season_id, **kwargs)
    if not elo:
        previous_season_id = st.get_previous_season(season_id, **kwargs)
        if not previous_season_id:
            logging.info(f"No previous season - inserting initial elo for {team}, {date}, {season_id}")
            elo = insert_initial_elo(team, season_id, "1900-01-01", **kwargs)
        else:
            elo = et.select_latest_for_team(team, date, previous_season_id[0], **kwargs)
            if not elo:
                elo = et.select_latest_for_season(previous_season_id[0], **kwargs)
                if not elo:
                    logging.info(f"Previous season exist but no latest for previous season - inserting initial elo for {team}, {date}, {season_id}")
                    elo = insert_initial_elo(team, season_id, date, **kwargs)
    return elo

def insert(team, season_id, date, elo, **kwargs):
    conn = kwargs["conn"]
    data = {
        "date": date,
        "team": team,
        "elo": elo,
        "season_id": season_id
    }
    return et.insert(conn, **data)

def attach_elo_to_match(match_id, home_elo_id, away_elo_id, **kwargs):
    et.attach_match_to_elo(match_id, home_elo_id, away_elo_id, **kwargs)

def calculate_elo_for_matches(matches, **kwargs):
    for _, record in matches.to_dict('index').items():
        home_elo, home_elo_id = get_elo_and_id(record["HomeTeam"], record["Date"], record["season_id"], **kwargs)
        away_elo, away_elo_id = get_elo_and_id(record["AwayTeam"], record["Date"], record["season_id"], **kwargs)
        attach_elo_to_match(record["id"], home_elo_id, away_elo_id, **kwargs)

        new_home_elo, new_away_elo = get_elo_from_result(home_elo, away_elo, record["FTHG"], record["FTAG"])
        insert(record["HomeTeam"], record["season_id"], record["Date"], new_home_elo, **kwargs)
        insert(record["AwayTeam"], record["season_id"], record["Date"], new_away_elo, **kwargs)
        kwargs["conn"].commit()
