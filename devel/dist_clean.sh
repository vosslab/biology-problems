#!/usr/bin/env bash
# Deep clean: build/test output, caches, and dependency installs.
# Run ./devel/clean_build.sh instead to retain dependencies between builds.
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

delete_paths dist dist-single dist_browser_test dist_wasm generated _site build out
delete_paths _bundle.js meta.json stats.html node_modules .cache .eslintcache
delete_paths .prettiercache .nyc_output .build .swiftpm DerivedData test-results
delete_paths playwright-report blob-report coverage cover_db .turbo .next .svelte-kit
delete_paths .vite .parcel-cache env .tox .nox .hypothesis .coverage htmlcov
delete_paths .dmypy.json .pytype .eggs sdist wheelhouse pip-wheel-metadata .installed.cfg
delete_paths blib _build Build Build.bat MYMETA.json MYMETA.yml Makefile.old pm_to_blib
delete_paths local/lib/perl5 CMakeCache.txt CMakeFiles cmake_install.cmake
delete_paths compile_commands.json autom4te.cache target
delete_find_matches -type f -name '*.tsbuildinfo'
delete_find_matches -type d -name '*.xcresult'
delete_find_matches -type d -name 'xcuserdata'
delete_find_matches -type f -path '*/xcshareddata/swiftpm/Package.resolved'
delete_find_matches -type d -path './Packages/*/.build'
delete_find_matches -type d -path './Packages/*/.swiftpm'
delete_find_matches -type f -path './Packages/*/Package.resolved'
delete_find_matches -type d -name '.venv'
delete_find_matches -type d -name 'venv'
delete_find_matches -type d -name '__pycache__'
delete_find_matches -type d -name '.pytest_cache'
delete_find_matches -type d -name '.mypy_cache'
delete_find_matches -type d -name '.ruff_cache'
delete_find_matches -type f -name '.coverage.*'
delete_find_matches -type d -name '*.egg-info'
delete_find_matches -type f -name '*.egg'
delete_find_matches -type d -name CMakeFiles
delete_find_matches -type f -name CMakeCache.txt
delete_find_matches -type f \( -name '*.o' -o -name '*.obj' -o -name '*.a' -o -name '*.so' -o -name '*.dylib' \)

# Only remove nested target directories when Cargo identifies them as build output.
while IFS= read -r -d '' match; do
	parent="$(dirname "$match")"
	if [ -f "$parent/Cargo.toml" ] || [ -f "$match/CACHEDIR.TAG" ] || [ -f "$match/.rustc_info.json" ]; then
		rm -rf "$match"
		DELETED+=("${match#./}")
	fi
done < <(find . -mindepth 2 -type d -name target -print0)

if [ "${#DELETED[@]}" -eq 0 ]; then
	echo "Nothing to clean."
else
	echo "Cleaned ${#DELETED[@]} path(s):"
	for p in "${DELETED[@]}"; do
		echo "  $p"
	done
fi
