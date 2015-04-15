import yaml

from fileutils import mkdir_p, read_path


class Config(object):
    def __init__(self, config_file):
        with open(config_file) as f:
            dct = yaml.load(f)

        self.workspace_base_dir = read_path(dct['workspace_base_dir'])
        self.log_base_dir = read_path(dct.get('log_base_dir', '~/.cache/nanoci/log'))

        mkdir_p(self.workspace_base_dir)
        mkdir_p(self.log_base_dir)
