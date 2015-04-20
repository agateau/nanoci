import os

import yaml

from nanoci.app import App

from nanoci.fileutils import mkdir_p


def create_project(tmpdir, name, dct):
    project_path = os.path.join(tmpdir, 'projects', name + '.yaml')
    mkdir_p(os.path.dirname(project_path))
    with open(project_path, 'wt') as fp:
        yaml.dump(dct, fp)


def test_app_properties(tmpdir):
    tmpdir = str(tmpdir)

    create_project(tmpdir, 'foo', dict())
    create_project(tmpdir, 'bar', dict())
    app = App(config_dir=tmpdir)

    config = app.config
    projects = app.projects
    assert set(projects.keys()) == {'foo', 'bar'}
