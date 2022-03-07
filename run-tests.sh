#!/bin/bash
set -eou pipefail

export DEVELOPMENT='TRUE'
poetry run python -m pytest -rx tests -v "$@"
