import numpy as np

def outcomes_from_odds(odds):
    outcomes = []
    for (home, draw, away) in odds:
        outcomes.append(np.argmin([away, draw, home]) - 1)
    return outcomes
