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
        return self._config.has_project(name)

    def get_project(self, name):
        return self._config.get_project(name)
