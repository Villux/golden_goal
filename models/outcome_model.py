from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

from services.data_provider import get_dataset

def run_grid_search(grid):
    X, y = get_dataset("master_data.csv")

    tuning = GridSearchCV(
        estimator=RandomForestClassifier(oob_score=True, bootstrap=True, n_jobs=-1),
        param_grid=grid,
        scoring='accuracy',
        cv=5)
    tuning.fit(X, y)
    return tuning.best_params_, tuning.best_score_

if __name__ == "__main__":
    param_grid = {
        'max_depth': [3, 5, 8, 12, None],
        'min_samples_leaf': [1, 3, 5, 10, 15],
        'max_features': ["sqrt", "log2"],
        'n_estimators': [2000]
    }
    params, score = run_grid_search(param_grid)
    print("Best params", params, score)
