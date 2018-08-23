from db.elo_table import attach_match_to_elo, insert, select_latest_for_team
from db.interface import open_connection, close_connection

def expected(A, B):
    return 1 / (1 + 10 ** ((B - A) / 400))

def elo(old, exp, score, K):
    return old + K * (score - exp)

def get_new_elo(A, B, goals_A, goals_B, K):
    goals_diff = abs(goals_A - goals_B)
    if goals_diff == 2:
        K *= 1.5
    elif goals_diff == 3:
        K *= 1.75
    elif goals_diff > 3:
        K *= (1.75 + (goals_diff - 3) / 8)

    if goals_A > goals_B:
        score = 1
    elif goals_A == goals_B:
        score = 0.5
    else:
        score = 0
    return elo(A, expected(A, B), score, K)

def get_elo_after_match(elo_A, elo_B, goals_A, goals_B):
    K = 40

    new_elo_A = get_new_elo(elo_A, elo_B, goals_A, goals_B, K)
    new_elo_B = get_new_elo(elo_B, elo_A, goals_B, goals_A, K)

    return new_elo_A, new_elo_B

def get_elo(team, date, conn):
    return select_latest_for_team(team, date, conn)

def attach_elo_to_match(match_id, match_date, home_team, away_team, conn):
    elo_A, id_A = get_elo(home_team, match_date, conn)
    elo_B, id_B = get_elo(away_team, match_date, conn)

    attach_match_to_elo(match_id, id_A, id_B, conn)
    return elo_A, elo_B

def update_elo_after_match(date, elo_home, elo_away, home_team, away_team, conn):
    home_data = {"date": date, "team": home_team, "elo": elo_home}
    away_data = {"date": date, "team": away_team, "elo": elo_away}

    insert(conn, **home_data)
    insert(conn, **away_data)


def calculate_elo_from_matches(matches):
    conn = open_connection()
    for (match_id, date, home_team, away_team, home_score, away_score) in matches:
        elo_A, elo_B = attach_elo_to_match(match_id, date, home_team, away_team, conn)
        new_elo_A, new_elo_B = get_elo_after_match(elo_A, elo_B, home_score, away_score)
        update_elo_after_match(date, new_elo_A, new_elo_B, home_team, away_team, conn)

    close_connection(conn)
