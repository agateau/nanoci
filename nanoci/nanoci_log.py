#!/usr/bin/env python3
import argparse
import os
import sys
import time

from pydoc import pager

from nanoci.config import Config
from nanoci.builder import Builder


DESCRIPTION = """\
Show build logs for a project
"""

def read_file_end(filename, linecount):
    content = open(filename, 'rt').readlines()
    return ''.join(content[-linecount:]).strip()


def list_builds(log_base_dir):
    ids = [int(x) for x in os.listdir(log_base_dir) if x.isdigit()]
    for id in sorted(ids):
        print()
        print(id, end=': ')
        log_file = os.path.join(log_base_dir, str(id), 'build.log')
        if not os.path.exists(log_file):
            print('No log file!')
            continue
        statinfo = os.stat(log_file)
        print(time.ctime(statinfo.st_mtime))
        print(read_file_end(log_file, 4))


def main():
    parser = argparse.ArgumentParser()
    parser.description = DESCRIPTION
    parser.add_argument('-l', '--list', dest='lst', action='store_true',
                        default=False, help='List build results')
    parser.add_argument('name', help='Name of project')
    parser.add_argument('build_id', help='Build number (defaults to last)',
                        nargs='?')
    args = parser.parse_args()
    project_name = args.name

    config = Config()
    if not config.has_project(project_name):
        parser.error('Invalid project name {}'.format(project_name))

    log_base_dir = Builder.get_log_base_dir(config, project_name)

    if args.lst:
        list_builds(log_base_dir)
        return 0

    if args.build_id is None:
        ids = [int(x) for x in os.listdir(log_base_dir) if x.isdigit()]
        build_id = str(max(ids))
    else:
        build_id = args.build_id
    log_dir = os.path.join(log_base_dir, build_id)

    log_path = os.path.join(log_dir, Builder.BUILD_LOG_NAME)
    pager(open(log_path, 'rt').read())


if __name__ == '__main__':
    sys.exit(main())
# vi: ts=4 sw=4 et
