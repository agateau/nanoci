# Nanoci

Nanoci is a personal CI server, designed to run on your developer machine.

## Install

    ./setup.py install

Optionally, run tests:

    python3 -m pytest -v

## Project configuration

Create a `~/.config/nanoci/projects/foo.yaml` with content similar to this:

    build:
        - type: git
          url: /path/to/a/git/repo  # Can also be a remote git url

        # A single-line script to run
        - type: shell
          script: make

        # A multi-line script to run
        - type: shell
          script: |
            make target1
            make target2

    notify:
        # An example of a command to run at the end of the build
        - type: shell
          name: notify
          script: |
            notify-send "$PROJECT_NAME $COMMIT_ID: $BUILD_STATUS"

## Global configuration

You can customize the global configuration by creating
`~/.config/nanoci/nanoci.yaml` with this content:

    # Port to listen to
    port: 5000
    # Where to checkout code and store build logs
    work_base_dir: ~/.cache/nanoci


## Starting nanoci

Run `nanoci-server`. This will start the server on port 5000 (unless you
changed the global configuration).

## Other commands

- `nanoci-build`: start a build
- `nanoci-log`: show the log of a build

## Triggering a build on each commit

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

## Author

Aurélien Gâteau

## License

3-clause BSD
