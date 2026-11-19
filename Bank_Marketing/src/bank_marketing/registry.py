"""Model versions, saved as plain files.

    registry/v001.joblib   the fitted pipeline
    registry/v001.json     its metadata: training data, validation result, reference distributions
    registry/champion.json the version in use
"""

from bank_marketing import storage


class Registry:
    def __init__(self, output_dir):
        self.root = storage.join(output_dir, 'registry')

    def _path(self, name):
        return storage.join(self.root, name)

    def champion_version(self):
        path = self._path('champion.json')
        return storage.read_json(path)['version'] if storage.exists(path) else None

    def load(self, version):
        return storage.read_model(self._path(f'{version}.joblib')), storage.read_json(self._path(f'{version}.json'))

    def champion(self):
        return self.load(self.champion_version())

    def promote(self, model, metadata):
        """Saves a new version and makes it the champion."""
        current = self.champion_version()
        version = f'v{int(current[1:]) + 1 if current else 1:03d}'
        storage.write_model(self._path(f'{version}.joblib'), model)
        storage.write_json(self._path(f'{version}.json'), {'version': version, **metadata})
        storage.write_json(self._path('champion.json'), {'version': version})
        return version
