import pandas as pd

from services import match as ms
import db.match_table as mt
from bet.unit_strategy import UnitStrategy
from bet.kelly_strategy import KellyStrategy

class SeasonSimulator():
    def __init__(self, season_id, data_loader, predictor, conn):
        self.season_id = season_id
        self.data_loader = data_loader
        self.predictor = predictor
        self.conn = conn

        self.matches = []
        self.unit_strategy = None
        self.kelly_strategy = None

    def run_match_simulations(self):
        matches = mt.get_matches_for_seasons([self.season_id], conn=self.conn)
        for _, match in matches.to_dict("index").items():
            feature_vector = self.data_loader.get_match_feature_vector(match, conn=self.conn)
            outcome_proba, outcome = self.predictor.predict(feature_vector)
            match["outcome_proba"] = outcome_proba
            match["predicted_outcome"] = outcome
            match["outcome"] = ms.get_match_outcome(match)

            self.matches.append(match)

    def simulate_betting(self):
        df = pd.DataFrame(self.matches)
        y_pred = df["predicted_outcome"]
        y_true = df["outcome"]
        probabilities = df["outcome_proba"]
        odds = self.data_loader.get_odds_for_matches(self.matches, "William Hill", conn=self.conn)

        self.unit_strategy = UnitStrategy(y_pred, y_true)
        self.unit_strategy.run(odds)

        self.kelly_strategy = KellyStrategy(y_true)
        self.kelly_strategy.run(odds, probabilities)

    def run(self):
        self.run_match_simulations()
        self.simulate_betting()
