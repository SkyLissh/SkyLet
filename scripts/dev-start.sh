#!/usr/bin/env bash

set -o errexit
set -o nounset

watchmedo auto-restart \
    --patterns="*.py" \
    --recursive \
    --directory="app/" \
    -- \
    python -m app.main
