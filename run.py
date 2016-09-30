#!/usr/bin/env python
import argparse
import os

from app import app

def all_files(dir):
    ''' list all files in a directory '''
    files = []
    for root, _, dirfiles in os.walk(dir):
        files.extend([os.path.join(root, f) for f in dirfiles])
    return files


def parse_args():
    ''' parse arguments and return their argparse.Namespace '''
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", help="set flask to debug mode", default=False, action="store_true")
    return parser.parse_args()


def run(debug):
    templates = all_files('templates')
    app.run(extra_files=templates, debug=debug)


if __name__ == '__main__':
    args = parse_args()
    run(args.debug)
