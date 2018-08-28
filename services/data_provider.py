import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from services import elo, match as ms, player
from db import odds_table as ot
from logger import logging

feature_columns = ["acceleration", "age", "aggression", "agility", "balance", "ball_control",
                "crossing", "curve", "dribbling", "finishing", "fk_accuracy", "gk_diving", "gk_handling",
                "gk_kicking", "gk_positioning", "gk_reflexes", "growth", "heading_accuracy", "height",
                "interceptions", "jumping", "long_passing", "long_shots", "marking", "overall_rating",
                "penalties", "positioning", "potential", "reactions", "short_passing", "shot_power",
                "skill_moves", "sliding_tackle", "sprint_speed", "stamina", "standing_tackle", "strength",
                "vision", "volleys", "weight", "xg", "goal_mean", "elo"]

class DataLoader():
    def __init__(self, features, label, filter_season=[], path="master_data.csv"):
        self.feature_columns = features
        self.filter_season = filter_season
        self.label = label
        self.path = path

    def filter_data(self, dataset):
        return dataset.loc[~dataset['season_id'].isin(self.filter_season)]

    def get_feature_matrix(self, df):
        X = pd.DataFrame()
        for feature in self.feature_columns:
            X[feature] = df[f"home_{feature}"].dropna() - df[f"away_{feature}"].dropna()
        return X

    def load_dataset(self):
        df = pd.read_csv(self.path)
        return self.filter_data(df)

    def get_train_and_test_dataset(self, random_state=42):
        X, y = self.get_dataset()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=random_state)
        return X_train, y_train, X_test, y_test

    def get_dataset(self):
        df = self.load_dataset()
        X = self.get_feature_matrix(df)
        df["outcome"] = np.sign(df["FTHG"] - df["FTAG"])

        X = X.dropna()
        y = df.loc[X.index, self.label]
        logging.debug(f"Dataset size: {X.shape}")
        return X, y

    def get_match_feature_vector(self, match, **kwargs):
        data_merge_obj = {"HomeTeam": match["HomeTeam"], "AwayTeam": match["AwayTeam"], "Date": match["Date"], "id": match["id"]}

        N = 20
        data_merge_obj["home_elo"] = elo.get_elo_and_id(match["HomeTeam"], match["Date"], match["season_id"], **kwargs)[0]
        data_merge_obj["home_xg"] = ms.calculate_xg(match["HomeTeam"], match["Date"], N, combination=ms.HOMEAWAY, **kwargs)
        data_merge_obj["home_goal_mean"] = ms.calculate_goal_average(match["HomeTeam"], match["Date"], N, **kwargs)

        data_merge_obj["away_elo"] = elo.get_elo_and_id(match["AwayTeam"], match["Date"], match["season_id"], **kwargs)[0]
        data_merge_obj["away_xg"] = ms.calculate_xg(match["AwayTeam"], match["Date"], N, combination=ms.HOMEAWAY, **kwargs)
        data_merge_obj["away_goal_mean"] = ms.calculate_goal_average(match["AwayTeam"], match["Date"], N, **kwargs)

        home, away = player.get_team_features_for_matches(match["HomeTeam"], match["AwayTeam"], match["Date"], **kwargs)

        data_merge_obj = {**data_merge_obj, **home, **away}
        return self.get_feature_matrix(pd.DataFrame([data_merge_obj]))

    def get_odds_for_matches(self, matches, odds_provider, **kwargs):
        output = []
        for match in matches:
            home_win, draw, away_win = ot.get_for_match(match["id"], odds_provider, **kwargs)
            output.append(np.array([home_win, draw, away_win]))
        return output
