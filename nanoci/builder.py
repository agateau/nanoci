import logging
import os

from subprocess import CalledProcessError

from nanoci import git

from nanoci.fileutils import mkdir_p, read_path
from nanoci.subproclog import log_check_call


STATUS_NEW = 'NEW'
STATUS_SUCCESS = 'SUCCESS'
STATUS_FAILURE = 'FAILURE'

class Builder(object):
    def __init__(self, config, project, commit_id):
        self.project = project
        self.commit_id = commit_id
        self.status = STATUS_NEW

        self.work_dir = os.path.join(config.work_base_dir, project['name'])
        self.src_dir = os.path.join(self.work_dir, 'src')

        log_base_dir = os.path.join(self.work_dir, 'log')
        mkdir_p(log_base_dir)
        self.build_id = 1
        while True:
            self.log_dir = os.path.join(log_base_dir, str(self.build_id))
            try:
                os.mkdir(self.log_dir)
                break
            except OSError:
                self.build_id += 1

        log_file_path = os.path.join(self.log_dir, 'main.log')
        self.log = logging.getLogger('build-{}-{}'.format(project['name'], self.build_id))
        self.log.setLevel(logging.DEBUG)
        self.log.addHandler(logging.FileHandler(log_file_path))

    def check_source(self):
        self.log.info('Running step "git"')
        source_url = read_path(self.project['source']['url'])
        log_file_path = os.path.join(self.log_dir, 'step-git.log')
        with open(log_file_path, 'w') as fp:
            if not os.path.isdir(self.src_dir):
                git.clone(fp, source_url, self.src_dir)
            git.update(fp, self.src_dir, self.commit_id)

    def run_steps(self, step_type):
        """
        Run steps, returns True on success, False on failure
        """
        steps = self.project.get(step_type)
        if not steps:
            return True
        env = dict(os.environ)
        env.update({
            'SRC_DIR': self.src_dir,
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
                with open(log_file_path, 'w') as fp:
                    log_check_call(fp, script, shell=True, env=env, cwd=self.src_dir)
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
