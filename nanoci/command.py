class Command(object):
    """A command run by one or more steps. This is an abstract class."""

    name = 'set-me'

    def run(self, args, log_fp, env):
        """Runs the command. Must return True on success, False on failure."""
        raise NotImplementedError()
