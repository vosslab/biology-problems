
source $HOME/.bashrc

source ~/nsh/PROBLEMS/qti-package-maker/source_me_for_testing.sh

THIS_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

REPO_TOPLEVEL_DIR="$(git -C "$THIS_SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null)" || {
  echo "Error: $THIS_SCRIPT_DIR is not inside a Git repository." >&2
  return 1 2>/dev/null || exit 1
}

REPO_PARENT_DIR="$(dirname "$REPO_TOPLEVEL_DIR")"
QTI_PACKAGE_MAKER_DIR="$REPO_PARENT_DIR/qti_package_maker"
CLEANPATH_PY="$REPO_PARENT_DIR/junk-drawer/cleanpath.py"
PYTHON_EXE="python3"

PYTHONPATH_PROPOSED="${PYTHONPATH-}"
if [[ -z "$PYTHONPATH_PROPOSED" ]]; then
  PYTHONPATH_PROPOSED="$THIS_SCRIPT_DIR"
else
  PYTHONPATH_PROPOSED="$THIS_SCRIPT_DIR:$PYTHONPATH_PROPOSED"
fi

# Add QTI package maker to PYTHONPATH if it exists
if [[ -d "$QTI_PACKAGE_MAKER_DIR" ]]; then
  PYTHONPATH_PROPOSED="$QTI_PACKAGE_MAKER_DIR:$PYTHONPATH_PROPOSED"
else
  echo "Warning: QTI package maker not found at $QTI_PACKAGE_MAKER_DIR" >&2
fi

if [[ -x "$CLEANPATH_PY" ]]; then
  export PYTHONPATH="$("$CLEANPATH_PY" -p "$PYTHONPATH_PROPOSED")"
else
  export PYTHONPATH="$PYTHONPATH_PROPOSED"
fi

export JUNKPATH="/Users/vosslab/nsh/junk-drawer"
export PYTHONPATH=$("$JUNKPATH/cleanpath.py" --separator ':' --path "$PYTHONPATH")

echo "PYTHONPATH is now: $PYTHONPATH"
echo "You can now run generators with: python3 path/to/script.py"
