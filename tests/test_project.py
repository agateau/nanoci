import pytest

from nanoci.project import Project, ProjectError
from nanoci.step import Step
from nanoci.stepcreator import StepCreator


class FooStep(Step):
    type = 'foo'


class BarStep(Step):
    type = 'bar'


def create_step_creator():
    return StepCreator([FooStep, BarStep])


def test_project():
    build1 = dict(type='foo')
    notify1 = dict(type='bar')
    prj = Project('test', {
        'build': [build1],
        'notify': [notify1],
    }, step_creator=create_step_creator())

    assert prj.name == 'test'
    assert len(prj.build_steps) == 1
    assert isinstance(prj.build_steps[0], FooStep)
    assert len(prj.notify_steps) == 1
    assert isinstance(prj.notify_steps[0], BarStep)


def test_project_build_only():
    build1 = dict(type='foo')
    prj = Project('test', {
        'build': [build1],
    }, step_creator=create_step_creator())

    assert prj.name == 'test'
    assert len(prj.build_steps) == 1
    assert isinstance(prj.build_steps[0], FooStep)
    assert len(prj.notify_steps) == 0


def test_project_unknown_step():
    with pytest.raises(ProjectError):
        prj = Project('test', {
            'build': [
                dict(type='foo'),
                dict(type='unknown')
            ]
        }, step_creator=create_step_creator())
