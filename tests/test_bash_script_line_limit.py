"""Enforce a maintainable size limit for Bash shell scripts."""

# Standard Library
import os

# PIP3 modules
import pytest

# local repo modules
import file_utils


LINE_LIMIT = 100
CHARACTER_LIMIT = 8000
REPORT_NAME = file_utils.report_name(__file__)
HEADER = "Bash script line-limit violations:"
VIOLATIONS_BY_FILE: dict[str, list[str]] = {}

FILES = file_utils.discover_files(
	extensions=(".sh",),
	test_key="bash_script_line_limit",
)


#============================================
def violations_for_counts(
		rel: str,
		line_count: int,
		character_count: int,
) -> list[str]:
	"""Return a violation when a Bash script reaches either exclusive limit."""
	if line_count < LINE_LIMIT and character_count < CHARACTER_LIMIT:
		return []
	message = (
		f"{rel}: {line_count} lines (limit {LINE_LIMIT}), {character_count} "
		f"characters (limit {CHARACTER_LIMIT}). Simplify this Bash script, or move "
		"substantial logic to Python (the source-file limit is 1000 lines)."
	)
	return [message]


#============================================
def check_file(rel: str) -> list[str]:
	"""Check one Bash script against both exclusive limits."""
	abs_path = os.path.join(file_utils.get_repo_root(), rel)
	with open(abs_path, "r", encoding="utf-8") as handle:
		contents = handle.read()
	line_count = contents.count("\n")
	if contents and not contents.endswith("\n"):
		line_count += 1
	character_count = len(contents)
	violations = violations_for_counts(rel, line_count, character_count)
	return violations


#============================================
@pytest.fixture(scope="module", autouse=True)
def collect_report() -> None:
	"""Collect line-limit violations and write the report when dirty."""
	file_utils.clear_stale_reports()
	VIOLATIONS_BY_FILE.clear()
	VIOLATIONS_BY_FILE.update(file_utils.collect_file_violations(FILES, check_file))
	lines = file_utils.format_violation_report(HEADER, VIOLATIONS_BY_FILE)
	if lines:
		file_utils.write_report_lines(REPORT_NAME, lines)


#============================================
@pytest.mark.parametrize("path", FILES, ids=file_utils.rel_id)
def test_bash_script_line_limit(path: str) -> None:
	"""Fail when a Bash script reaches 100 lines or 8000 characters."""
	rel = file_utils.rel_to_root(path)
	assert rel not in VIOLATIONS_BY_FILE, file_utils.format_violation_assert_message(
		rel, VIOLATIONS_BY_FILE.get(rel, []), REPORT_NAME
	)
# Vendored pytest file. Local changes can and will be overwritten.
