import ipdb
import numpy as np
import pandas as pd

from db.interface import open_connection, fetchall, close_connection, execute_statement
from db import match_table as mt
from db import queries as q


conn = open_connection()

# season_id = 53
# data_loader = DataLoader(feature_columns, "outcome", filter_season=[season_id])
# X, y = data_loader.get_dataset()
# model = get_model(get_default_param(), X, y)
# predictor = OutcomePredictor(model)

# simulator = SeasonSimulator(season_id, data_loader, predictor, conn)
# simulator.run()
# plot_simulation(simulator)

# df = pd.DataFrame(simulator.matches)
# plot_probabilities_against_market(simulator.probabilities, get_implied_probabilities(simulator.odds), "outcome_model")

# teams_tuple = mt.get_teams_for_season(season_id, conn=conn)
# teams = [team_tuple[0] for team_tuple in teams_tuple]

# records = []
# for team in teams:
#     record = calculate_player_features_for_team(team, "2018-04-19", conn=conn)
#     records.append(record)

# df = pd.DataFrame(records)

ipdb.set_trace()

execute_statement(q.drop_player_identity_table, conn)
execute_statement(q.create_player_identity_table, conn)
execute_statement(q.create_fifa_id_index, conn)

execute_statement(q.drop_lineup_table, conn)
execute_statement(q.create_lineup_table, conn)
execute_statement(q.create_match_id_index, conn)
