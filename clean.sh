#!/usr/bin/env bash

find . -name '*.pyc' -delete
find . -name '__pycache__' -exec rm -r {} +
