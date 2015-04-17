import os
import yaml

from nanoci.fileutils import mkdir_p, read_path


class Config(object):
    def __init__(self, path_or_dict):
        if isinstance(path_or_dict, str):
            if os.path.exists(path_or_dict):
                with open(path_or_dict) as f:
                    dct = yaml.load(f)
            else:
                dct = {}
        else:
            dct = path_or_dict

        self.work_base_dir = read_path(dct.get('work_base_dir', '~/.cache/nanoci'))
        mkdir_p(self.work_base_dir)
