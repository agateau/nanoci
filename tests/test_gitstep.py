import os
import subprocess
import sys

from nanoci.fileutils import mkdir_p
from nanoci.gitstep import GitStep


def create_file(dirname, filename, content=''):
    mkdir_p(dirname)
    file_path = os.path.join(dirname, filename)
    with open(file_path, 'w') as fp:
        fp.write(content)
    return file_path


def create_repo(tmpdir, name):
    repo_url = os.path.join(tmpdir, name)

    mkdir_p(repo_url)
    subprocess.check_call(['git', 'init'], cwd=repo_url)
    create_file(repo_url, 'README')
    subprocess.check_call(['git', 'add', '.'], cwd=repo_url)
    subprocess.check_call(['git', 'commit', '-m', 'Import'], cwd=repo_url)
    return repo_url


def run_step(step, src_dir, commit_id='origin/HEAD'):
    env = dict(SRC_DIR=src_dir, COMMIT_ID=commit_id)
    return step.run(sys.stderr, env=env)


def test_clone(tmpdir):
    tmpdir = str(tmpdir)
    src_dir = os.path.join(tmpdir, 'foo')
    repo_url = create_repo(tmpdir, 'foo.git')

    step = GitStep(dict(url=repo_url))
    ok = run_step(step, src_dir)
    assert ok
    assert os.path.exists(os.path.join(src_dir, 'README'))


def test_clone_fail(tmpdir):
    tmpdir = str(tmpdir)
    src_dir = os.path.join(tmpdir, 'foo')

    step = GitStep(dict(url='/does/not/exist'))
    ok = run_step(step, src_dir)
    assert not ok


def test_update(tmpdir):
    tmpdir = str(tmpdir)
    src_dir = os.path.join(tmpdir, 'foo')
    repo_url = create_repo(tmpdir, 'foo.git')

    # Initial clone
    step = GitStep(dict(url=repo_url))
    ok = run_step(step, src_dir)
    assert ok
    assert os.path.exists(os.path.join(src_dir, 'README'))

    # Create a new file
    file_path = create_file(repo_url, 'test.py')
    subprocess.check_call(['git', 'add', file_path], cwd=repo_url)
    subprocess.check_call(['git', 'commit', '-m', 'add test.py'], cwd=repo_url)

    # Update our copy
    step = GitStep(dict(url=repo_url))
    ok = run_step(step, src_dir)
    assert ok
    assert os.path.exists(os.path.join(src_dir, 'test.py'))

    # Go back to previous commit
    step = GitStep(dict(url=repo_url))
    ok = run_step(step, src_dir, commit_id='HEAD^1')
    assert ok
    assert not os.path.exists(os.path.join(src_dir, 'test.py'))
