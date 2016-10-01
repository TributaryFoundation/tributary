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
    parser.add_argument("--port", help="port to listen on", default=5000, action="store", type=int)
    return parser.parse_args()


def run(port, debug):
    extra_files = all_files('templates') + all_files('static')
    app.run(host='0.0.0.0', port=port, extra_files=extra_files, debug=debug)


if __name__ == '__main__':
    args = parse_args()
    run(args.port, args.debug)
