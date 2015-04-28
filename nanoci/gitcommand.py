import os

from nanoci import git
from nanoci.command import Command
from nanoci.fileutils import read_path


class GitCommand(Command):
    """A command to checkout or update a git repository.
    """
    name = 'git'

    def run(self, arguments, log_fp, env):
        url = read_path(arguments['url'])
        src_dir = env['SRC_DIR']
        if not os.path.isdir(src_dir):
            git.clone(log_fp, url, src_dir)
        git.update(log_fp, src_dir, env['COMMIT_ID'])
        log_fp.flush()
        return True
