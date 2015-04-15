# Project config

Create `~/.config/nanoci/projects/foo.yaml` with this content:

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

# Global config

You can customize the global configuration by creating
`~/.config/nanoci/nanoci.yaml` with this content:

    work_base_dir: /where/to/checkout/code  # defaults to ~/.cache/nanoci/


# Start nanoci

`python nanoci.py`

Will listen on `http://localhost:5000`.

# Trigger a build on each commit

Create a .git/hooks/post-commit file with this content:

    #!/bin/sh
    commit_id=$(git rev-parse HEAD)
    curl http://localhost:5000/projects/$name/build?commit_id=$commit_id

And make it executable.

# REST API

## /projects/

Returns the project list.

## /projects/$name/build

Requests a build of project `name`.

The project name is the name of the project .yaml file, without extensions.

## /queue

Show the state of the queue.
