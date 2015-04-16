from multiprocessing import Process
from threading import Lock, Thread

from copy import deepcopy

import projects


class ProcessQueue(object):
    def __init__(self):
        self._lock = Lock()
        self._queue = []
        self._thread = None

    def add(self, name, commit_id):
        with self._lock:
            self._queue.append((name, commit_id))
            queue_size = len(self._queue)

        if self._thread is None or not self._thread.is_alive():
            self._thread = Thread(target=self._worker)
            self._thread.start()

        return queue_size

    def _worker(self):
        while True:
            with self._lock:
                try:
                    name, commit_id = self._queue.pop(0)
                except IndexError:
                    return
            proc = Process(target=projects.build, args=(name, commit_id))
            proc.start()
            proc.join()

    def get_queue(self):
        with self._lock:
            return deepcopy(self._queue)
