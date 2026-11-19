import numpy as np
import pandas as pd

from bank_marketing import monitor


def test_psi_is_zero_without_drift_and_high_with_it():
    rng = np.random.default_rng(0)
    reference = monitor.profile(rng.normal(0, 1, 5000))
    assert monitor.psi(reference, rng.normal(0, 1, 5000)) < 0.02
    assert monitor.psi(reference, rng.normal(1, 1, 5000)) > monitor.DRIFT_ALERT


def test_psi_handles_categories_unseen_in_training():
    reference = monitor.profile(pd.Series(['a'] * 50 + ['b'] * 50))
    assert monitor.psi(reference, pd.Series(['a'] * 50 + ['b'] * 50)) == 0
    assert monitor.psi(reference, pd.Series(['a'] * 50 + ['c'] * 50)) > monitor.DRIFT_ALERT


def test_calibration_matches_the_observed_rate():
    rng = np.random.default_rng(0)
    y = rng.random(2000) < 0.5
    scores = np.clip(0.2 + 0.1 * y + rng.normal(0, 0.05, 2000), 0.01, 0.99)   # ranks well, but averages 0.25
    calibrated = monitor.calibrate(scores, monitor.fit_calibration(scores, y))
    assert abs(calibrated.mean() - y.mean()) < 0.01
    assert (np.argsort(calibrated) == np.argsort(scores)).all()   # the ranking is unchanged
