import pytest

from nanoci.project import Project, ProjectError


def test_project():
    build1 = dict(script='make')
    notify1 = dict(script='hello')
    prj = Project('test', {
        'build': [build1],
        'notify': [notify1],
    })

    assert prj.name == 'test'
    assert len(prj.build_steps) == 1
    assert prj.build_steps[0]._arguments == build1
    assert len(prj.notify_steps) == 1
    assert prj.notify_steps[0]._arguments == notify1


def test_project_build_only():
    build1 = dict(script='make')
    prj = Project('test', {
        'build': [build1],
    })

    assert prj.name == 'test'
    assert len(prj.build_steps) == 1
    assert prj.build_steps[0]._arguments == build1
    assert len(prj.notify_steps) == 0


def test_project_unknown_step():
    with pytest.raises(ProjectError):
        prj = Project('test', {
            'build': [
                dict(type='shell', script='make'),
                dict(type='unknown')
            ]
        })
