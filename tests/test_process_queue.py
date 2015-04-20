import os

from nanoci.process_queue import ProcessQueue


def test_many_processes(tmpdir):
    tmpdir = str(tmpdir)
    print(tmpdir)

    def job(flag):
        path = os.path.join(tmpdir, flag)
        with open(path, 'w') as f:
            f.write('boo')
        return 0

    queue = ProcessQueue(job)

    flags = [str(x) for x in range(200)]
    flags.sort()
    for flag in flags:
        queue.add(str(flag))

    queue.join()

    lst = os.listdir(tmpdir)
    lst.sort()
    assert lst == flags


def test_empty_at_end():
    def job():
        return 0
    queue = ProcessQueue(job)
    queue.add()
    queue.join()

    current, remaining = queue.get_queue()
    assert current == None
    assert remaining == []
