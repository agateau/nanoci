import yaml

from fileutils import mkdir_p, read_path


class Config(object):
    def __init__(self, path_or_dict):
        if isinstance(path_or_dict, str):
            with open(path_or_dict) as f:
                dct = yaml.load(f)
        else:
            dct = path_or_dict

        self.workspace_base_dir = read_path(dct['workspace_base_dir'])
        self.log_base_dir = read_path(dct.get('log_base_dir', '~/.cache/nanoci/log'))

        mkdir_p(self.workspace_base_dir)
        mkdir_p(self.log_base_dir)
