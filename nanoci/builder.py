import os
import traceback

from datetime import datetime

from nanoci.fileutils import mkdir_p


STATUS_NEW = 'NEW'
STATUS_SUCCESS = 'SUCCESS'
STATUS_FAILURE = 'FAILURE'

class Builder(object):
    BUILD_LOG_NAME = 'build.log'

    def __init__(self, config, project, commit_id):
        self.project = project
        self.commit_id = commit_id
        self.status = STATUS_NEW

        self.src_dir = Builder.get_src_base_dir(config, project.name)
        log_base_dir = Builder.get_log_base_dir(config, project.name)
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

    def run_steps(self, category, steps):
        """
        Run steps, returns True on success, False on failure
        """
        if not steps:
            return True
        env = dict(os.environ)
        env.update({
            'SRC_DIR': self.src_dir,
            'PROJECT_NAME': self.project.name,
            'COMMIT_ID': self.commit_id,
            'SHORT_COMMIT_ID': self.commit_id[:8],
            'BUILD_ID': str(self.build_id),
            'BUILD_STATUS': self.status,
        })
        for idx, step in enumerate(steps):
            self.log('Running step {}-{}: {}'.format(category, idx + 1, step))
            if not step.run(self.log_fp, env=env):
                return False
        return True

    def build(self):
        log_file_path = os.path.join(self.log_dir, Builder.BUILD_LOG_NAME)
        with open(log_file_path, 'w') as self.log_fp:
            self.log('Starting build #{}'.format(self.build_id))
            try:
                ok = self.run_steps('build', self.project.build_steps)
                self.status = STATUS_SUCCESS if ok else STATUS_FAILURE
            except Exception as exc:
                trace = traceback.format_exc()
                self.log('Build failed with an exception:\n{}'.format(trace))
                self.status = STATUS_FAILURE
            finally:
                self.log('Build #{} finished: {}'.format(self.build_id, self.status))
                self.run_steps('notify', self.project.notify_steps)
