import os

import yaml


_projects = {}


def get_all():
    return _projects


def load_all(dir_name):
    for name in os.listdir(dir_name):
        project_name, ext = os.path.splitext(name)
        if ext != '.yaml':
            continue
        path = os.path.join(dir_name, name)
        with open(path) as f:
            dct = yaml.load(f)
            dct['name'] = project_name
            _projects[project_name] = dct
