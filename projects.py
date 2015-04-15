import os

import yaml

from builder import Builder
from config import Config


_projects = {}
_config = None


def init(config_file):
    global _config
    _config = Config(config_file)


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


def build(project_name, commit_id):
    project = _projects[project_name]
    builder = Builder(_config, project, commit_id)
    builder.build()
