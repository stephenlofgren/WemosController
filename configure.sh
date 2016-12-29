#!/bin/bash

virtualenv --no-site-packages --distribute . && source ./bin/activate && pip install -r requirements.txt

