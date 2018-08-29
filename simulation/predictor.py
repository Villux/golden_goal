import numpy as np
from scipy.stats import poisson

class OutcomePredictor():
    def __init__(self, model):
        self.model = model

    def predict_outcome_probabilities(self, x):
        return self.model.predict_proba(x)[0]

    def predict(self, feature_vector):
        outcome_proba = self.predict_outcome_probabilities(feature_vector)
        outcome = np.argmax(outcome_proba) - 1
        return np.flip(outcome_proba, axis=0), outcome

class ScorePredictor():
    def __init__(self, model):
        self.model = model

    @staticmethod
    def get_goal_matrix(home_mu, away_mu):
        home_goal_prob, away_goal_prob = [[poisson.pmf(i, team_avg) for i in range(0, 11)] for team_avg in [home_mu, away_mu]]
        return np.outer(home_goal_prob, away_goal_prob)

    @staticmethod
    def get_outcome_probabilities(goal_matrix):
        home_win = np.sum(np.tril(goal_matrix, -1))
        draw = np.sum(np.diag(goal_matrix))
        away_win = np.sum(np.triu(goal_matrix, 1))

        return [home_win, draw, away_win]

    def predict_score(self, x):
        mu_score = self.model.predict(x)[0]
        return mu_score

    def predict(self, home_fv, away_fv):
        home_mu = self.predict_score(home_fv)
        away_mu = self.predict_score(away_fv)

        goal_matrix = self.get_goal_matrix(home_mu, away_mu)
        outcome_proba = self.get_outcome_probabilities(goal_matrix)

        outcome = np.argmax(outcome_proba) - 1
        return outcome_proba, outcome
