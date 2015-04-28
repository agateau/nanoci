from nanoci.fileutils import read_yaml_dict
from nanoci.step import Step


class ProjectError(Exception):
    pass


def _load_steps(dct, step_type):
    in_lst = dct.get(step_type)
    if in_lst is None:
        return []

    # FIXME: get available commands from somewhere else
    from nanoci.shellcommand import ShellCommand
    commands = {}
    def add_command(klass):
        commands[klass.name] = klass()
    add_command(ShellCommand)

    out_lst = []
    for idx, dct in enumerate(in_lst):
        name = dct.get('command', 'shell')
        try:
            command = commands[name]
        except KeyError:
            raise ProjectError('{}-{}: Unknown command "{}"'
                               .format(step_type, idx + 1, name))
        arguments = dct
        step = Step(command, arguments)
        out_lst.append(step)
    return out_lst


class Project(object):
    def __init__(self, name, path_or_dict):
        self._name = name
        if isinstance(path_or_dict, dict):
            self._dct = path_or_dict
        else:
            self._dct = read_yaml_dict(path_or_dict)

        self._build_steps = _load_steps(self._dct, 'build')
        self._notify_steps = _load_steps(self._dct, 'notify')

    @property
    def name(self):
        return self._name

    @property
    def build_steps(self):
        return self._build_steps

    @property
    def notify_steps(self):
        return self._notify_steps

    def __getitem__(self, name):
        return self._dct[name]

    def get(self, name, default=None):
        return self._dct.get(name, default)
