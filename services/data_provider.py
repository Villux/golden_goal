import pandas as pd
import numpy as np

feature_columns = ["acceleration", "age", "aggression", "agility", "balance", "ball_control",
                "crossing", "curve", "dribbling", "finishing", "fk_accuracy", "gk_diving", "gk_handling",
                "gk_kicking", "gk_positioning", "gk_reflexes", "growth", "heading_accuracy", "height",
                "interceptions", "jumping", "long_passing", "long_shots", "marking", "overall_rating",
                "penalties", "positioning", "potential", "reactions", "short_passing", "shot_power",
                "skill_moves", "sliding_tackle", "sprint_speed", "stamina", "standing_tackle", "strength",
                "vision", "volleys", "weight", "xg", "goal_mean", "elo"]

def get_feature_matrix(df, features):
    X = pd.DataFrame()
    for feature in features:
        X[feature] = df[f"home_{feature}"].dropna() - df[f"away_{feature}"].dropna()
    return X


def get_dataset(label, path="master_data.csv"):
    df = pd.read_csv(path)
    X = get_feature_matrix(df, feature_columns)
    if label == "outcome":
        df["outcome"] = np.sign(df["FTHG"] - df["FTAG"])
    X = X.dropna()
    y = df.loc[X.index, label]
    return X, y
