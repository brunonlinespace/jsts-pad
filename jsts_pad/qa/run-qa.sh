#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
CACHE_ROOT="$(mktemp -d -t jsts-pad-qa-cache.XXXXXX)"
trap 'rm -rf "$CACHE_ROOT"' EXIT
export PYTHONPYCACHEPREFIX="$CACHE_ROOT/pycache"
python3 -m unittest discover -s "$ROOT/jsts_pad/qa/tests" -p 'test_*.py' -v
python3 "$ROOT/jsts_pad/qa/release_check.py"
