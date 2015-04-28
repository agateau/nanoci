from nanoci.project import Project


def test_project():
    build1 = dict(script='make')
    notify1 = dict(script='hello')
    prj = Project('test', {
        'build': [build1],
        'notify': [notify1],
    })

    assert prj.name == 'test'
    assert prj.build_steps == [build1]
    assert prj.notify_steps == [notify1]


def test_project_build_only():
    build1 = dict(script='make')
    prj = Project('test', {
        'build': [build1],
    })

    assert prj.name == 'test'
    assert prj.build_steps == [build1]
    assert prj.notify_steps == []
