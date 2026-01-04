#!/usr/bin/env bash

THIS_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

REPO_TOPLEVEL_DIR="$(git -C "$THIS_SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null)" || {
  echo "Error: $THIS_SCRIPT_DIR is not inside a Git repository." >&2
  return 1 2>/dev/null || exit 1
}

REPO_PARENT_DIR="$(dirname "$REPO_TOPLEVEL_DIR")"
QTI_PACKAGE_MAKER_DIR="$REPO_PARENT_DIR/qti_package_maker"
CLEANPATH_PY="$REPO_PARENT_DIR/junk-drawer/cleanpath.py"

SETUP_SCRIPT="$QTI_PACKAGE_MAKER_DIR/source_me_for_testing.sh"
if [[ ! -f "$SETUP_SCRIPT" ]]; then
  echo "Error: missing $SETUP_SCRIPT" >&2
  return 1 2>/dev/null || exit 1
fi

# shellcheck source=/dev/null
source "$SETUP_SCRIPT"

PYTHONPATH_PROPOSED="${PYTHONPATH-}"
if [[ -z "$PYTHONPATH_PROPOSED" ]]; then
  PYTHONPATH_PROPOSED="$THIS_SCRIPT_DIR"
else
  PYTHONPATH_PROPOSED="$THIS_SCRIPT_DIR:$PYTHONPATH_PROPOSED"
fi

if [[ -x "$CLEANPATH_PY" ]]; then
  export PYTHONPATH="$("$CLEANPATH_PY" -p "$PYTHONPATH_PROPOSED")"
else
  export PYTHONPATH="$PYTHONPATH_PROPOSED"
fi

echo "PYTHONPATH is now: $PYTHONPATH"
echo "You can now run generators with: python3 path/to/script.py"
