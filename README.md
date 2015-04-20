# Install

    ./setup.py install

Optionally, run tests:

    python3 -m pytest -v

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

    port: 5000
    work_base_dir: /where/to/checkout/code  # defaults to ~/.cache/nanoci/


# Start nanoci

Run `nanoci`. This will start the daemon, listening on port 5000 by default.

# Trigger a build on each commit

Create a .git/hooks/post-commit file with this content:

    #!/bin/sh
    commit_id=$(git rev-parse HEAD)
    nanoci-build $name $commit_id

And make it executable.
