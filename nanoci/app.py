import os

from nanoci import projects
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

    @property
    def projects(self):
        if self._projects == None:
            # FIXME: Refactor to turn projects into a class?
            projects.load_all(os.path.join(self._config_dir, 'projects'))
            self._projects = projects.get_all()
        return self._projects
