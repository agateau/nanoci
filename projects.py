import logging
import os
import shutil
from subprocess import check_call, STDOUT, CalledProcessError

import yaml

import git


def mkdir_p(dirname):
    if not os.path.isdir(dirname):
        os.makedirs(dirname)


def read_path(txt):
    return os.path.expanduser(txt)


class Config(object):
    def __init__(self, config_file):
        with open(config_file) as f:
            dct = yaml.load(f)

        self.workspace_base_dir = read_path(dct['workspace_base_dir'])
        self.log_base_dir = read_path(dct.get('log_base_dir', '~/.cache/nanoci/log'))

        mkdir_p(self.workspace_base_dir)
        mkdir_p(self.log_base_dir)


STATUS_NEW = 'NEW'
STATUS_SUCCESS = 'SUCCESS'
STATUS_FAILURE = 'FAILURE'


class Builder(object):
    def __init__(self, config, project, commit_id):
        self.project = project
        self.workspace_dir = os.path.join(config.workspace_base_dir, project['name'])
        self.commit_id = commit_id
        self.status = STATUS_NEW

        self.build_id = 1
        while True:
            self.log_dir = os.path.join(config.log_base_dir, str(self.build_id))
            try:
                os.mkdir(self.log_dir)
                break
            except OSError:
                self.build_id += 1

        log_file_path = os.path.join(self.log_dir, 'main.log')
        self.log = logging.getLogger('build-{}'.format(self.build_id))
        self.log.setLevel(logging.DEBUG)
        self.log.addHandler(logging.FileHandler(log_file_path))

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
            'BUILD_ID': str(self.build_id),
            'BUILD_STATUS': self.status,
        })
        for step in steps:
            name = step['name']
            self.log.info('Running step "%s"', name)
            script = step['script']
            try:
                log_file_path = os.path.join(self.log_dir, 'step-{}.log'.format(name))
                with open(log_file_path, 'w') as f:
                    check_call(script, shell=True, stderr=STDOUT, stdout=f,
                               env=env, cwd=self.workspace_dir)
            except CalledProcessError as exc:
                self.log.error('Command failed with exit code %d', exc.returncode)
                self.status = STATUS_FAILURE
                return

    def build(self):
        self.log.info('Starting build #%d', self.build_id)
        try:
            self.check_source()
            self.run_steps(self.project['build_steps'])
            self.status = STATUS_SUCCESS
        except Exception as exc:
            self.log.exception(exc)
            self.status = STATUS_FAILURE
        finally:
            self.log.info('Build #%d finished: %s', self.build_id, self.status)
            self.run_steps(self.project['notifiers'])


_projects = {}
_config = None


def init(config_file):
    global _config
    _config = Config(config_file)


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
