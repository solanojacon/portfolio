import numpy as np
import pandas as pd
import pytest

from bank_marketing.data import MONTHS, prepare_calls


def make_raw(start='2008-05-01', end='2010-06-30', calls_per_day=15, seed=0):
    """Random calls with the columns and row order of bank-full.csv, and a target that depends on the features."""
    rng = np.random.default_rng(seed)
    dates = pd.DatetimeIndex(np.repeat(pd.bdate_range(start, end), calls_per_day))
    n = len(dates)
    poutcome = rng.choice(['unknown', 'failure', 'success', 'other'], n, p=[0.7, 0.15, 0.1, 0.05])
    contact = rng.choice(['cellular', 'telephone', 'unknown'], n, p=[0.6, 0.1, 0.3])
    pdays = np.where(poutcome == 'unknown', -1, rng.integers(1, 500, n))
    logit = -2 + 2.5 * (poutcome == 'success') + 0.5 * (contact == 'cellular')
    return pd.DataFrame({
        'age': rng.integers(18, 90, n),
        'job': rng.choice(['admin.', 'blue-collar', 'retired', 'student', 'unknown'], n),
        'marital': rng.choice(['married', 'single', 'divorced'], n),
        'education': rng.choice(['primary', 'secondary', 'tertiary', 'unknown'], n),
        'default': rng.choice(['no', 'yes'], n, p=[0.98, 0.02]),
        'balance': rng.integers(-2000, 20000, n),
        'housing': rng.choice(['no', 'yes'], n),
        'loan': rng.choice(['no', 'yes'], n),
        'contact': contact,
        'day': dates.day,
        'month': [MONTHS[m - 1] for m in dates.month],
        'duration': rng.integers(0, 2000, n),
        'campaign': rng.integers(1, 30, n),
        'pdays': pdays,
        'previous': np.where(pdays < 0, 0, rng.integers(1, 20, n)),
        'poutcome': poutcome,
        'y': np.where(rng.random(n) < 1 / (1 + np.exp(-logit)), 'yes', 'no'),
    }), dates


@pytest.fixture(scope='session')
def raw():
    """(raw calls, their true dates)."""
    return make_raw()


@pytest.fixture(scope='session')
def calls(raw):
    return prepare_calls(raw[0])
