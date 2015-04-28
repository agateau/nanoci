from nanoci.fileutils import read_yaml_dict


class ProjectError(Exception):
    pass


def _load_steps(dct, category):
    in_lst = dct.get(category)
    if in_lst is None:
        return []

    # FIXME: get available step_classes from somewhere else
    from nanoci.gitstep import GitStep
    from nanoci.shellstep import ShellStep
    step_classes = {}
    def add_step_class(klass):
        step_classes[klass.type] = klass
    add_step_class(ShellStep)
    add_step_class(GitStep)

    out_lst = []
    for idx, dct in enumerate(in_lst):
        ttype = dct.get('type', 'shell')
        try:
            step_class = step_classes[ttype]
        except KeyError:
            raise ProjectError('{}-{}: Unknown step type "{}"'
                               .format(category, idx + 1, ttype))
        arguments = dct
        step = step_class(arguments)
        out_lst.append(step)
    return out_lst


class Project(object):
    def __init__(self, name, path_or_dict):
        self._name = name
        if isinstance(path_or_dict, dict):
            dct = path_or_dict
        else:
            dct = read_yaml_dict(path_or_dict)

        self._build_steps = _load_steps(dct, 'build')
        self._notify_steps = _load_steps(dct, 'notify')

    @property
    def name(self):
        return self._name

    @property
    def build_steps(self):
        return self._build_steps

    @property
    def notify_steps(self):
        return self._notify_steps
