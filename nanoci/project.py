from nanoci.fileutils import read_yaml_dict


class Project(object):
    def __init__(self, name, path_or_dict):
        self._name = name
        if isinstance(path_or_dict, dict):
            self._dct = path_or_dict
        else:
            self._dct = read_yaml_dict(path_or_dict)

        self._build_steps = self._dct.get('build', [])
        self._notify_steps = self._dct.get('notify', [])

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
