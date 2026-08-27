#!/usr/bin/env bash
# dist_clean.sh - deep clean: wipe build artifacts, tool caches, and dependency
# installs to return the repo to a distribution-clean checkout.
#
# Front door: run this directly as ./devel/dist_clean.sh. This is the deep reset,
# used when preparing the repo for distribution or forcing a clean dependency
# reinstall. The lighter everyday build clean is devel/clean_build.sh (wired to
# `npm run clean`), which leaves node_modules intact.
#
# Keeps package-lock.json: it is committed and drives reproducible `npm ci`.
#
# Universal across repo types (python, perl, typescript, rust, c/c++, swift,
# etc.). Patterns that do not exist in a given repo are silently skipped via an
# existence check, so no false-positive output.
#
# After this runs you may need to reinstall language-specific dependencies
# before the usual gates work again:
#   typescript: npm install
#   python:     pip install -r pip_requirements.txt -r pip_requirements-dev.txt
#   rust:       cargo build (recompiles dependencies on next invocation)
#   swift:      dependencies re-fetch automatically on next build
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

delete_find_matches() {
	local label="$1"
	shift
	local match
	while IFS= read -r -d '' match; do
		rm -rf "$match"
		DELETED+=("${match#./}")
	done < <(find . "$@" -print0)
}

# Generic build outputs (any language).
delete_path dist
delete_path dist-single
delete_path dist_browser_test
delete_path dist_wasm
delete_path generated
delete_path _site
delete_path build
delete_path out

# TypeScript / JS build artifacts and bundler metadata.
delete_path _bundle.js
delete_path meta.json
delete_path stats.html
delete_find_matches tsbuildinfo -type f -name '*.tsbuildinfo'

# JS dependency installs (forces clean reinstall on next npm install). Keeps
# package-lock.json, which is committed and drives reproducible npm ci.
delete_path node_modules

# JS/TS tool caches.
delete_path .cache
delete_path .eslintcache
delete_path .prettiercache
delete_path .nyc_output

# Xcode / Swift build outputs and metadata.
delete_path .build
delete_path .swiftpm
delete_path DerivedData
delete_find_matches xcresult -type d -name '*.xcresult'
delete_find_matches xcuserdata -type d -name 'xcuserdata'
delete_find_matches PackageResolved -type f -path '*/xcshareddata/swiftpm/Package.resolved'
delete_find_matches packageBuild -type d -path './Packages/*/.build'
delete_find_matches packageSwiftpm -type d -path './Packages/*/.swiftpm'
delete_find_matches packageResolved -type f -path './Packages/*/Package.resolved'

# Test outputs (Playwright, coverage).
delete_path test-results
delete_path playwright-report
delete_path blob-report
delete_path coverage
delete_path cover_db

# Node framework build caches.
delete_path .turbo
delete_path .next
delete_path .svelte-kit
delete_path .vite
delete_path .parcel-cache

# Python bytecode, virtualenvs, and tool caches (any depth). Bare `env` stays
# root-only (delete_path below) because the name is too generic to sweep at
# depth without risking an unrelated directory.
delete_find_matches venvDot -type d -name '.venv'
delete_find_matches venvBare -type d -name 'venv'
delete_path env
delete_find_matches pycache -type d -name '__pycache__'
delete_find_matches pytest_cache -type d -name '.pytest_cache'
delete_find_matches mypy_cache -type d -name '.mypy_cache'
delete_find_matches ruff_cache -type d -name '.ruff_cache'
delete_path .tox
delete_path .nox
delete_path .hypothesis
delete_path .coverage
delete_find_matches coverageDataFiles -type f -name '.coverage.*'
delete_path htmlcov
delete_path .dmypy.json
delete_path .pytype

# Python packaging artifacts (PyPI sdist/wheel builds).
delete_find_matches eggInfo -type d -name '*.egg-info'
delete_find_matches eggFiles -type f -name '*.egg'
delete_path .eggs
delete_path sdist
delete_path wheelhouse
delete_path pip-wheel-metadata
delete_path .installed.cfg

# Perl build/test artifacts. Do not remove Makefile because many repos commit
# hand-written makefiles.
delete_path blib
delete_path _build
delete_path Build
delete_path Build.bat
delete_path MYMETA.json
delete_path MYMETA.yml
delete_path Makefile.old
delete_path pm_to_blib
delete_path local/lib/perl5

# C/C++ and CMake/autotools generated outputs.
delete_path CMakeCache.txt
delete_path CMakeFiles
delete_path cmake_install.cmake
delete_path compile_commands.json
delete_path autom4te.cache
delete_find_matches cmakeFiles -type d -name CMakeFiles
delete_find_matches cmakeCache -type f -name CMakeCache.txt
delete_find_matches objectFiles -type f \( -name '*.o' -o -name '*.obj' -o -name '*.a' -o -name '*.so' -o -name '*.dylib' \)

# Rust build outputs.
delete_path target

# Nested Rust workspace crate output dirs (cargo workspaces nest crates below
# the root). A bare `find . -name target` is dangerous because asset
# directories are commonly named target too, so only delete a nested `target`
# dir that sits beside a Cargo.toml or that carries cargo's own marker file.
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
