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

Create a `.git/hooks/post-commit` file with this content:

    #!/bin/sh
    set -e
    if [ -d .git/rebase-merge ] ; then
        # post-commit is called for each commit while rebasing, you probably
        # don't want nanoci to be called at this time.
        exit 0
    fi
    commit_id=$(git rev-parse HEAD)
    nanoci-build $name $commit_id

And make it executable.

Note that you should use `post-commit`, not `pre-commit` because Nanoci needs
the commit ID to start building, so the commit must have been created.
