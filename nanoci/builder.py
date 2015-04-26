import os
import traceback

from datetime import datetime
from subprocess import CalledProcessError

from nanoci import git

from nanoci.fileutils import mkdir_p, read_path
from nanoci.subproclog import log_check_call


STATUS_NEW = 'NEW'
STATUS_SUCCESS = 'SUCCESS'
STATUS_FAILURE = 'FAILURE'

class Builder(object):
    BUILD_LOG_NAME = 'build.log'

    def __init__(self, config, project, commit_id):
        self.project = project
        self.commit_id = commit_id
        self.status = STATUS_NEW

        self.src_dir = Builder.get_src_base_dir(config, project['name'])
        log_base_dir = Builder.get_log_base_dir(config, project['name'])
        mkdir_p(log_base_dir)
        self.build_id = 1
        while True:
            self.log_dir = os.path.join(log_base_dir, str(self.build_id))
            try:
                os.mkdir(self.log_dir)
                break
            except OSError:
                self.build_id += 1

        self.log_fp = None

    @staticmethod
    def get_log_base_dir(config, project_name):
        return os.path.join(config.work_base_dir, project_name, 'log')

    @staticmethod
    def get_src_base_dir(config, project_name):
        return os.path.join(config.work_base_dir, project_name, 'src')

    def log(self, message):
        # We do not use the logging module because we want to have one single
        # log file containing our messages and the output of the build steps
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.log_fp.write('# ' + timestamp + ': ' + message + '\n')
        self.log_fp.flush()

    def check_source(self):
        self.log('Running step "git"')
        source_url = read_path(self.project['source']['url'])
        if not os.path.isdir(self.src_dir):
            git.clone(self.log_fp, source_url, self.src_dir)
        git.update(self.log_fp, self.src_dir, self.commit_id)
        self.log_fp.flush()

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
            self.log('Running step "{}"'.format(name))
            script = step['script']
            try:
                self.log_fp.write('## Script\n{}\n## Output\n'.format(script.strip()))
                self.log_fp.flush()
                log_check_call(self.log_fp, script, shell=True, env=env, cwd=self.src_dir)
            except CalledProcessError as exc:
                self.log('Command failed with exit code {}'.format(exc.returncode))
                return False
        return True

    def build(self):
        log_file_path = os.path.join(self.log_dir, Builder.BUILD_LOG_NAME)
        with open(log_file_path, 'w') as self.log_fp:
            self.log('Starting build #{}'.format(self.build_id))
            try:
                self.check_source()
                ok = self.run_steps('build')
                self.status = STATUS_SUCCESS if ok else STATUS_FAILURE
            except Exception as exc:
                trace = traceback.format_exc()
                self.log('Build failed with an exception:\n{}'.format(trace))
                self.status = STATUS_FAILURE
            finally:
                self.log('Build #{} finished: {}'.format(self.build_id, self.status))
                self.run_steps('notify')
