import os

import yaml

from nanoci.fileutils import read_path


class Project(object):
    def __init__(self, name, path_or_dict):
        self._name = name
        if isinstance(path_or_dict, dict):
            self._dct = path_or_dict
        else:
            path = read_path(path_or_dict)
            if os.path.exists(path):
                with open(path) as fp:
                    self._dct = yaml.load(fp)
            else:
                self._dct = {}

    @property
    def name(self):
        return self._name

    def __getitem__(self, name):
        return self._dct[name]

    def get(self, name, default=None):
        return self._dct.get(name, default)
