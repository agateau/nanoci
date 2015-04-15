#!/usr/bin/env python3
import logging
import json
import os
import sys

from flask import Flask, request

import process_queue
import projects

app = Flask(__name__)


_running_builds = []


@app.route('/projects/')
def project_list():
    dct = projects.get_all()
    return json.dumps({'list': sorted(dct.keys())})


@app.route('/projects/<name>/build')
def build(name):
    commit_id = request.args.get('commit_id', 'origin/HEAD')
    logging.info('Received request to build %s %s', name, commit_id)
    qsize = process_queue.add(name, commit_id)
    return json.dumps({'queue_size': qsize})


@app.route('/queue')
def show_queue():
    return json.dumps({'waiting': process_queue.get_queue()})


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)

    projects.init(os.path.expanduser('~/.config/nanoci/nanoci.yaml'))
    projects.load_all(os.path.expanduser('~/.config/nanoci/projects'))
    app.run(debug=True)

# vi: ts=4 sw=4 et
