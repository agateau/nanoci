class StepCreator(object):
    def __init__(self, factories=None):
        self._factories = {}
        if factories is not None:
            for factory in factories:
                self.add_factory(factory)

    def add_factory(self, factory):
        self._factories[factory.step_type] = factory

    def create(self, step_type, arguments):
        factory = self._factories[step_type]
        return factory(arguments)
