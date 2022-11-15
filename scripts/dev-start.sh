#!/usr/bin/env bash

set -o errexit
set -o nounset

watchfiles "python -m app.main" "app"
