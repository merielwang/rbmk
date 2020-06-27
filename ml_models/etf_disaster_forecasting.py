import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import fbeta_score, make_scorer
from sklearn.model_selection import GridSearchCV


def train_test_split_weights(t_feature, t_label, t_weights, test_size=0.3):
    divider = round((1-test_size)*len(t_feature))
    X_train = t_feature[:divider]
    X_test = t_feature[divider:]
    y_train = t_label[:divider]
    y_test = t_label[divider:]
    w_train = t_weights[:divider]
    w_test = t_weights[divider:]
    return X_train, X_test, y_train, y_test, w_train, w_test


def svc_modeling(t_feature, t_label, weights=None):
    # X_train, X_test, y_train, y_test = train_test_split(t_feature, t_label, test_size=0.3, random_state=0)
    X_train, X_test, y_train, y_test, w_train, w_test = train_test_split_weights(t_feature, t_label, weights, test_size=0.4)
    clf = SVC(kernel="rbf", C=1, gamma='scale')
    # scores = cross_val_score(clf, X_train, y_train.values.ravel(), cv=5)
    clf.fit(X_train, y_train.values.ravel(), sample_weight=w_train.values.ravel())
    if weights is not None:
        score = clf.score(X_test, y_test.values.ravel(), sample_weight=w_test.values.ravel())
    else:
        score = clf.score(X_test, y_test.values.ravel())
    print(score)

    return clf



