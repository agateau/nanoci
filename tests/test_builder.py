import os
import shutil
import subprocess

import pytest

from nanoci.builder import Builder, STATUS_SUCCESS, STATUS_FAILURE


class FakeObject(object):
    def __init__(self, dct):
        self._dct = dct

    def __getattr__(self, name):
        return self._dct[name]


def create_repo(src_dir, tmpdir):
    base_src_dir = os.path.dirname(__file__)
    repo_url = os.path.join(tmpdir, src_dir)
    shutil.copytree(os.path.join(base_src_dir, src_dir), repo_url)
    subprocess.check_call(['git', 'init'], cwd=repo_url)
    subprocess.check_call(['git', 'add', '.'], cwd=repo_url)
    subprocess.check_call(['git', 'commit', '-m', 'Import'], cwd=repo_url)
    return repo_url


@pytest.fixture(
    params=[{'dir': 'builds', 'success': True}, {'dir': 'fails', 'success': False}],
    ids=['builds', 'fails']
    )
def builder_info(request):
    return request.param


def test_builder(tmpdir, builder_info):
    tmpdir = str(tmpdir)
    url = create_repo(builder_info['dir'], tmpdir)
    config = FakeObject({
        'work_base_dir': tmpdir,
    })

    project = {
        'name': 'test',
        'source': {
            'url': url
        },
        'build': [{
            'script': './build.sh'
        }]
    }

    builder = Builder(config, project, 'HEAD')
    builder.build()
    expected_status = STATUS_SUCCESS if builder_info['success'] else STATUS_FAILURE
    assert builder.status == expected_status
