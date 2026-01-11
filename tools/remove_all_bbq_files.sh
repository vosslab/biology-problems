#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

find "$repo_root" -type f -name "bbq-*.txt" -print0 | xargs -0 rm -fv
