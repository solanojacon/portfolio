"""Command line: `bank-marketing train | run-month | simulate`. Run `bank-marketing --help` for the options."""

import argparse

from bank_marketing import config, storage
from bank_marketing.data import read_calls


def main(argv=None):
    parser = argparse.ArgumentParser(prog='bank-marketing', description=__doc__)
    parser.add_argument('--data', default=config.DATA_PATH,
                        help='bank-full.csv (default: %(default)s, or $BANK_MARKETING_DATA)')
    parser.add_argument('--output', default=config.OUTPUT_DIR,
                        help='folder for models, scores and reports (default: %(default)s, or $BANK_MARKETING_OUTPUT)')
    commands = parser.add_subparsers(dest='command', required=True)
    train = commands.add_parser('train', help='train the first champion on the calls before a month')
    train.add_argument('--before', default='2010-01', help='first month not used for training (default: %(default)s)')
    run = commands.add_parser('run-month', help='run the monthly job at the start of a month')
    run.add_argument('month', help='for example 2010-02')
    simulate = commands.add_parser('simulate', help='replay the monthly job from a month until the data ends')
    simulate.add_argument('--start', default='2010-01', help='first month in production (default: %(default)s)')
    simulate.add_argument('--chart', help='where to save the monitoring chart (default: OUTPUT/monitoring.png)')
    args = parser.parse_args(argv)

    calls = read_calls(args.data)
    if args.command in ('train', 'simulate') and storage.exists(storage.join(args.output, 'registry')):
        parser.error(f'{args.output} already has a model registry: remove it or choose another --output')

    if args.command == 'train':
        from bank_marketing.job import train_first_model
        print(f'Champion: {train_first_model(calls, args.output, args.before)}')
    elif args.command == 'run-month':
        from bank_marketing.job import run_month
        report = run_month(calls, args.output, args.month)
        if report:
            print(f'{report["month"]}: ROC AUC {report["performance"]["roc_auc"]:.3f}, '
                  f'recipe in use: {report["retraining"]["recipe_in_use"]}, alerts: {report["alerts"] or "none"}')
    else:
        from bank_marketing.simulation import plot, simulate
        summary = simulate(calls, args.output, args.start)
        plot(summary, args.chart or storage.join(args.output, 'monitoring.png'))
        print(summary.round(3).to_string(index=False))
        print(f'\nMean monthly ROC AUC: {summary["roc_auc"].mean():.3f} retrained every month, '
              f'{summary["frozen_model_roc_auc"].mean():.3f} frozen at the start')


if __name__ == '__main__':
    main()
