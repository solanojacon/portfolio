"""Monitoring: ranking quality, drift and calibration of the scores."""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

TOP_SHARE = 0.3       # the calling policy used in the notebook: call the top 30% by score
DRIFT_ALERT = 0.25    # population stability index (PSI) above 0.25 is usually read as a major shift
MIN_ROC_AUC = 0.60    # validation ROC AUC of the chosen model in the notebook (section 5.2)
CALIBRATION_ALERT = 0.10   # mean calibrated score more than 10 points away from the observed rate
_FLOOR = 1e-4         # keeps PSI finite when a bin is empty


def profile(values):
    """Reference distribution of a feature or of the scores: decile bins for numbers, shares for categories."""
    values = pd.Series(values)
    if pd.api.types.is_numeric_dtype(values):
        edges = np.unique(np.quantile(values, np.linspace(0.1, 0.9, 9))).tolist()
        return {'edges': edges, 'shares': _bin_shares(edges, values)}
    return {'shares': values.value_counts(normalize=True).to_dict()}


def _bin_shares(edges, values):
    bins = np.searchsorted(edges, np.asarray(values, dtype=float), side='right')
    return (np.bincount(bins, minlength=len(edges) + 1) / len(bins)).tolist()


def psi(reference, values):
    """Population stability index of `values` against a reference `profile`."""
    if 'edges' in reference:
        expected, actual = np.array(reference['shares']), np.array(_bin_shares(reference['edges'], values))
    else:
        actual_shares = pd.Series(values).value_counts(normalize=True)
        categories = sorted(set(reference['shares']) | set(actual_shares.index))
        expected = np.array([reference['shares'].get(c, 0) for c in categories])
        actual = np.array([actual_shares.get(c, 0) for c in categories])
    expected, actual = np.maximum(expected, _FLOOR), np.maximum(actual, _FLOOR)
    return float(np.sum((actual - expected) * np.log(actual / expected)))


def performance(y, scores):
    """Ranking quality on calls whose outcome is known."""
    y, scores = np.asarray(y), np.asarray(scores)
    top = np.argsort(-scores)[:max(1, int(TOP_SHARE * len(y)))]
    deciles = 10 - pd.qcut(pd.Series(scores).rank(method='first'), 10, labels=False)
    return {
        'calls': len(y),
        'subscription_rate': float(y.mean()),
        'roc_auc': float(roc_auc_score(y, scores)) if 0 < y.sum() < len(y) else None,
        'top_30_subscription_rate': float(y[top].mean()),
        'subscription_rate_by_decile': pd.Series(y).groupby(deciles.to_numpy()).mean().round(3).tolist(),
    }


def fit_calibration(scores, y):
    """Platt scaling: maps the scores to probabilities that match the latest observed outcomes."""
    y = np.asarray(y)
    if not 0 < y.sum() < len(y):
        return None
    calibrator = LogisticRegression(C=1e6).fit(_logit(scores), y)
    return {'slope': float(calibrator.coef_[0, 0]), 'intercept': float(calibrator.intercept_[0])}


def calibrate(scores, calibration):
    if calibration is None:
        return np.asarray(scores)
    return 1 / (1 + np.exp(-(calibration['slope'] * _logit(scores)[:, 0] + calibration['intercept'])))


def _logit(scores):
    p = np.clip(np.asarray(scores, dtype=float), 1e-6, 1 - 1e-6)
    return np.log(p / (1 - p)).reshape(-1, 1)
