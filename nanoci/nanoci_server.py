#!/usr/bin/env python3
import logging
import json

from flask import Flask, request

from nanoci.builder import Builder
from nanoci.config import Config
from nanoci.process_queue import ProcessQueue
from nanoci.project import Project
from nanoci.stepcreator import StepCreator


config = None
queue = None
step_creator = StepCreator()
app = Flask(__name__)


@app.route('/projects/<name>/build')
def build(name):
    commit_id = request.args.get('commit_id', 'origin/HEAD')
    logging.info('Received request to build %s %s', name, commit_id)
    qsize = queue.add(name, commit_id)
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

    current, queued = queue.get_queue()
    return json.dumps({
        'current': _format_queue_args(current),
        'queued': [_format_queue_args(x) for x in queued]
    })


def _build(name, commit_id):
    project_path = config.get_project_path(name)
    project = Project(name, project_path, step_creator=step_creator)
    builder = Builder(config, project, commit_id)
    builder.build()


def main():
    global config
    global queue
    global step_creator
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(name)s/%(process)d: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)

    config = Config()

    # FIXME: get available step_classes from somewhere else
    from nanoci.gitstep import GitStep
    from nanoci.shellstep import ShellStep
    step_creator.add_step_class(ShellStep)
    step_creator.add_step_class(GitStep)

    queue = ProcessQueue(_build)
    app.run(port=config.port)


if __name__ == '__main__':
    main()
# vi: ts=4 sw=4 et
