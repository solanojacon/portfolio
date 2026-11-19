from bank_marketing.data import prepare_calls


def test_dates_are_rebuilt_from_month_and_day(raw):
    raw, dates = raw
    calls = prepare_calls(raw)
    assert (calls['date'] == dates).all()
    assert set(calls['subscribed']) == {0, 1}
    assert 'date' not in raw   # the input is not modified
