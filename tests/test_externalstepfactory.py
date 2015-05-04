import os

from nanoci.externalstepfactory import find_step_executables


def create_executable(dirname, filename):
    path = os.path.join(dirname, filename)
    with open(path, 'w') as f:
        f.write('')
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
