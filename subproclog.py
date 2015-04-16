from subprocess import check_call, STDOUT


def log_check_call(fp, command, shell=False, env=None, cwd=None):
    return check_call(command, shell=shell, env=env, cwd=cwd,
                      stderr=STDOUT, stdout=fp)
