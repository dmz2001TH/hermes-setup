#!/bin/bash
source "$(dirname "$0")/venv/bin/activate"
hermes dashboard --port 9119 --host 127.0.0.1 --no-open
