class Step(object):
    """A step in a project. It groups a command and its arguments."""
    def __init__(self, command, arguments):
        self._command = command
        self._arguments = arguments

    def run(self, log_fp, env):
        """Runs a step, returns True on success, False on failure."""
        return self._command.run(self._arguments, log_fp, env)
