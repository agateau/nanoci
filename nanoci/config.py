import os
import yaml

from nanoci.fileutils import mkdir_p, read_path
from nanoci.project import Project


class Config(object):
    def __init__(self, config_dir='~/.config/nanoci'):
        self._config_dir = read_path(config_dir)

        config_file = os.path.join(self._config_dir, 'nanoci.yaml')
        if os.path.exists(config_file):
            with open(config_file) as f:
                dct = yaml.load(f)
        else:
            dct = {}

        self._work_base_dir = read_path(dct.get('work_base_dir', '~/.cache/nanoci'))
        mkdir_p(self._work_base_dir)

        self._port = int(dct.get('port', '5000'))

    @property
    def server_url(self):
        return 'http://localhost:{}'.format(self._port)

    @property
    def config_dir(self):
        return self._config_dir

    @property
    def work_base_dir(self):
        return self._work_base_dir

    @property
    def port(self):
        return self._port

    def has_project(self, name):
        return os.path.exists(self._get_project_path(name))

    def get_project(self, name):
        """Load a project by name, returns a Project instance. Each call
        re-reads the project from its file so the returned object is always up
        to date.
        """
        project_path = self._get_project_path(name)
        return Project(name, project_path)

    def _get_project_path(self, name):
        return os.path.join(self._config_dir, 'projects', name + '.yaml')
