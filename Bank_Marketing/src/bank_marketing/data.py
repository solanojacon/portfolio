"""Reading the calls and rebuilding their dates."""

import pandas as pd

MONTHS = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
FIRST_YEAR = 2008   # the dataset documentation: calls from May 2008 to November 2010, ordered by date


def prepare_calls(raw):
    """Adds the full date of each call and the 0/1 target `subscribed`.

    The file gives only the month and day of the last call, but its rows are in date order:
    the (month, day) pair only goes backwards when a new year starts.
    """
    month_number = raw['month'].map({m: i for i, m in enumerate(MONTHS, 1)})
    goes_back = (month_number * 100 + raw['day']).diff() < 0
    calls = raw.copy()
    calls['date'] = pd.to_datetime(pd.DataFrame({'year': FIRST_YEAR + goes_back.cumsum(), 'month': month_number,
                                                 'day': raw['day']}))
    calls['subscribed'] = (calls['y'] == 'yes').astype(int)
    return calls


def read_calls(path):
    """Reads `bank-full.csv` (semicolon-separated) and prepares it with `prepare_calls`."""
    from bank_marketing import storage  # imported here: the notebook uses this module without the pipeline extras
    return prepare_calls(storage.read_csv(path, sep=';'))
