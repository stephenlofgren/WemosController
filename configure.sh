#!/bin/bash

python3 -m venv --no-site-packages --distribute . && source ./bin/activate && pip install -r requirements.txt

