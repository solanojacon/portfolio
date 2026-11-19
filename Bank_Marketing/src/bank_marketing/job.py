"""The monthly batch job.

At the start of each month, `run_month`:

1. Closes the previous month, whose call outcomes are now known: ranking quality, calibration and drift.
2. Retrains with champion/challenger. Two training recipes compete: all history, or only the last 12 months.
   Each is fitted on the calls before the previous month and judged on it. The challenger recipe replaces the
   champion's only if it ranks the previous month better. The winning recipe is then refitted with the calls
   up to now, and that model becomes the new champion.
3. Recalibrates the scores on the previous month's outcomes.
4. Scores the clients of the new month with the champion.
"""

import pandas as pd
from sklearn.metrics import roc_auc_score

from bank_marketing import monitor, storage
from bank_marketing.features import FEATURES, build_features
from bank_marketing.model import score, train
from bank_marketing.registry import Registry

RECIPES = {'all history': None, 'last 12 months': 12}   # months of training data (None: all)


def training_calls(calls, before, recipe):
    """Calls with a known outcome before the month `before`, as used by a training recipe."""
    history = calls[calls['date'] < before.start_time]
    months = RECIPES[recipe]
    return history if months is None else history[history['date'] >= (before - months).start_time]


def train_first_model(calls, output_dir, before):
    """Trains the first champion on all calls before the month `before` (for example '2010-01'), as in the notebook."""
    before = pd.Period(before, 'M')
    return _promote(Registry(output_dir), calls, before, 'all history', validation=None)


def run_month(calls, output_dir, month):
    """Runs the job at the start of `month`. Returns the report on the previous month, if it was scored."""
    month = pd.Period(month, 'M')
    previous = month - 1
    scores_path = storage.join(output_dir, 'scores', f'{previous}.csv')
    report = _close_month(calls, output_dir, previous, month) if storage.exists(scores_path) else None

    batch = calls[calls['date'].dt.to_period('M') == month]
    if len(batch):
        model, info = Registry(output_dir).champion()
        calibration_path = storage.join(output_dir, 'calibration.json')
        calibration = storage.read_json(calibration_path) if storage.exists(calibration_path) else None
        raw = score(model, batch)
        storage.write_csv(storage.join(output_dir, 'scores', f'{month}.csv'), pd.DataFrame({
            'call_id': batch.index, 'model': info['version'],
            'score': raw, 'calibrated_score': monitor.calibrate(raw, calibration),
        }))
    return report


def _close_month(calls, output_dir, previous, month):
    registry = Registry(output_dir)
    _, info = registry.champion()   # the model that scored the previous month
    scored = storage.read_csv(storage.join(output_dir, 'scores', f'{previous}.csv'))
    outcomes = calls.loc[scored['call_id']]
    y = outcomes['subscribed'].to_numpy()

    features = build_features(outcomes)[FEATURES]
    drift = {column: monitor.psi(info['profiles'][column], features[column]) for column in FEATURES}
    report = {
        'month': str(previous),
        'model': info['version'],
        'performance': monitor.performance(y, scored['score']),
        'calibration': {'subscription_rate': float(y.mean()), 'mean_score': float(scored['score'].mean()),
                        'mean_calibrated_score': float(scored['calibrated_score'].mean())},
        'drift': {'score': monitor.psi(info['profiles']['score'], scored['score']), 'features': drift},
    }

    champion_recipe = info['recipe']
    challenger_recipe = next(recipe for recipe in RECIPES if recipe != champion_recipe)
    challenger_scores = score(train(training_calls(calls, previous, challenger_recipe)), outcomes)
    champion_auc = report['performance']['roc_auc']
    challenger_auc = float(roc_auc_score(y, challenger_scores)) if champion_auc is not None else None
    switch = champion_auc is not None and challenger_auc > champion_auc
    recipe = challenger_recipe if switch else champion_recipe
    validation = {'month': str(previous), 'champion_recipe': champion_recipe, 'champion_roc_auc': champion_auc,
                  'challenger_recipe': challenger_recipe, 'challenger_roc_auc': challenger_auc}
    retraining = {**validation, 'recipe_in_use': recipe,
                  'new_version': _promote(registry, calls, month, recipe, validation)}
    report['retraining'] = retraining

    # Fitted on the previous month's scores of the recipe now in use, from a model that had not seen that month.
    calibration = monitor.fit_calibration(challenger_scores if switch else scored['score'], y)
    if calibration is not None:
        storage.write_json(storage.join(output_dir, 'calibration.json'), {'fitted_on': str(previous), **calibration})

    report['alerts'] = _alerts(report)
    storage.write_json(storage.join(output_dir, 'reports', f'{previous}.json'), report)
    return report


def _promote(registry, calls, before, recipe, validation):
    """Fits `recipe` on the calls before the month `before` and makes it the champion."""
    history = training_calls(calls, before, recipe)
    model = train(history)
    features = build_features(history)[FEATURES]
    return registry.promote(model, {
        'recipe': recipe,
        'trained_on': f'{history["date"].min():%Y-%m-%d} to {history["date"].max():%Y-%m-%d}',
        'training_calls': len(history),
        'training_subscription_rate': float(history['subscribed'].mean()),
        'validation': validation,
        'profiles': {**{column: monitor.profile(features[column]) for column in FEATURES},
                     'score': monitor.profile(score(model, history))},
    })


def _alerts(report):
    alerts = []
    auc = report['performance']['roc_auc']
    if auc is not None and auc < monitor.MIN_ROC_AUC:
        alerts.append(f'ROC AUC {auc:.2f} below {monitor.MIN_ROC_AUC:.2f}')
    if report['drift']['score'] > monitor.DRIFT_ALERT:
        alerts.append(f'score drift (PSI {report["drift"]["score"]:.2f})')
    alerts += [f'{column} drift (PSI {value:.2f})' for column, value in report['drift']['features'].items()
               if value > monitor.DRIFT_ALERT]
    gap = abs(report['calibration']['mean_calibrated_score'] - report['calibration']['subscription_rate'])
    if gap > monitor.CALIBRATION_ALERT:
        alerts.append(f'calibrated scores off by {gap:.0%} from the subscription rate')
    return alerts
