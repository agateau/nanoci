import os

from nanoci.subproclog import log_check_call


def test_log_stdout_and_stderr(tmpdir):
    tmpdir = str(tmpdir)
    path = os.path.join(tmpdir, 'out')
    with open(path, 'wb') as fp:
        log_check_call(fp, 'echo OUT ; echo ERR 1>&2', shell=True)

    with open(path, 'rb') as fp:
        content = fp.read()
    assert content == b'OUT\nERR\n'
