# Global config

Create ~/.config/nanoci.yaml

Content:
    workspace_base_dir: /path/to/a/dir

# Project config

Create ~/projects/foo.yaml

Content:

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

# REST API

## /projects/<name>/build

The project name is the name of the project .yaml file, without extensions.
Request building project <name>.

## /queue

State of the queue
