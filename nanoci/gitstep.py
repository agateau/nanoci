import os

from nanoci.fileutils import read_path
from nanoci.step import Step
from nanoci.subproclog import log_check_call


class GitStep(Step):
    """A step to checkout or update a git repository.
    """
    type = 'git'

    def run(self, log_fp, env):
        url = read_path(self._arguments['url'])
        src_dir = env['SRC_DIR']

        if os.path.isdir(src_dir):
            log_check_call(log_fp, ['git', 'fetch'], cwd=src_dir)
        else:
            log_check_call(log_fp, ['git', 'clone', url, src_dir])

        log_check_call(log_fp, ['git', 'checkout', env['COMMIT_ID']], cwd=src_dir)

        log_fp.flush()
        return True
