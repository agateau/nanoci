# Global config

Create `~/.config/nanoci.yaml` with this content:

    workspace_base_dir: /where/to/checkout/code
    log_dir: /where/to/store/logs                # defaults to ~/.cache/nanoci/log

# Project config

Create `~/projects/foo.yaml` with this content:

    source:
        url: <git_url>
    build_steps:
        - type: shell
          name: build
          script: ...
        - type: shell
          name: test
          script: ...
    notifiers:
        - type: shell
          name: notify
          script: ...

# Start nanoci

`python nanoci.py ~/projects`

Will listen on `http://localhost:5000`.

# REST API

## /projects/$name/build

Requests a build of project `name`.

The project name is the name of the project .yaml file, without extensions.


## /queue

Show the state of the queue.
