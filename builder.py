import logging
import os

from subprocess import check_call, STDOUT, CalledProcessError

import git


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

    def run_steps(self, step_type):
        """
        Run steps, returns True on success, False on failure
        """
        steps = self.project.get(step_type)
        if not steps:
            return True
        env = dict(os.environ)
        env.update({
            'WORKSPACE': self.workspace_dir,
            'PROJECT_NAME': self.project['name'],
            'COMMIT_ID': self.commit_id,
            'SHORT_COMMIT_ID': self.commit_id[:8],
            'BUILD_ID': str(self.build_id),
            'BUILD_STATUS': self.status,
        })
        for idx, step in enumerate(steps):
            name = step.get('name', '{}-{}'.format(step_type, idx + 1))
            self.log.info('Running step "%s"', name)
            script = step['script']
            try:
                log_file_path = os.path.join(self.log_dir, 'step-{}.log'.format(name))
                with open(log_file_path, 'w') as f:
                    check_call(script, shell=True, stderr=STDOUT, stdout=f,
                               env=env, cwd=self.workspace_dir)
            except CalledProcessError as exc:
                self.log.error('Command failed with exit code %d', exc.returncode)
                return False
        return True

    def build(self):
        self.log.info('Starting build #%d', self.build_id)
        try:
            self.check_source()
            ok = self.run_steps('build')
            self.status = STATUS_SUCCESS if ok else STATUS_FAILURE
        except Exception as exc:
            self.log.exception(exc)
            self.status = STATUS_FAILURE
        finally:
            self.log.info('Build #%d finished: %s', self.build_id, self.status)
            self.run_steps('notify')
