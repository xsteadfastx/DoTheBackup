#!/bin/bash

set -e

pex -r <(pipenv lock -r | cut -d' ' -f1) . -e dothebackup.ui:main --python=python3.6 --python=python3.5 --python=python3.4 --python-shebang=/usr/bin/python3 -o dist/dothebackup-`uname -s`-`uname -m`.pex -v
