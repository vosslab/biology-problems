#!/usr/bin/env bash
set -euo pipefail

#repo_root="$(git rev-parse --show-toplevel)"
#cd "$repo_root"
#search_dir="$repo_root"
search_dir="."

find "$search_dir" -type f -name "bbq-*.txt" -print0 | xargs -0 rm -fv
find "$search_dir" -type f -name "bez-*.zip" -print0 | xargs -0 rm -fv
find "$search_dir" -type f -name "selftest-*.html" -print0 | xargs -0 rm -fv
