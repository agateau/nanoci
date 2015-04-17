#!/usr/bin/env python3
import sys
import argparse

import requests

from app import App


DESCRIPTION = """\
"""


def main():
    parser = argparse.ArgumentParser()
    parser.description = DESCRIPTION
    parser.add_argument('name', help='Name of project to build')
    parser.add_argument('commit_id', help='Which commit ID to build, defaults to HEAD',
                        nargs='?')
    args = parser.parse_args()

    app = App()
    if not args.name in app.projects:
        parser.error('Invalid project name {}'.format(args.name))

    if args.commit_id:
        params = { 'commit_id': args.commit_id }
    else:
        params = {}

    url = app.config.server_url + '/projects/{}/build'.format(args.name)
    res = requests.get(url, params=params)
    if res.status_code == 200:
        print('Build scheduled')
        return 0
    else:
        print(res.content)
        return 1


if __name__ == '__main__':
    sys.exit(main())
# vi: ts=4 sw=4 et
