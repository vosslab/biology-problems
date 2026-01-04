#!/usr/bin/env bash
set -euo pipefail

GIT_ROOT=$(git rev-parse --show-toplevel)
REFACTOR_DIR="${GIT_ROOT}/refactor-Jan_2026"
LIST_FILE="${REFACTOR_DIR}/upgraded_phase_1_python_scripts.txt"
BUGS_FILE="${REFACTOR_DIR}/list_of_bugs.txt"

cd ${REFACTOR_DIR}

mapfile -t SCRIPTS < <(grep -v 'TEMPLATE' "${LIST_FILE}" | sed '/^[[:space:]]*$/d' | sort -R)

TOTAL=${#SCRIPTS[@]}
N=0

rm -f "${BUGS_FILE}"
FAILED_SCRIPTS=()

for SCRIPT in "${SCRIPTS[@]}"; do
	N=$((N + 1))

	sleep 0.1
	echo ""
	echo "------"
	echo "Script ${N} of ${TOTAL}: ${SCRIPT}"
	echo ""
	sleep 0.1

	set +e
	python3 "${GIT_ROOT}/${SCRIPT}" -d 5 -x 2
	RC=$?
	set -e

	if [[ "${RC}" -ne 0 ]]; then
		FAILED_SCRIPTS+=("${SCRIPT}")
		{
			echo "Script ${N} of ${TOTAL}: ${SCRIPT}"
			echo "Exit code: ${RC}"
			echo ""
		} >> "${BUGS_FILE}"
	fi

	sleep 0.1
	echo ""
	echo "Done ${N} of ${TOTAL}: ${SCRIPT}"
	echo "------"
	echo ""
done

echo ""
wc -l "${REFACTOR_DIR}"/bbq-*-questions.txt | sort -n | head -n 10
echo ""
wc -l "${REFACTOR_DIR}"/bbq-*-questions.txt | sort -n | tail -n 10
echo ""

rm -f "${REFACTOR_DIR}"/bbq-*-questions.txt

if [[ "${#FAILED_SCRIPTS[@]}" -ne 0 ]]; then
	echo ""
	echo "FAILED SCRIPTS (${#FAILED_SCRIPTS[@]}):"
	for SCRIPT in "${FAILED_SCRIPTS[@]}"; do
		echo "${SCRIPT}"
	done
	echo ""
	echo "Wrote: ${BUGS_FILE}"
	exit 1
fi

echo ""
echo "All scripts passed: ${TOTAL}"
