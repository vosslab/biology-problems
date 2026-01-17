#!/usr/bin/env bash
set -e

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "${REPO_ROOT}"

PYFLAKES_OUT="${REPO_ROOT}/pyflakes.txt"
PYFLAKES_TMP=""
CHANGED_LIST=""
TRACKED_LIST=""

cleanup() {
	if [ -n "${CHANGED_LIST:-}" ]; then
		rm -f "${CHANGED_LIST}"
	fi
	if [ -n "${TRACKED_LIST:-}" ]; then
		rm -f "${TRACKED_LIST}"
	fi
	if [ -n "${PYFLAKES_TMP:-}" ]; then
		rm -f "${PYFLAKES_TMP}"
	fi
}
trap cleanup EXIT

SCOPE="${REPO_HYGIENE_SCOPE:-}"
if [ -z "${SCOPE}" ] && [ "${FAST_REPO_HYGIENE:-}" = "1" ]; then
	SCOPE="changed"
fi

# Run pyflakes on all Python files and capture output
if [ "${SCOPE}" = "changed" ]; then
	CHANGED_LIST="$(mktemp)"
	collect_changed_files() {
		git diff --name-only --diff-filter=ACMRTUXB -z
		git diff --name-only --cached --diff-filter=ACMRTUXB -z
	}
	collect_changed_files | while IFS= read -r -d '' path; do
		if [ -z "${path}" ]; then
			continue
		fi
		case "${path}" in
			.git/*|*/.git/*|.venv/*|*/.venv/*|old_shell_folder/*|*/old_shell_folder/*)
				continue
				;;
		esac
		if [[ "${path}" != *.py ]]; then
			continue
		fi
		if [[ "${path}" == *TEMPLATE* ]]; then
			continue
		fi
		printf '%s\0' "${path}"
	done | sort -zu > "${CHANGED_LIST}"
	FILE_COUNT=$(tr -cd '\0' < "${CHANGED_LIST}" | wc -c | tr -d ' ')
	if [ "${FILE_COUNT}" -eq 0 ]; then
		echo "pyflakes: no Python files matched scope changed."
		rm -f "${PYFLAKES_OUT}"
		echo "No errors found!!!"
		exit 0
	fi
	echo "pyflakes: scanning ${FILE_COUNT} files..."
	PYFLAKES_TMP="$(mktemp)"
	xargs -0 pyflakes < "${CHANGED_LIST}" > "${PYFLAKES_TMP}" 2>&1 || true
else
	TRACKED_LIST="$(mktemp)"
	git ls-files -z -- "*.py" | while IFS= read -r -d '' path; do
		if [ -z "${path}" ]; then
			continue
		fi
		case "${path}" in
			.git/*|*/.git/*|.venv/*|*/.venv/*|old_shell_folder/*|*/old_shell_folder/*)
				continue
				;;
		esac
		if [[ "${path}" == *TEMPLATE* ]]; then
			continue
		fi
		if [ ! -f "${path}" ]; then
			continue
		fi
		printf '%s\0' "${path}"
	done | sort -zu > "${TRACKED_LIST}"
	FILE_COUNT=$(tr -cd '\0' < "${TRACKED_LIST}" | wc -c | tr -d ' ')
	if [ "${FILE_COUNT}" -eq 0 ]; then
		echo "pyflakes: no Python files matched scope all."
		rm -f "${PYFLAKES_OUT}"
		echo "No errors found!!!"
		exit 0
	fi
	echo "pyflakes: scanning ${FILE_COUNT} files..."
	PYFLAKES_TMP="$(mktemp)"
	xargs -0 pyflakes < "${TRACKED_LIST}" > "${PYFLAKES_TMP}" 2>&1 || true
fi

RESULT=$(wc -l < "${PYFLAKES_TMP}" | tr -d ' ')

N=5
SMALL_LIMIT=20

# Success if no errors were found
if [ "${RESULT}" -eq 0 ]; then
	rm -f "${PYFLAKES_OUT}"
	echo "No errors found!!!"
	exit 0
fi

mv "${PYFLAKES_TMP}" "${PYFLAKES_OUT}"
PYFLAKES_TMP=""

shorten_paths() {
	sed -E 's|.*/([^/:]+:)|\1|'
}

