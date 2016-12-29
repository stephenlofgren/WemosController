#!/bin/bash

python3 venv --no-site-packages --distribute . && source ./bin/activate && pip install -r requirements.txt

