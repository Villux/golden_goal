from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

def get_default_param():
    return {'max_depth': 5, 'max_features': 'log2', 'min_samples_leaf': 1,
            'n_estimators': 2000, "oob_score": True, "bootstrap": True, "n_jobs": -1}

def run_grid_search(grid, data_loader):
    X, y = data_loader.get_dataset()

    tuning = GridSearchCV(
        estimator=RandomForestClassifier(oob_score=True, bootstrap=True, n_jobs=-1),
        param_grid=grid,
        scoring='neg_log_loss',
        n_jobs=-1,
        cv=5)
    tuning.fit(X, y)

    print("Grid scores on development set:")
    print()
    means = tuning.cv_results_['mean_test_score']
    stds = tuning.cv_results_['std_test_score']
    for mean, std, params in zip(means, stds, tuning.cv_results_['params']):
        print("%0.3f (+/-%0.03f) for %r"
              % (mean, std * 2, params))
    print()

    return tuning.best_params_, tuning.best_score_

def get_model(params, X=None, y=None):
    model = RandomForestClassifier(**params)
    if (X is not None) and (y is not None):
        model.fit(X, y)
    return model

if __name__ == "__main__":
    from services.data_provider import DataLoader, feature_columns
    param_grid = {
        'max_depth': [3, 5, 8, 12, None],
        'min_samples_leaf': [1, 3, 5, 10, 15],
        'max_features': ["sqrt", "log2"],
        'n_estimators': [2000]
    }
    dl = DataLoader(feature_columns, "outcome")
    best_params, score = run_grid_search(param_grid, dl)
    print("Best params", best_params, score)
