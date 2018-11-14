import numpy as np

from db import player_table as pt
from db import lineup_table as lt
from logger import logging

TOP = 4
HALF =  5
FIELD =  11
GK = 1
ALL = 25

field_list = [("acceleration", TOP, None), ("age", FIELD, "overall_rating"), ("aggression", TOP, None), ("agility", TOP, None),
              ("balance", TOP, None), ("ball_control", HALF, None), ("composure", TOP, None), ("crossing", HALF, None),
              ("curve", HALF, None), ("dribbling", HALF, None), ("finishing", TOP, None), ("fk_accuracy", TOP, None),
              ("gk_diving", GK, None), ("gk_handling", GK, None), ("gk_kicking", GK, None), ("gk_positioning", GK, None),
              ("gk_reflexes", GK, None), ("growth", HALF, None), ("heading_accuracy", HALF, None), ("height", FIELD, "overall_rating"),
              ("interceptions", HALF, None), ("jumping", TOP, None), ("long_passing", HALF, None), ("long_shots", TOP, None),
              ("marking", TOP, None), ("overall_rating", ALL, None), ("penalties", TOP, None), ("positioning", HALF, None),
              ("potential", ALL, None), ("reactions", HALF, None), ("short_passing", HALF, None), ("shot_power", TOP, None),
              ("skill_moves", TOP, None), ("sliding_tackle", TOP, None), ("sprint_speed", TOP, None), ("stamina", FIELD, None),
              ("standing_tackle", HALF, None), ("strength", FIELD, None), ("vision", HALF, None), ("volleys", TOP, None)]

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

def calculate_team_average(df):
    record = {}
    for (field, N, sort_key) in field_list:
        if not sort_key:
            sort_key = field
        sorted_df = df.sort_values(by=[sort_key], ascending=False)
        if sorted_df.shape[0] > 0:
            record[field] = sorted_df[field].iloc[0:N].mean()
        else:
            record[field] = None
    return record

def calculate_player_features_for_team(player_ids, date, **kwargs):
    dd_tuple = pt.get_last_data_date(date, **kwargs)
    if dd_tuple:
        data_date = dd_tuple[0]
        player_data = pt.get_data_for_player_ids(player_ids, data_date, **kwargs)
        record = calculate_team_average(player_data)
    else:
        record = {}
    return record

def get_team_features_for_matches(match_id, date, **kwargs):
    lineup = lt.get_by_match_id(match_id, **kwargs)
    if not lineup.shape[0]:
        return {}, {}

    home_players = lineup.loc[:, lineup.columns.str.startswith('hp')].values[0]
    home_subst = lineup.loc[:, lineup.columns.str.startswith('hs')].values[0]
    home_fifa_ids = [player for player in np.concatenate((home_players, home_subst)) if player]
    home_features = calculate_player_features_for_team(home_fifa_ids, date, **kwargs)
    if home_features["gk_handling"] < 60:
        logging.warning(f"No goalkeeper in home team's lineup!! Match id: {match_id}")
    home_features = {f'home_{k}': v for k, v in home_features.items()}

    away_players = lineup.loc[:, lineup.columns.str.startswith('ap')].values[0]
    away_subst = lineup.loc[:, lineup.columns.str.startswith('as')].values[0]
    away_fifa_ids = [player for player in np.concatenate((away_players, away_subst)) if player]
    away_features = calculate_player_features_for_team(away_fifa_ids, date, **kwargs)
    if away_features["gk_handling"] < 60:
        logging.warning(f"No goalkeeper in away team's lineup!! Match id: {match_id}")
    away_features = {f'away_{k}': v for k, v in away_features.items()}

    return home_features, away_features
