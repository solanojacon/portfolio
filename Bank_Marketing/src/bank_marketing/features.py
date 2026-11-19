"""Model features. Used both to train the model (notebook and pipeline) and to score new calls."""

import numpy as np
import pandas as pd

CATEGORICAL = ['job', 'marital', 'education', 'default', 'housing', 'loan', 'contact',
               'previous_outcome', 'days_since_previous']
NUMERIC = ['age', 'balance', 'calls_this_campaign', 'previous_calls']
FEATURES = CATEGORICAL + NUMERIC


def build_features(calls):
    """Turns the raw call columns into model features. Uses only what is known before the call."""
    features = calls[['job', 'marital', 'education', 'default', 'housing', 'loan', 'contact', 'age',
                      'month', 'day']].copy()
    features['previous_outcome'] = calls['poutcome']
    days_since = pd.cut(calls['pdays'].where(calls['pdays'] >= 0), [0, 90, 180, 270, 365, 1000],
                        labels=['under 3 months', '3-6 months', '6-9 months', '9-12 months', 'over 12 months'])
    features['days_since_previous'] = days_since.cat.add_categories('never').fillna('never').astype(str)
    features['balance'] = np.sign(calls['balance']) * np.log1p(calls['balance'].abs())
    features['calls_this_campaign'] = calls['campaign'].clip(upper=10)
    features['previous_calls'] = calls['previous'].clip(upper=10)
    return features
