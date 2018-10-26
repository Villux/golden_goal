import numpy as np
from sklearn.metrics import accuracy_score, log_loss
import matplotlib.pyplot as plt

from models.model_utils import get_feature_importance
from utils import write_as_json

def run(model, data_loader, original_features, n_iter):
    feature_set = original_features.copy()

    avg_accuracies = []
    avg_log_loss = []
    removed_features = []

    while feature_set:
        data_loader.set_feature_columns(feature_set)

        accuracies = []
        log_losses = []
        feature_values = {}
        for _ in range(n_iter):
            X_train, y_train, X_test, y_test = data_loader.get_train_and_test_dataset(random_state=None)
            model.fit(X_train, y_train)

            y_true, y_pred = y_test, model.predict(X_test)
            accuracies.append(accuracy_score(y_true, y_pred))
            y_true, y_prob = y_test, model.predict_proba(X_test)
            log_losses.append(log_loss(y_true, y_prob))

            feature_dict = get_feature_importance(model.feature_importances_, feature_set)
            for key, value in feature_dict.items():
                if key in feature_values:
                    feature_values[key] = feature_values[key] + [value]
                else:
                    feature_values[key] = [value]

        feature_scores = []
        for key, value in feature_values.items():
            feature_scores.append((key, np.mean(value)))

        feature_scores = sorted(feature_scores, key = lambda t: t[1], reverse=True)
        last_feature, _ = feature_scores[-1]

        feature_set.remove(last_feature)

        removed_features.append(last_feature)
        avg_accuracies.append(np.mean(accuracies))
        avg_log_loss.append(np.mean(log_losses))

    return avg_accuracies, avg_log_loss, removed_features


def plot_feature_selection(avg_accuracies, avg_log_loss, removed_features, prefix):
    figsize = (12, 6)
    plt.subplots(figsize=figsize)
    plt.plot(removed_features, avg_accuracies)
    plt.xticks(rotation='vertical')
    plt.xlabel('Accuracy')
    plt.ylabel('Removed feature')
    plt.savefig(f"img/{prefix}_accuracy.png")

    plt.subplots(figsize=figsize)
    plt.plot(removed_features, avg_log_loss)
    plt.xticks(rotation='vertical')
    plt.xlabel('Log loss')
    plt.ylabel('Removed feature')
    plt.savefig(f"img/{prefix}_logloss.png")

def store_results(avg_accuracies, avg_log_loss, removed_features, prefix):
    data = {
        "avg_accuracies": avg_accuracies,
        "avg_log_loss": avg_log_loss,
        "removed_features": removed_features
    }

    write_as_json(data, f"img/meta/{prefix}_feature_selection")

if __name__ == "__main__":
    from models.outcome_model import get_model, get_default_param
    from services.data_provider import DataLoader, feature_columns
    import pdb
    dl = DataLoader(feature_columns, "outcome")
    clf = get_model(get_default_param())

    accuracy, log_loss, remove_feat = run(clf, dl, feature_columns, 1)
    pdb.set_trace()
    store_results(accuracy, log_loss, remove_feat, "outcome_model")
    plot_feature_selection(accuracy, log_loss, remove_feat, "outcome_model")
