class StepMixin(object):
    """
    This mixin provides a default implementation of some features a step must
    provide.
    """
    def __init__(self, arguments):
        self._arguments = arguments

    def __str__(self):
        return '{}({})'.format(self.step_type, self._arguments)
