from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

from services.data_provider import DataLoader, feature_columns
from db.interface import open_connection, close_connection

def get_default_param():
    return {'max_depth': 8, 'max_features': 'log2', 'min_samples_leaf': 3, 'n_estimators': 2000, "oob_score": True, "bootstrap": True, "n_jobs": -1}

def run_grid_search(grid):
    conn = open_connection()
    data_loader = DataLoader(feature_columns, "outcome", conn)
    X, y = data_loader.get_dataset()

    tuning = GridSearchCV(
        estimator=RandomForestClassifier(oob_score=True, bootstrap=True, n_jobs=-1),
        param_grid=grid,
        scoring='accuracy',
        cv=5)
    tuning.fit(X, y)

    close_connection(conn)
    return tuning.best_params_, tuning.best_score_

def get_model(params, X=None, y=None):
    model = RandomForestClassifier(**params)
    if (X is not None) and (y is not None):
        model.fit(X, y)
    return model

if __name__ == "__main__":
    param_grid = {
        'max_depth': [3, 5, 8, 12, None],
        'min_samples_leaf': [1, 3, 5, 10, 15],
        'max_features': ["sqrt", "log2"],
        'n_estimators': [2000]
    }
    best_params, score = run_grid_search(param_grid)
    print("Best params", best_params, score)
