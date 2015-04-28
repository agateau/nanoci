import os

import yaml


def mkdir_p(dirname):
    if not os.path.isdir(dirname):
        os.makedirs(dirname)


def read_path(txt):
    return os.path.expanduser(txt)


def read_yaml_dict(file_path, default=None):
    """Reads `file_path` as a dict if it exists. If it does not, returns an
    empty dict or `default` if it is set.
    """
    if not os.path.exists(file_path):
        if default is None:
            return {}
        else:
            return default

    with open(file_path) as fp:
        return yaml.load(fp)
