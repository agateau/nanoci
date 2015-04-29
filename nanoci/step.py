class Step(object):
    """A step in a project. This is an abstract class. Classes inheriting from
    this class must set `type` and implement `run`."""
    type = 'set-me'

    def __init__(self, arguments):
        self._arguments = arguments

    def run(self, log_fp, env):
        """Runs a step, returns True on success, False on failure."""
        raise NotImplementedError()
