from multiprocessing import Process
from threading import Lock, Thread

from copy import deepcopy


class ProcessQueue(object):
    def __init__(self, target):
        self._lock = Lock()
        self._queue = []
        self._thread = None
        self._target = target

    def add(self, *args, **kwargs):
        with self._lock:
            self._queue.append((args, kwargs))
            queue_size = len(self._queue)

        if self._thread is None or not self._thread.is_alive():
            self._thread = Thread(target=self._worker)
            self._thread.start()

        return queue_size

    def _worker(self):
        while True:
            with self._lock:
                try:
                    args, kwargs = self._queue.pop(0)
                except IndexError:
                    return
            proc = Process(target=self._target, args=args, kwargs=kwargs)
            proc.start()
            proc.join()

    def get_queue(self):
        with self._lock:
            return deepcopy(self._queue)
