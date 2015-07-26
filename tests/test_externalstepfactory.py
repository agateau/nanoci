import os

from io import StringIO

from nanoci.externalstepfactory import ExternalStep, find_step_executables


def create_executable(dirname, filename, content=None):
    path = os.path.join(dirname, filename)
    with open(path, 'w') as f:
        f.write(content or '')
    os.chmod(path, 0o755)
    return path


def test_find_executables(tmpdir):
    tmpdir = str(tmpdir)

    dirname1 = os.path.join(tmpdir, 'dir1')
    os.mkdir(dirname1)
    exe1 = create_executable(dirname1, 'exe1')
    exe2 = create_executable(dirname1, '_nanoci-step-foo')

    dirname2 = os.path.join(tmpdir, 'dir2')
    os.mkdir(dirname2)
    exe3 = create_executable(dirname2, '_nanoci-step-bar')
    exe4 = create_executable(dirname2, 'exe4')

    env = dict(PATH=dirname1 + ':' + dirname2)

    result = list(find_step_executables(environ=env))

    assert result == [exe2, exe3]


def test_find_executables_skip_non_existent_dirs(tmpdir):
    tmpdir = str(tmpdir)
    env = dict(PATH=os.path.join(tmpdir, '/does/not/exist'))
    result = list(find_step_executables(environ=env))
    assert result == []


def test_run_in_src_dir(tmpdir):
    tmpdir = str(tmpdir)
    bin_dir = os.path.join(tmpdir, 'bin')
    os.mkdir(bin_dir)

    create_executable(bin_dir, '_nanoci-step-echo-pwd', \
        content='#!/bin/sh\necho $PWD')

    src_dir = os.path.join(tmpdir, 'src')
    os.mkdir(src_dir)

    env = dict(SRC_DIR=src_dir, PATH=bin_dir + ':/usr/bin:/bin')

    step = ExternalStep(step_type='test', executable='_nanoci-step-echo-pwd', arguments={})

    out_log = os.path.join(tmpdir, 'out.log')
    with open(out_log, 'wt') as fp:
        step.run(fp, env=env)
    output = open(out_log).read()
    assert output.strip() == src_dir
