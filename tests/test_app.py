import os

import yaml

from nanoci.app import App

from nanoci.fileutils import mkdir_p


def create_project(tmpdir, name, dct):
    project_path = os.path.join(tmpdir, 'projects', name + '.yaml')
    mkdir_p(os.path.dirname(project_path))
    with open(project_path, 'wt') as fp:
        yaml.dump(dct, fp)


def test_app_config(tmpdir):
    tmpdir = str(tmpdir)
    app = App(config_dir=tmpdir)
    config = app.config


def test_app_projects(tmpdir):
    tmpdir = str(tmpdir)
    app = App(config_dir=tmpdir)
    create_project(tmpdir, 'foo', dict(a=1))
    create_project(tmpdir, 'bar', dict())

    assert app.has_project('foo')
    assert app.has_project('bar')
    assert not app.has_project('baz')

    foo = app.get_project('foo')
    assert foo['a'] == 1


def test_reload_project(tmpdir):
    tmpdir = str(tmpdir)
    app = App(config_dir=tmpdir)
    create_project(tmpdir, 'foo', dict(a=1))

    foo = app.get_project('foo')
    assert foo['a'] == 1

    with open(app._get_project_path('foo'), 'wt') as fp:
        yaml.dump(dict(a=2), fp)

    foo = app.get_project('foo')
    assert foo['a'] == 2
