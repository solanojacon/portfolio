"""Where the pipeline reads its data and writes its outputs. Environment variables override the defaults."""

import os
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]                    # this project's folder in the repository
PROJECT_DATA = PROJECT.parents[1] / 'portfolio-data' / PROJECT.name   # next to the repository, outside it

DATA_PATH = os.environ.get('BANK_MARKETING_DATA', str(PROJECT_DATA / 'data' / 'bank-full.csv'))
OUTPUT_DIR = os.environ.get('BANK_MARKETING_OUTPUT', str(PROJECT_DATA / 'models' / 'pipeline'))
