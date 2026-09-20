#!/usr/bin/env bash
# This file is vendored. Local changes can and will be overwritten by propagation.

# Light clean: build/test output and caches only. Dependencies stay installed.
# For a distribution-clean checkout that re-fetches dependencies, use dist_clean.sh.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

DELETED=()

delete_path() {
	local p="$1"
	if [ -e "$p" ] || [ -L "$p" ]; then
		rm -rf "$p"
		DELETED+=("$p")
	fi
}

delete_paths() {
	local path
	for path in "$@"; do
		delete_path "$path"
	done
}

delete_find_matches() {
	local match
	while IFS= read -r -d '' match; do
		rm -rf "$match"
		DELETED+=("${match#./}")
	done < <(find . "$@" -print0)
}

delete_paths dist dist-single _site build out _bundle.js meta.json stats.html
delete_paths .cache .eslintcache .prettiercache .nyc_output
# Keep SwiftPM dependency checkouts and resolution state for the next build.
delete_paths .build/debug .build/release .build/artifacts .build/build.db DerivedData
delete_paths test-results playwright-report blob-report coverage
delete_find_matches -type f -name '*.tsbuildinfo'
delete_find_matches -type d -path './.build/*-apple-macosx'
delete_find_matches -type f -path './.build/*.yaml'
delete_find_matches -type d -name '*.xcresult'
delete_find_matches -type d -name 'xcuserdata'
delete_find_matches -type d -name '__pycache__'
delete_find_matches -type d -name '.pytest_cache'
delete_find_matches -type d -name '.mypy_cache'
delete_find_matches -type d -name '.ruff_cache'

if [ "${#DELETED[@]}" -eq 0 ]; then
	echo "Nothing to clean."
else
	echo "Cleaned ${#DELETED[@]} path(s):"
	for p in "${DELETED[@]}"; do
		echo "  $p"
	done
fi
