class StepCreator(object):
    def __init__(self, step_classes=None):
        self._classes = {}
        if step_classes is not None:
            for step_class in step_classes:
                self.add_step_class(step_class)

    def add_step_class(self, step_class):
        self._classes[step_class.type] = step_class

    def create(self, step_type, arguments):
        step_class = self._classes[step_type]
        return step_class(arguments)
