import os

import yaml

from nanoci.config import Config

from nanoci.fileutils import mkdir_p


def create_project(tmpdir, name, dct):
    project_path = os.path.join(tmpdir, 'projects', name + '.yaml')
    mkdir_p(os.path.dirname(project_path))
    with open(project_path, 'wt') as fp:
        yaml.dump(dct, fp)


def test_projects(tmpdir):
    tmpdir = str(tmpdir)
    config = Config(config_dir=tmpdir)
    create_project(tmpdir, 'foo', dict(a=1))
    create_project(tmpdir, 'bar', dict())

    assert config.has_project('foo')
    assert config.has_project('bar')
    assert not config.has_project('baz')

    foo = config.get_project('foo')
    assert foo['a'] == 1


def test_reload_project(tmpdir):
    tmpdir = str(tmpdir)
    config = Config(config_dir=tmpdir)
    create_project(tmpdir, 'foo', dict(a=1))

    foo = config.get_project('foo')
    assert foo['a'] == 1

    with open(config._get_project_path('foo'), 'wt') as fp:
        yaml.dump(dict(a=2), fp)

    foo = config.get_project('foo')
    assert foo['a'] == 2
