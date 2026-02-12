
source $HOME/.bashrc

THIS_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

REPO_TOPLEVEL_DIR="$(git -C "$THIS_SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null)" || {
  echo "Error: $THIS_SCRIPT_DIR is not inside a Git repository." >&2
  return 1 2>/dev/null || exit 1
}

REPO_PARENT_DIR="$(dirname "$REPO_TOPLEVEL_DIR")"
QTI_PACKAGE_MAKER_DIR="$REPO_PARENT_DIR/qti_package_maker"
PGML_LINTER_DIR="$REPO_PARENT_DIR/webwork-pgml-linter"
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

# Add PGML linter to PYTHONPATH if it exists
if [[ -d "$PGML_LINTER_DIR" ]]; then
  PYTHONPATH_PROPOSED="$PGML_LINTER_DIR:$PYTHONPATH_PROPOSED"
fi

if [[ -x "$CLEANPATH_PY" ]]; then
  export PYTHONPATH="$("$CLEANPATH_PY" -p "$PYTHONPATH_PROPOSED")"
else
  export PYTHONPATH="$PYTHONPATH_PROPOSED"
fi

echo "PYTHONPATH is now: $PYTHONPATH"
echo "You can now run generators with: python3 path/to/script.py"

# ================================
# PGML Linter Setup
# ================================
PGML_LINTER_SCRIPT="$PGML_LINTER_DIR/tools/webwork_pgml_simple_lint.py"
PG_RENDERER_SCRIPT="$REPO_PARENT_DIR/webwork-pg-renderer/script/lint_pg_via_renderer_api.py"

if [[ -f "$PGML_LINTER_SCRIPT" ]]; then
	# Create a shell function to invoke the linter
	pgml-lint() {
		"$PYTHON_EXE" "$PGML_LINTER_SCRIPT" "$@"
	}
	export -f pgml-lint
	echo "PGML linter available: pgml-lint -i file.pg"
else
	echo "Warning: PGML linter not found at $PGML_LINTER_SCRIPT" >&2
fi

# ================================
# PG Renderer Shortcut
# ================================
if [[ -f "$PG_RENDERER_SCRIPT" ]]; then
	pg-render() {
		"$PYTHON_EXE" "$PG_RENDERER_SCRIPT" "$@"
	}
	export -f pg-render
	echo "Renderer shortcut available: pg-render -r -i file.pgml"
else
	echo "Warning: renderer script not found at $PG_RENDERER_SCRIPT" >&2
fi
