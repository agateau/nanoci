import os


def mkdir_p(dirname):
    if not os.path.isdir(dirname):
        os.makedirs(dirname)


def read_path(txt):
    return os.path.expanduser(txt)
