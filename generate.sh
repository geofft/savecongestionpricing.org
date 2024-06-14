#!/bin/bash

set -eux -o pipefail

python3 -m venv venv
venv/bin/pip install -U pip
venv/bin/pip install -r requirements.txt

venv/bin/python3 render.py
