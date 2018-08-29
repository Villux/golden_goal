def get_feature_importance(feature_importances, feature_columns):
    zipped = sorted(zip(feature_columns, feature_importances), key = lambda t: t[1], reverse=True)
    D = {}
    for feature, importance in zipped:
        D[feature] = round(importance, 5)
    return D
