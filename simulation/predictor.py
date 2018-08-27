import numpy as np

class OutcomePredictor():
    def __init__(self, model):
        self.model = model

    def predict_outcome_probabilities(self, x):
        return self.model.predict_proba(x)[0]

    def predict(self, feature_vector):
        outcome_proba = self.predict_outcome_probabilities(feature_vector)
        outcome = np.argmax(outcome_proba) - 1
        return np.flip(outcome_proba, axis=0), outcome
