"""Replays the monthly job over past data, as if it had run in production."""

import pandas as pd
from sklearn.metrics import roc_auc_score

from bank_marketing import storage
from bank_marketing.job import run_month, train_first_model
from bank_marketing.model import score
from bank_marketing.registry import Registry


def simulate(calls, output_dir, start):
    """Trains the first model on the calls before `start`, then runs the job every month until the data ends.

    Returns one row per month, with the first model kept frozen as a comparison.
    """
    first_version = train_first_model(calls, output_dir, start)
    last_month = calls['date'].max().to_period('M')
    reports = [report for month in pd.period_range(start, last_month + 1, freq='M')
               if (report := run_month(calls, output_dir, month))]

    frozen, _ = Registry(output_dir).load(first_version)
    rows = []
    for report in reports:
        month_scores = storage.read_csv(storage.join(output_dir, 'scores', f'{report["month"]}.csv'))
        outcomes = calls.loc[month_scores['call_id']]
        month_scores['subscribed'] = outcomes['subscribed'].to_numpy()
        month_scores['frozen_score'] = score(frozen, outcomes)
        rows.append({
            'month': report['month'],
            'model': report['model'],
            'calls': report['performance']['calls'],
            'subscription_rate': report['performance']['subscription_rate'],
            'roc_auc': report['performance']['roc_auc'],
            'frozen_model_roc_auc': roc_auc_score(month_scores['subscribed'], month_scores['frozen_score']),
            'top_30_subscription_rate': report['performance']['top_30_subscription_rate'],
            'mean_score': report['calibration']['mean_score'],
            'mean_calibrated_score': report['calibration']['mean_calibrated_score'],
            'score_psi': report['drift']['score'],
            'next_recipe': report['retraining']['recipe_in_use'],
            'alerts': len(report['alerts']),
        })
    summary = pd.DataFrame(rows)
    storage.write_csv(storage.join(output_dir, 'monitoring.csv'), summary)
    return summary


def plot(summary, path):
    """Saves the monitoring chart: ranking quality, calibration and drift by month."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    blue, orange, gray, ink, ink_2, grid, surface = ('#2a78d6', '#eb6834', '#8a8985', '#0b0b0b', '#52514e',
                                                     '#e4e3df', '#fcfcfb')
    plt.rcParams.update({
        'figure.facecolor': surface, 'axes.facecolor': surface, 'savefig.facecolor': surface,
        'axes.edgecolor': grid, 'axes.labelcolor': ink_2, 'axes.titlecolor': ink,
        'axes.titlesize': 12, 'axes.titleweight': 'bold', 'axes.titlelocation': 'left',
        'axes.spines.top': False, 'axes.spines.right': False,
        'axes.grid': True, 'grid.color': grid, 'grid.linewidth': 0.8, 'axes.axisbelow': True,
        'xtick.color': ink_2, 'ytick.color': ink_2, 'font.size': 10, 'legend.frameon': False,
        'lines.linewidth': 2,
    })
    months = pd.PeriodIndex(summary['month'], freq='M').strftime('%b')
    percent = plt.FuncFormatter(lambda v, _: f'{v:.0%}')

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4.5))
    ax1.plot(months, summary['roc_auc'], color=blue, marker='o', label='Retrained every month')
    ax1.plot(months, summary['frozen_model_roc_auc'], color=gray, linestyle='--', marker='o',
             label='Frozen at the end of 2009')
    ax1.axhline(0.5, color=grid, linewidth=1.5)
    ax1.set_ylim(0.4, 0.9)
    ax1.set_title('ROC AUC by month')
    ax1.legend(loc='lower left')

    ax2.plot(months, summary['subscription_rate'], color=ink, marker='o', label='Observed subscription rate')
    ax2.plot(months, summary['mean_calibrated_score'], color=blue, marker='o', label='Mean calibrated score')
    ax2.plot(months, summary['mean_score'], color=orange, marker='o', label='Mean raw score')
    ax2.set_ylim(0, 1)
    ax2.yaxis.set_major_formatter(percent)
    ax2.set_title('Calibration: scores vs outcomes')
    ax2.legend(loc='lower right')

    ax3.bar(months, summary['score_psi'], color=blue, width=0.6)
    ax3.axhline(0.25, color=orange, linestyle='--', linewidth=1.5, label='Alert threshold (0.25)')
    ax3.set_title('Score drift vs training data (PSI)')
    ax3.grid(axis='x', visible=False)
    ax3.legend(loc='upper right')

    fig.suptitle('Simulated production in 2010: monthly scoring, monitoring and retraining',
                 x=0.01, ha='left', color=ink_2, fontsize=10)
    plt.tight_layout()
    with storage.open_file(path, 'wb') as file:
        fig.savefig(file, format='png', dpi=100)
    plt.close(fig)
