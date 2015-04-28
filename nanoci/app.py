import os

import yaml

from nanoci.config import Config


class App(object):
    def __init__(self, config_dir='~/.config/nanoci'):
        self._config = Config(config_dir)
        self._projects = None

    @property
    def config(self):
        return self._config

    def has_project(self, name):
        return os.path.exists(self._get_project_path(name))

    def get_project(self, name):
        """Load a project by name, returns a dictionary of its definition.
        Each call re-reads the project from its file so the returned definition
        is always up to date.
        """
        project_path = self._get_project_path(name)
        with open(project_path) as f:
            dct = yaml.load(f)
            dct['name'] = name
            return dct

    def _get_project_path(self, name):
        return os.path.join(self._config.config_dir, 'projects', name + '.yaml')