summarize_errors() {
	awk '
		BEGIN {
			import=0; syntax=0; name=0; variable=0; warning=0; other=0
		}
		{
			line=$0
			if (line !~ /:[0-9]+:[0-9]+:/) {
				next
			}
			if (line ~ /imported but unused/ || line ~ /import \* used/ || line ~ /could not import/) {
				import++
			} else if (line ~ /syntax error/ || line ~ /SyntaxError/ || line ~ /invalid syntax/ \
				|| line ~ /Missing parentheses in call to/ || line ~ /Did you mean print/ \
				|| line ~ /from __future__ imports must occur at the beginning/ \
				|| line ~ /unexpected indent/ || line ~ /EOL while scanning string literal/ \
				|| line ~ /EOF while scanning triple-quoted string literal/ \
				|| line ~ /unterminated string literal/ || line ~ /cannot assign to/ \
				|| line ~ /cannot use .* as / || line ~ /invalid decimal literal/) {
				syntax++
			} else if (line ~ /undefined name/ || line ~ /undefined local/ || line ~ /undefined variable/) {
				name++
			} else if (line ~ /assigned to but never used/ || line ~ /referenced before assignment/ \
				|| line ~ /redefinition of unused/) {
				variable++
			} else if (line ~ /Warning:/ || line ~ /DeprecationWarning/ || line ~ /SyntaxWarning/) {
				warning++
			} else {
				other++
			}
		}
		END {
			print "Error categories"
			print "Import errors: " import
			print "Syntax errors: " syntax
			print "Name errors: " name
			print "Variable errors: " variable
			print "Warning errors: " warning
			print "Other errors: " other
		}
	' "${PYFLAKES_OUT}"
}

print_unclassified() {
	awk '
		BEGIN {
			printed=0
		}
		{
			line=$0
			if (line !~ /:[0-9]+:[0-9]+:/) {
				next
			}
			if (line ~ /imported but unused/ || line ~ /import \* used/ || line ~ /could not import/) {
				next
			} else if (line ~ /syntax error/ || line ~ /SyntaxError/ || line ~ /invalid syntax/ \
				|| line ~ /Missing parentheses in call to/ || line ~ /Did you mean print/ \
				|| line ~ /from __future__ imports must occur at the beginning/ \
				|| line ~ /unexpected indent/ || line ~ /EOL while scanning string literal/ \
				|| line ~ /EOF while scanning triple-quoted string literal/ \
				|| line ~ /unterminated string literal/ || line ~ /cannot assign to/ \
				|| line ~ /cannot use .* as / || line ~ /invalid decimal literal/) {
				next
			} else if (line ~ /undefined name/ || line ~ /undefined local/ || line ~ /undefined variable/) {
				next
			} else if (line ~ /assigned to but never used/ || line ~ /referenced before assignment/ \
				|| line ~ /redefinition of unused/) {
				next
			} else if (line ~ /Warning:/ || line ~ /DeprecationWarning/ || line ~ /SyntaxWarning/) {
				next
			}
			print line
			printed++
			if (printed >= 5) {
				exit
			}
		}
	' "${PYFLAKES_OUT}" | shorten_paths
}

if [ "${RESULT}" -le "${SMALL_LIMIT}" ]; then
	echo ""
	echo "Last ${N} errors"
	grep -E ':[0-9]+:[0-9]+:' "${PYFLAKES_OUT}" | tail -n "${N}" | shorten_paths
	echo "-------------------------"
	echo ""
	echo "Found ${RESULT} pyflakes errors written to REPO_ROOT/pyflakes.txt"
	exit 1
fi

echo ""
echo "First ${N} errors"
grep -E ':[0-9]+:[0-9]+:' "${PYFLAKES_OUT}" | head -n "${N}" | shorten_paths
echo "-------------------------"
echo ""

echo "Random ${N} errors"
grep -E ':[0-9]+:[0-9]+:' "${PYFLAKES_OUT}" | sort -R | head -n "${N}" | shorten_paths || true
echo "-------------------------"
echo ""

echo "Last ${N} errors"
grep -E ':[0-9]+:[0-9]+:' "${PYFLAKES_OUT}" | tail -n "${N}" | shorten_paths
echo "-------------------------"
echo ""

summarize_errors
echo "-------------------------"
echo ""

echo "Unclassified errors (up to ${N})"
print_unclassified
echo "-------------------------"
echo ""

echo "Found ${RESULT} pyflakes errors written to REPO_ROOT/pyflakes.txt"

# Fail if any errors were found
exit 1
