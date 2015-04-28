import os

from nanoci.fileutils import mkdir_p, read_path, read_yaml_dict


class Config(object):
    def __init__(self, config_dir='~/.config/nanoci'):
        self._config_dir = read_path(config_dir)

        config_file = os.path.join(self._config_dir, 'nanoci.yaml')
        dct = read_yaml_dict(config_file)

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
        return os.path.exists(self.get_project_path(name))

    def get_project_path(self, name):
        return os.path.join(self._config_dir, 'projects', name + '.yaml')
