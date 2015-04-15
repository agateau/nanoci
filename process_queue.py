from multiprocessing import Process
from threading import Lock, Thread

from copy import deepcopy

import projects


_thread = None
_lock = Lock()
_queue = []


def worker():
    while True:
        with _lock:
            try:
                name, commit_id = _queue.pop(0)
            except IndexError:
                return
        proc = Process(target=projects.build, args=(name, commit_id))
        proc.start()
        proc.join()


def add(name, commit_id):
    global _thread

    with _lock:
        _queue.append((name, commit_id))
        queue_size = len(_queue)

    if _thread is None or not _thread.is_alive():
        _thread = Thread(target=worker)
        _thread.start()

    return queue_size


def get_queue():
    with _lock:
        return deepcopy(_queue)
