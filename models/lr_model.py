from multiprocessing import cpu_count
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression

from services.data_provider import DataLoader, feature_columns

def get_default_param():
    return {'n_jobs': cpu_count(), "solver": "newton-cg", 'C': 0.001, 'penalty': 'l2'}

def run_grid_search(grid, data_loader):
    X, y = data_loader.get_dataset()

    tuning = GridSearchCV(
        estimator=LogisticRegression(n_jobs=cpu_count(), solver="newton-cg"),
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
    model = LogisticRegression(**params)
    if (X is not None) and (y is not None):
        model.fit(X, y)
    return model

if __name__ == "__main__":
    param_grid = {
        'penalty': ['l2'],
        'C': [0.001,0.01,0.1,1,10,100,1000]
    }

    dl = DataLoader(feature_columns, "outcome")
    best_params, score = run_grid_search(param_grid, dl)
    print("Best params", best_params, score)
