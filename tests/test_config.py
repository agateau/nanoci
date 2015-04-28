import os

import yaml

from nanoci.config import Config

from nanoci.fileutils import mkdir_p


def create_project(tmpdir, name, build=None, notify=None):
    project_path = os.path.join(tmpdir, 'projects', name + '.yaml')
    mkdir_p(os.path.dirname(project_path))
    dct = {}
    if build is not None:
        dct['build'] = build
    if notify is not None:
        dct['notify'] = notify
    with open(project_path, 'wt') as fp:
        yaml.dump(dct, fp)


def test_projects(tmpdir):
    tmpdir = str(tmpdir)
    config = Config(config_dir=tmpdir)
    create_project(tmpdir, 'foo', build=[{'script':'make'}])
    create_project(tmpdir, 'bar')

    assert config.has_project('foo')
    assert config.has_project('bar')
    assert not config.has_project('baz')

    assert config.get_project_path('foo') == os.path.join(tmpdir, 'projects/foo.yaml')
