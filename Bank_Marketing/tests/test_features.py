import pandas as pd

from bank_marketing.features import FEATURES, build_features


def test_features_use_only_what_is_known_before_the_call():
    # duration is only known when the call ends; month and day mostly mark the period (notebook, section 2.3)
    assert not {'duration', 'month', 'day', 'y', 'subscribed', 'date'} & set(FEATURES)


def test_build_features(calls):
    features = build_features(calls)
    assert list(features[FEATURES].columns) == FEATURES
    assert len(features) == len(calls)
    assert not features[FEATURES].isna().any().any()


def test_feature_transformations(calls):
    sample = calls.head(3).copy()
    sample[['pdays', 'campaign', 'previous', 'balance']] = [[-1, 63, 0, 0], [100, 2, 1, -10], [400, 10, 40, 10]]
    features = build_features(sample)
    assert features['days_since_previous'].tolist() == ['never', '3-6 months', 'over 12 months']
    assert features['calls_this_campaign'].tolist() == [10, 2, 10]
    assert features['previous_calls'].tolist() == [0, 1, 10]
    assert features['balance'].iloc[0] == 0 and features['balance'].iloc[1] < 0 < features['balance'].iloc[2]
    assert isinstance(features, pd.DataFrame) and sample['campaign'].iloc[0] == 63   # input unchanged
