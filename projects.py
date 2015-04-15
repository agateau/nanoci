import logging
import os
from subprocess import check_output, STDOUT, CalledProcessError

import yaml

import git


_projects = {}

class Config(object):
    pass
_config = Config()


STATUS_NEW = 'NEW'
STATUS_SUCCESS = 'SUCCESS'
STATUS_FAILURE = 'FAILURE'


class Builder(object):
    def __init__(self, project, workspace_dir, commit_id):
        self.project = project
        self.workspace_dir = workspace_dir
        self.commit_id = commit_id
        self.status = STATUS_NEW

    def check_source(self):
        source_url = self.project['source']['url']
        if not os.path.isdir(self.workspace_dir):
            git.clone(source_url, self.workspace_dir)
        git.update(self.workspace_dir, self.commit_id)

    def run_steps(self, steps):
        env = dict(os.environ)
        env.update({
            'WORKSPACE': self.workspace_dir,
            'PROJECT_NAME': self.project['name'],
            'COMMIT_ID': self.commit_id,
            'SHORT_COMMIT_ID': self.commit_id[:8],
            'BUILD_STATUS': self.status,
        })
        for step in steps:
            script = step['script']
            try:
                logging.info('Running %s', script)
                output = check_output(script, shell=True, stderr=STDOUT, env=env,
                                      cwd=self.workspace_dir)
                logging.info(output)
            except CalledProcessError as exc:
                output = exc.output.decode('utf-8')
                logging.error('Command failed with exit code %d. Output:\n%s',
                              exc.returncode, output)
                self.status = STATUS_FAILURE
                return


def _read_path(txt):
    return os.path.expanduser(txt)


def init(config_file):
    with open(config_file) as f:
        dct = yaml.load(f)
    _config.workspace_base_dir = _read_path(dct['workspace_base_dir'])
    if not os.path.isdir(_config.workspace_base_dir):
        os.makedirs(_config.workspace_base_dir)


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
    workspace_dir = os.path.join(_config.workspace_base_dir, project_name)

    builder = Builder(project, workspace_dir, commit_id)

    try:
        builder.check_source()
        builder.run_steps(project['build_steps'])
        builder.status = STATUS_SUCCESS
    except Exception as exc:
        logging.exception(exc)
        builder.status = STATUS_FAILURE
    finally:
        logging.info('Finished: %s', builder.status)
        builder.run_steps(project['notifiers'])
