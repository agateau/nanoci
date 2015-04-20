#!/usr/bin/env python3
import logging
import json

from flask import Flask, request

from nanoci.app import App
from nanoci.builder import Builder
from nanoci.process_queue import ProcessQueue


app = None
queue = None
webapp = Flask(__name__)


@webapp.route('/projects/')
def project_list():
    dct = app.projects
    return json.dumps({'list': sorted(dct.keys())})


@webapp.route('/projects/<name>/build')
def build(name):
    commit_id = request.args.get('commit_id', 'origin/HEAD')
    logging.info('Received request to build %s %s', name, commit_id)
    qsize = queue.add(name, commit_id)
    return json.dumps({'queue_size': qsize})


@webapp.route('/queue')
def show_queue():
    def _format_queue_args(queue_item):
        if queue_item is None:
            return None
        args = queue_item[0]
        return {
            'name': args[0],
            'commit_id': args[1]
        }

    current, queued = app.queue.get_queue()
    return json.dumps({
        'current': _format_queue_args(current),
        'queued': [_format_queue_args(x) for x in queued]
    })


def _build(name, commit_id):
    project = app.projects[name]
    builder = Builder(app.config, project, commit_id)
    builder.build()


def main():
    global app
    global queue
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(name)s/%(process)d: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)

    app = App()
    queue = ProcessQueue(_build)
    webapp.run(port=app.config.port)

if __name__ == '__main__':
    main()
# vi: ts=4 sw=4 et
