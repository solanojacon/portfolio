import numpy as np

from bank_marketing import storage
from bank_marketing.job import run_month, train_first_model
from bank_marketing.model import score
from bank_marketing.registry import Registry


def test_monthly_job(calls, tmp_path):
    output = str(tmp_path)
    assert train_first_model(calls, output, '2010-01') == 'v001'
    assert run_month(calls, output, '2010-01') is None   # nothing scored before: only scores January

    reports = [run_month(calls, output, month) for month in ['2010-02', '2010-03', '2010-04']]
    assert [report['month'] for report in reports] == ['2010-01', '2010-02', '2010-03']
    for report in reports:
        assert 0 <= report['performance']['roc_auc'] <= 1
        assert report['retraining']['recipe_in_use'] in ('all history', 'last 12 months')
        assert storage.exists(storage.join(output, 'reports', f'{report["month"]}.json'))

    registry = Registry(output)
    assert registry.champion_version() == 'v004'   # one new champion each month
    model, info = registry.champion()
    april = storage.read_csv(storage.join(output, 'scores', '2010-04.csv'))
    assert (april['model'] == 'v004').all()
    assert np.allclose(april['score'], score(model, calls.loc[april['call_id']]))   # saved model reproduces the scores
    assert info['validation']['month'] == '2010-03'
