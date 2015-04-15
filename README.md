# Global config

Create `~/.config/nanoci.yaml` with this content:

    workspace_base_dir: /where/to/checkout/code
    log_base_dir: /where/to/store/logs                # defaults to ~/.cache/nanoci/log

# Project config

Create `~/projects/foo.yaml` with this content:

    source:
        url: <git_url>
    build:
        - type: shell
          name: build
          script: ...
        - type: shell
          name: test
          script: ...
    notify:
        - type: shell
          name: notify
          script: ...

# Start nanoci

`python nanoci.py ~/projects`

Will listen on `http://localhost:5000`.

# Trigger a build on each commit

Create a .git/hooks/post-commit file with this content:

    #!/bin/sh
    commit_id=$(git rev-parse HEAD)
    curl http://localhost:5000/projects/$name/build?commit_id=$commit_id

And make it executable.

# REST API

## /projects/$name/build

Requests a build of project `name`.

The project name is the name of the project .yaml file, without extensions.

## /queue

Show the state of the queue.
