import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score

from services import match as ms
import db.match_table as mt
from bet.unit_strategy import UnitStrategy
from bet.kelly_strategy import KellyStrategy
from bet.single_kelly_strategy import KellyStrategySingle
from bet.bet_utils import outcomes_from_odds
from logger import logging

class SeasonSimulator():
    def __init__(self, season_id, data_loader, predictor, conn):
        self.season_id = season_id
        self.data_loader = data_loader
        self.predictor = predictor
        self.conn = conn

        self.matches = []
        self.odds = None
        self.probabilities = None
        self.unit_strategy = None
        self.kelly_strategy = None
        self.kelly_strategy_single = None

    def run_match_simulations(self):
        matches = mt.get_matches_for_seasons([self.season_id], conn=self.conn)
        for _, match in matches.to_dict("index").items():
            feature_vector = self.data_loader.get_match_feature_vector(match, conn=self.conn)
            outcome_proba, outcome = self.predictor.predict(feature_vector)
            match["outcome_proba"] = outcome_proba
            match["predicted_outcome"] = outcome
            match["outcome"] = ms.get_match_outcome(match)

            logging.info(f'Simulating match {match["HomeTeam"]} - {match["AwayTeam"]} with id {match["id"]}. Outcome {match["predicted_outcome"]} {match["outcome_proba"]}')

            self.matches.append(match)

    def simulate_betting(self):
        df = pd.DataFrame(self.matches)
        y_pred = df["predicted_outcome"].values
        y_true = df["outcome"].values
        logging.info(f"Model's accuracy for season {self.season_id}: {accuracy_score(y_true, y_pred)}")
        self.probabilities = df["outcome_proba"].values
        self.odds = self.data_loader.get_odds_for_matches(self.matches, conn=self.conn)
        logging.info(f"Average overroundness of the odds: {np.mean([((1/odd[0] + 1/odd[1] + 1/odd[2])-1) for odd in self.odds])}")
        bet_outcomes = outcomes_from_odds(self.odds)
        logging.info(f"Betting market accuracy for season {self.season_id}: {accuracy_score(y_true, bet_outcomes)}")

        self.unit_strategy = UnitStrategy(y_true, y_pred)
        self.unit_strategy.run(self.odds)
        logging.info(f'Unit strategy profitability for season {self.season_id}: {self.unit_strategy.get_total_profit()}')

        self.kelly_strategy = KellyStrategy(y_true)
        self.kelly_strategy.run(self.odds, self.probabilities)
        logging.info(f'Kelly strategy profitability for season {self.season_id}: {self.kelly_strategy.get_total_profit()}')

        self.kelly_strategy_single = KellyStrategySingle(y_true, y_pred)
        self.kelly_strategy_single.run(self.odds, self.probabilities)
        logging.info(f'Kelly strategy single profitability for season {self.season_id}: {self.kelly_strategy_single.get_total_profit()}')

    def run(self):
        self.run_match_simulations()
        self.simulate_betting()
