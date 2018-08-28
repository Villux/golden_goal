from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier

from services.data_provider import DataLoader, feature_columns

def get_default_param():
    return {'n_neighbors': 5, "n_jobs": -1}

def run_grid_search(grid, data_loader):
    X, y = data_loader.get_dataset()

    tuning = GridSearchCV(
        estimator=KNeighborsClassifier(n_jobs=-1),
        param_grid=grid,
        scoring='accuracy',
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
    model = KNeighborsClassifier(**params)
    if (X is not None) and (y is not None):
        model.fit(X, y)
    return model

if __name__ == "__main__":
    param_grid = {
        'n_neighbors': [3, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    }
    dl = DataLoader(feature_columns, "outcome")
    best_params, score = run_grid_search(param_grid, dl)
    print("Best params", best_params, score)
