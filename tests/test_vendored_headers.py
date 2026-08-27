# Standard Library
import os

# PIP3 modules
import pytest

# local repo modules
import file_utils

# Marker pair written by propagation into files it seeds and then refreshes.
# Any file carrying these markers is checked, so a file added to the HEADER
# bucket later is covered here without editing this test.
HEADER_START_MARKER = "<!-- VENDORED HEADER: START -->"
HEADER_END_MARKER = "<!-- VENDORED HEADER: END -->"


#============================================
def marker_lines(lines: list[str]) -> tuple[list[int], list[int]]:
	"""
	Return the line numbers of start and end markers outside fenced code blocks.

	Docs that document the marker convention quote it inside a fence. Those
	quotations are examples, not a header region, so fenced content is skipped
	here and such a file never enters discovery.

	Args:
		lines: All lines of the file.

	Returns:
		tuple[list[int], list[int]]: One-based start and end marker line numbers.
	"""
	starts: list[int] = []
	ends: list[int] = []
	in_fence = False
	for line_number, line in enumerate(lines, 1):
		stripped = line.strip()
		if stripped.startswith("```"):
			in_fence = not in_fence
			continue
		if in_fence:
			continue
		if stripped == HEADER_START_MARKER:
			starts.append(line_number)
		if stripped == HEADER_END_MARKER:
			ends.append(line_number)
	return starts, ends


#============================================
def carries_header_markers(rel: str) -> bool:
	"""
	Select files that carry, or should carry, a vendored header region.

	A file counts when either marker appears outside a fence, so a half-removed
	pair is still checked rather than quietly dropping out of discovery.

	Args:
		rel: Repo-relative POSIX path offered by discovery.

	Returns:
		bool: True when the file carries either marker as content.
	"""
	abs_path = os.path.join(file_utils.get_repo_root(), rel)
	with open(abs_path, "r", encoding="utf-8") as handle:
		lines = handle.read().splitlines()
	starts, ends = marker_lines(lines)
	return bool(starts or ends)


FILES = file_utils.discover_files(
	extensions=(".md",), extra_filter=carries_header_markers, test_key="vendored_headers"
)

REPORT_NAME = file_utils.report_name(__file__)

HEADER = "vendored header violations"

# Module-level dict of repo-relative POSIX key -> list of violation lines.
# Populated by the autouse collect_report fixture before any test runs.
VIOLATIONS_BY_FILE: dict[str, list[str]] = {}


#============================================
def check_file(rel: str) -> list[str]:
	"""
	Check that a file carries exactly one non-empty vendored header region.

	Propagation rewrites this region on every sync and refuses to touch a file
	whose markers are ambiguous, so a damaged pair stays damaged until someone
	notices. This check surfaces that, and the loss of a header from a file that
	was rewritten wholesale.

	Args:
		rel: Repo-relative POSIX path for the file.

	Returns:
		list[str]: Violation lines (empty when the region is well formed).
	"""
	abs_path = os.path.join(file_utils.get_repo_root(), rel)
	with open(abs_path, "r", encoding="utf-8") as handle:
		lines = handle.read().splitlines()
	starts, ends = marker_lines(lines)
	if (len(starts), len(ends)) != (1, 1):
		return [
			f"{rel}: expected one vendored header region "
			f"(start markers {starts}, end markers {ends}); "
			f"run propagation to restore it, or repair the markers by hand"
		]
	if starts[0] > ends[0]:
		return [f"{rel}:{ends[0]}: vendored header end marker precedes its start marker"]
	region = [line for line in lines[starts[0]:ends[0] - 1] if line.strip()]
	if not region:
		return [f"{rel}:{starts[0]}: vendored header region is empty; run propagation to restore it"]
	return []


#============================================
@pytest.fixture(scope="module", autouse=True)
def collect_report() -> None:
	"""
	Autouse fixture: clear stale reports, populate VIOLATIONS_BY_FILE, write report.

	Runs the guarded once-per-process cleanup first, rebuilds the module-level
	violations dict via the shared harness, then writes the report only when there
	are violations.
	"""
	# Once-per-process guarded cleanup of repo-root report_*.txt (no-op after first call).
	file_utils.clear_stale_reports()
	# Clear any state left from a previous collection in the same process.
	VIOLATIONS_BY_FILE.clear()
	VIOLATIONS_BY_FILE.update(file_utils.collect_file_violations(FILES, check_file))
	lines = file_utils.format_violation_report(HEADER, VIOLATIONS_BY_FILE)
	# Write only when there are violations; cleanup already removed stale reports.
	if lines:
		file_utils.write_report_lines(REPORT_NAME, lines)


#============================================
@pytest.mark.parametrize("path", FILES, ids=file_utils.rel_id)
def test_vendored_headers(path: str) -> None:
	"""Fail on a missing, unpaired, reversed, duplicated, or empty header region."""
	rel = file_utils.rel_to_root(path)
	# Python evaluates an assert's message expression ONLY when the assert fails,
	# so format_violation_assert_message runs on the failing path only -- not per pass.
	assert rel not in VIOLATIONS_BY_FILE, file_utils.format_violation_assert_message(
		rel, VIOLATIONS_BY_FILE.get(rel, []), REPORT_NAME
	)
# Vendored pytest file. Local changes can and will be overwritten.
