import numpy as np
from db import player_table as pt

TOP = 3
HALF =  5
FIELD =  10
GK = 2
ALL = 25

field_list = [("acceleration", TOP), ("age", ALL), ("aggression", TOP), ("agility", TOP),
              ("balance", TOP), ("ball_control", HALF), ("composure", TOP), ("crossing", HALF),
              ("curve", HALF), ("dribbling", HALF), ("finishing", TOP), ("fk_accuracy", TOP),
              ("gk_diving", GK), ("gk_handling", GK), ("gk_kicking", GK), ("gk_positioning", GK),
              ("gk_reflexes", GK), ("growth", HALF), ("heading_accuracy", HALF), ("height", FIELD),
              ("interceptions", HALF), ("international_reputation", ALL), ("jumping", TOP),
              ("long_passing", HALF), ("long_shots", TOP), ("marking", TOP), ("overall_rating", ALL),
              ("penalties", TOP), ("positioning", HALF), ("potential", ALL), ("reactions", HALF),
              ("short_passing", HALF), ("shot_power", TOP), ("skill_moves", TOP), ("sliding_tackle", TOP),
              ("sprint_speed", TOP), ("stamina", FIELD), ("standing_tackle", HALF), ("strength", FIELD),
              ("vision", HALF), ("volleys", TOP), ("week_foot", HALF), ("weight", ALL)]

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
