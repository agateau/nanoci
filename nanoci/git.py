from nanoci.subproclog import log_check_call


def clone(fp, source_url, dst):
    log_check_call(fp, ['git', 'clone', source_url, dst])


def update(fp, worktree_dir, commit_id):
    log_check_call(fp, ['git', 'fetch'], cwd=worktree_dir)
    log_check_call(fp, ['git', 'checkout', commit_id], cwd=worktree_dir)
