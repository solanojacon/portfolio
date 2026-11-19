"""File access for the pipeline.

Paths can be local, or cloud URLs such as `s3://bucket/key` once the matching fsspec backend
(for example s3fs) is installed. Nothing else in the pipeline touches files directly.
"""

import json

import fsspec
import joblib
import pandas as pd


def join(*parts):
    return '/'.join(str(part).rstrip('/') for part in parts)


def exists(path):
    fs, local_path = fsspec.core.url_to_fs(path)
    return fs.exists(local_path)


def open_file(path, mode):
    if 'w' in mode:
        fs, local_path = fsspec.core.url_to_fs(path)
        fs.makedirs(fs._parent(local_path), exist_ok=True)
    return fsspec.open(path, mode)


def read_csv(path, **kwargs):
    with open_file(path, 'rb') as file:
        return pd.read_csv(file, **kwargs)


def write_csv(path, frame):
    with open_file(path, 'w') as file:
        frame.to_csv(file, index=False)


def read_json(path):
    with open_file(path, 'r') as file:
        return json.load(file)


def write_json(path, data):
    with open_file(path, 'w') as file:
        json.dump(data, file, indent=2)


def read_model(path):
    with open_file(path, 'rb') as file:
        return joblib.load(file)


def write_model(path, model):
    with open_file(path, 'wb') as file:
        joblib.dump(model, file)
