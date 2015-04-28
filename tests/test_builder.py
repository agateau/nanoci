import pytest

from nanoci.builder import Builder, STATUS_SUCCESS, STATUS_FAILURE
from nanoci.project import Project
from nanoci.step import Step
from nanoci.stepcreator import StepCreator


class FakeObject(object):
    def __init__(self, dct):
        self._dct = dct

    def __getattr__(self, name):
        return self._dct[name]


class FakeStep(Step):
    type = 'fake'

    def run(self, log_fp, env):
        return self._arguments['ok']


@pytest.fixture(
    params=[
        {
            'build': [
                dict(type='fake', ok=True)
            ],
            'success': True
        },
        {
            'build': [
                dict(type='fake', ok=False)
            ],
            'success': False
        }
    ],
    ids=['builds', 'fails']
    )
def builder_info(request):
    return request.param


def test_builder(tmpdir, builder_info):
    tmpdir = str(tmpdir)
    config = FakeObject({
        'work_base_dir': tmpdir,
    })

    project = Project('test', {
        'build': builder_info['build']
    }, step_creator=StepCreator([FakeStep]))

    builder = Builder(config, project, 'HEAD')
    builder.build()
    expected_status = STATUS_SUCCESS if builder_info['success'] else STATUS_FAILURE
    assert builder.status == expected_status
