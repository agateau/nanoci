import os

from nanoci import projects
from nanoci.builder import Builder
from nanoci.config import Config
from nanoci.process_queue import ProcessQueue


class App(object):
    def __init__(self, config_dir):
        self._config_dir = config_dir
        self._config = None
        self._projects = None
        self._queue = ProcessQueue(self._build)

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

    @property
    def queue(self):
        return self._queue

    def _build(self, name, commit_id):
        project = self.projects[name]
        builder = Builder(self._config, project, commit_id)
        builder.build()
