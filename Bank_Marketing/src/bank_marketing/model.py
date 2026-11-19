"""The model: preprocessing and classifier in one scikit-learn pipeline."""

import warnings

from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from bank_marketing.features import CATEGORICAL, FEATURES, NUMERIC, build_features

CHOSEN_PARAMETERS = {'C': 0.01}   # chosen in the notebook (section 5.3)


def make_pipeline(model, categorical=CATEGORICAL, numeric=NUMERIC, scale=False):
    preprocess = ColumnTransformer([
        ('categorical', OneHotEncoder(drop='if_binary', handle_unknown='ignore', sparse_output=False), categorical),
        ('numeric', StandardScaler() if scale else 'passthrough', numeric),
    ])
    return Pipeline([('preprocess', preprocess), ('model', model)])


def make_model():
    """The model chosen in the notebook: a logistic regression on standardized features."""
    return make_pipeline(LogisticRegression(max_iter=2000, **CHOSEN_PARAMETERS), scale=True)


def train(calls):
    """Fits a new model on calls with a known outcome."""
    return make_model().fit(build_features(calls)[FEATURES], calls['subscribed'])


def score(model, calls):
    """Chance of subscribing for each call, as a score from 0 to 1."""
    with warnings.catch_warnings():   # a category unseen in training (for example, in a short window) is encoded as 0
        warnings.filterwarnings('ignore', message='Found unknown categories')
        return model.predict_proba(build_features(calls)[FEATURES])[:, 1]
