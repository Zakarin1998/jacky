import os
import json

DATA_FILE = os.path.expanduser('~/.finance_tracker.json')


class JSONStorage:
    def __init__(self, path=DATA_FILE):
        self.path = path
        if not os.path.exists(self.path):
            self._init_db()

    def _init_db(self):
        default = {'profile': {}, 'incomes': [], 'expenses': []}
        with open(self.path, 'w') as f:
            json.dump(default, f, indent=4)

    def load(self):
        with open(self.path) as f:
            return json.load(f)

    def save(self, data: dict):
        with open(self.path, 'w') as f:
            json.dump(data, f, indent=4)
