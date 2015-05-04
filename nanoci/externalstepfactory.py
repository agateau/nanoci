"""
This module makes it possible to register external executables as steps.

To be considered as a step, the executable name must start with EXECUTABLE_PREFIX.
"""
import os

from subprocess import CalledProcessError

from nanoci.stepmixin import StepMixin
from nanoci.subproclog import log_check_call


EXECUTABLE_PREFIX = '_nanoci-step-'


def find_step_executables(environ=None):
    if environ is None:
        environ = os.environ
    path_dirs = environ['PATH'].split(':')
    for path_dir in path_dirs:
        if not os.path.isdir(path_dir):
            continue
        for executable in os.listdir(path_dir):
            if executable.startswith(EXECUTABLE_PREFIX):
                yield os.path.join(path_dir, executable)


class ExternalStep(StepMixin):
    def __init__(self, step_type, executable, arguments):
        super(ExternalStep, self).__init__(arguments)
        self._step_type = step_type
        self._executable = executable

    @property
    def step_type(self):
        return self._step_type

    def run(self, log_fp, env):
        cwd = env['SRC_DIR']
        cmd_env = dict(env)
        for key, value in self._arguments.items():
            name = 'NARG_{}'.format(key.upper())
            cmd_env[name] = str(value)
        try:
            log_check_call(log_fp, [self._executable], env=cmd_env, cwd=cwd)
            return True
        except CalledProcessError as exc:
            log_fp.write('Command failed with exit code {}'.format(exc.returncode))
            log_fp.flush()
            return False


class ExternalStepFactory(object):
    def __init__(self, executable):
        self._executable = executable
        self._step_type = os.path.basename(self._executable)[len(EXECUTABLE_PREFIX):]

    @property
    def step_type(self):
        return self._step_type

    def __call__(self, arguments):
        return ExternalStep(self._step_type, self._executable, arguments)
