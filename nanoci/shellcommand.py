from subprocess import CalledProcessError

from nanoci.command import Command
from nanoci.subproclog import log_check_call


class ShellCommand(Command):
    name = 'shell'

    def run(self, arguments, log_fp, env):
        script = arguments['script']
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
