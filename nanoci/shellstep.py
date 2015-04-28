from subprocess import CalledProcessError

from nanoci.step import Step
from nanoci.subproclog import log_check_call


class ShellStep(Step):
    type = 'shell'

    def run(self, log_fp, env):
        script = self._arguments['script']
        cwd = env['SRC_DIR']
        try:
            log_fp.write('## Script\n{}\n## Output\n'.format(script.strip()))
            log_fp.flush()
            log_check_call(log_fp, script, shell=True, env=env, cwd=cwd)
            return True
        except CalledProcessError as exc:
            log_fp.write('Command failed with exit code {}'.format(exc.returncode))
            log_fp.flush()
            return False
