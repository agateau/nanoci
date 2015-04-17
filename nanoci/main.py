#!/usr/bin/env python3
import logging
import json
import os

from flask import Flask, request

from nanoci import projects
from nanoci.process_queue import ProcessQueue


app = Flask(__name__)

_process_queue = ProcessQueue(projects.build)


@app.route('/projects/')
def project_list():
    dct = projects.get_all()
    return json.dumps({'list': sorted(dct.keys())})


@app.route('/projects/<name>/build')
def build(name):
    commit_id = request.args.get('commit_id', 'origin/HEAD')
    logging.info('Received request to build %s %s', name, commit_id)
    qsize = _process_queue.add(name, commit_id)
    return json.dumps({'queue_size': qsize})


@app.route('/queue')
def show_queue():
    def _format_queue_args(queue_item):
        if queue_item is None:
            return None
        args = queue_item[0]
        return {
            'name': args[0],
            'commit_id': args[1]
        }

    current, queued = _process_queue.get_queue()
    return json.dumps({
        'current': _format_queue_args(current),
        'queued': [_format_queue_args(x) for x in queued]
    })


def main():
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(name)s/%(process)d: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)

    projects.init(os.path.expanduser('~/.config/nanoci/nanoci.yaml'))
    projects.load_all(os.path.expanduser('~/.config/nanoci/projects'))
    app.run(debug=True)

if __name__ == '__main__':
    main()
# vi: ts=4 sw=4 et
