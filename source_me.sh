#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ -z "${PYTHONPATH:-}" ]]; then
	export PYTHONPATH="${SCRIPT_DIR}"
	echo "PYTHONPATH was unset. Initialized to: ${PYTHONPATH}"
elif [[ ":${PYTHONPATH}:" != *":${SCRIPT_DIR}:"* ]]; then
	export PYTHONPATH="${SCRIPT_DIR}:${PYTHONPATH}"
	echo "PYTHONPATH updated: ${PYTHONPATH}"
else
	echo "PYTHONPATH already contains repo root. No update needed."
fi

echo "You can now run generators with 'python3 path/to/script.py'."
