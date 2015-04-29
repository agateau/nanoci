from nanoci.fileutils import read_yaml_dict


class ProjectError(Exception):
    pass


def _load_steps(dct, category, step_creator):
    in_lst = dct.get(category)
    if in_lst is None:
        return []

    out_lst = []
    for idx, dct in enumerate(in_lst):
        arguments = dict(dct)
        try:
            step_type = arguments.pop('type')
        except KeyError:
            step_type = 'shell'
        try:
            step = step_creator.create(step_type, arguments)
        except KeyError:
            raise ProjectError('{}-{}: Unknown step type "{}"'
                               .format(category, idx + 1, step_type))
        out_lst.append(step)
    return out_lst


class Project(object):
    def __init__(self, name, path_or_dict, step_creator):
        self._name = name
        if isinstance(path_or_dict, dict):
            dct = path_or_dict
        else:
            dct = read_yaml_dict(path_or_dict)

        self._build_steps = _load_steps(dct, 'build', step_creator)
        self._notify_steps = _load_steps(dct, 'notify', step_creator)

    @property
    def name(self):
        return self._name

    @property
    def build_steps(self):
        return self._build_steps

    @property
    def notify_steps(self):
        return self._notify_steps
