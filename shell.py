import ipdb
from db.interface import open_connection
from simulation.season_simulator import SeasonSimulator
from simulation.predictor import OutcomePredictor
from services.data_provider import DataLoader, feature_columns
from models.outcome_model import get_model, get_default_param

conn = open_connection()

season_id = 65
data_loader = DataLoader(feature_columns, "outcome", filter_season=[season_id])
X, y = data_loader.get_dataset()
model = get_model(get_default_param(), X, y)
predictor = OutcomePredictor(model)

simulator = SeasonSimulator(season_id, data_loader, predictor, conn)
simulator.run()

ipdb.set_trace()
