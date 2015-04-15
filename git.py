import logging

from subprocess import check_call

def clone(source_url, dst):
    logging.info('Cloning %s', source_url)
    check_call(['git', 'clone', source_url, dst])

def update(worktree_dir, commit_id):
    logging.info('Updating %s to %s', worktree_dir, commit_id)
    check_call(['git', 'fetch'], cwd=worktree_dir)
    check_call(['git', 'checkout', commit_id], cwd=worktree_dir)
