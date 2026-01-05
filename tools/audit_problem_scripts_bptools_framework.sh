#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
PYTHON="/opt/homebrew/opt/python@3.12/bin/python3.12"
exec "${PYTHON}" "${REPO_ROOT}/tools/audit_problem_scripts_bptools_framework.py"
