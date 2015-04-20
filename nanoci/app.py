import os

import yaml

from nanoci.config import Config

from nanoci.fileutils import read_path


class App(object):
    def __init__(self, config_dir='~/.config/nanoci'):
        self._config_dir = read_path(config_dir)
        self._config = None
        self._projects = None

    @property
    def config(self):
        if self._config == None:
            self._config = Config(os.path.join(self._config_dir, 'nanoci.yaml'))
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
        return os.path.join(self._config_dir, 'projects', name + '.yaml')
