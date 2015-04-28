import os

from nanoci import git
from nanoci.step import Step
from nanoci.fileutils import read_path


class GitStep(Step):
    """A step to checkout or update a git repository.
    """
    type = 'git'

    def run(self, log_fp, env):
        url = read_path(self._arguments['url'])
        src_dir = env['SRC_DIR']
        if not os.path.isdir(src_dir):
            git.clone(log_fp, url, src_dir)
        git.update(log_fp, src_dir, env['COMMIT_ID'])
        log_fp.flush()
        return True
