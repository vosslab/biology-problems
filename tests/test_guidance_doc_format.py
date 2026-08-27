# Standard Library
import os
import re

# PIP3 modules
import pytest

# local repo modules
import file_utils

# Marker pair written by propagation. Keep these strings in step with the
# template's vendored headers.
HEADER_START_MARKER = "<!-- VENDORED HEADER: START -->"
HEADER_END_MARKER = "<!-- VENDORED HEADER: END -->"

GUIDANCE_DOC = "docs/HUMAN_GUIDANCE.md"
DECISIONS_DOC = "docs/DESIGN_DECISIONS.md"
HEADER_DOCS = (GUIDANCE_DOC, DECISIONS_DOC)

# Maximum physical lines in one HUMAN_GUIDANCE bullet, per docs/REPO_STYLE.md.
# A bullet that runs longer has usually stopped being a stated preference and
# become an agent's explanation of one.
MAX_BULLET_LINES = 3

# Fields every DESIGN_DECISIONS entry carries. Entries may add more (a consequence,
# an owner, a planned closure); these two are what make an entry a decision.
REQUIRED_DECISION_FIELDS = ("**Decision.**", "**Why.**")

# An ordered-list item, which counts as an entry the same way a bullet does.
ORDERED_ITEM_PATTERN = re.compile(r"^\d+\.\s")

# Closing prompt on a HUMAN_GUIDANCE failure. The formatting rules are a proxy for
# the real question, so the failure asks it directly: length and prose are how
# agent narration gives itself away.
PROVENANCE_PROMPT = (
	"-> are we sure this guidance came from the human, and not from an agent or an "
	"LLM reviewer? Long prose usually means it did not. Keep what the human said "
	f"here in his own words as short bullets, and record the reasoning in {DECISIONS_DOC}. "
	f"Rearrange aggressively: when a line's origin is uncertain, move it to {DECISIONS_DOC}."
)


#============================================
def keep_header_docs(rel: str) -> bool:
	"""
	Select the two consumer-owned docs that carry a vendored header.

	Args:
		rel: Repo-relative POSIX path offered by discovery.

	Returns:
		bool: True when the path is one of the header-carrying docs.
	"""
	return rel in HEADER_DOCS


FILES = file_utils.discover_files(
	extensions=(".md",), extra_filter=keep_header_docs, test_key="guidance_doc_format"
)

REPORT_NAME = file_utils.report_name(__file__)

HEADER = "guidance doc format violations"

# Module-level dict of repo-relative POSIX key -> list of violation lines.
# Populated by the autouse collect_report fixture before any test runs.
VIOLATIONS_BY_FILE: dict[str, list[str]] = {}


#============================================
def read_lines(rel: str) -> list[str]:
	"""
	Read a doc's lines from its repo-relative path.

	Args:
		rel: Repo-relative POSIX path for the doc.

	Returns:
		list[str]: Lines without line endings.
	"""
	abs_path = os.path.join(file_utils.get_repo_root(), rel)
	with open(abs_path, "r", encoding="utf-8") as handle:
		text = handle.read()
	return text.splitlines()


#============================================
def body_lines(lines: list[str]) -> list[tuple[int, str]]:
	"""
	Return the doc's own entries: line numbers paired with text.

	Drops the vendored header region, which propagation owns, and fenced code
	blocks, whose contents are examples rather than entries. The seeded stub keeps
	its entry skeleton inside a fence for exactly that reason.

	Args:
		lines: All lines of the doc.

	Returns:
		list[tuple[int, str]]: One-based line numbers paired with their text.
	"""
	numbered: list[tuple[int, str]] = []
	in_header = False
	in_fence = False
	for line_number, line in enumerate(lines, 1):
		stripped = line.strip()
		if stripped == HEADER_START_MARKER:
			in_header = True
			continue
		if stripped == HEADER_END_MARKER:
			in_header = False
			continue
		if stripped.startswith("```"):
			in_fence = not in_fence
			continue
		if in_header or in_fence:
			continue
		numbered.append((line_number, line))
	return numbered


#============================================
def gather_bullets(numbered: list[tuple[int, str]]) -> list[tuple[int, list[str]]]:
	"""
	Group body lines into bullets, each with its continuation lines.

	A bullet starts at a `- ` or `* ` line and absorbs following continuation lines
	until a blank line, a heading, or the next bullet.

	Args:
		numbered: Body lines with their line numbers.

	Returns:
		list[tuple[int, list[str]]]: Starting line number and lines of each bullet.
	"""
	bullets: list[tuple[int, list[str]]] = []
	start_line = 0
	current: list[str] = []
	for line_number, line in numbered:
		stripped = line.strip()
		# A blank line or a heading closes the open bullet.
		if not stripped or stripped.startswith("#"):
			if current:
				bullets.append((start_line, current))
				current = []
			continue
		# A new bullet closes the previous one and opens its own.
		if stripped.startswith("- ") or stripped.startswith("* "):
			if current:
				bullets.append((start_line, current))
			start_line = line_number
			current = [line]
			continue
		# Any other line continues an open bullet; prose outside a bullet is
		# not a bullet and is left alone here.
		if current:
			current.append(line)
	if current:
		bullets.append((start_line, current))
	return bullets


#============================================
def gather_decision_entries(numbered: list[tuple[int, str]]) -> list[tuple[int, str, list[str]]]:
	"""
	Group body lines into decision entries, one per level-three heading.

	Args:
		numbered: Body lines with their line numbers.

	Returns:
		list[tuple[int, str, list[str]]]: Line number, heading text, and body lines
			of each entry.
	"""
	entries: list[tuple[int, str, list[str]]] = []
	start_line = 0
	heading = ""
	current: list[str] = []
	for line_number, line in numbered:
		stripped = line.strip()
		# A level-three heading opens a new entry; a shallower heading closes one.
		if stripped.startswith("### "):
			if heading:
				entries.append((start_line, heading, current))
			start_line = line_number
			heading = stripped[4:].strip()
			current = []
			continue
		if stripped.startswith("## ") or stripped.startswith("# "):
			if heading:
				entries.append((start_line, heading, current))
				heading = ""
				current = []
			continue
		if heading:
			current.append(line)
	if heading:
		entries.append((start_line, heading, current))
	return entries


#============================================
def check_guidance_bullets(rel: str, lines: list[str]) -> list[str]:
	"""
	Check that HUMAN_GUIDANCE bullets keep the human's own short shape.

	A bullet that runs long has usually stopped being a stated preference and
	become an agent's explanation of one, which belongs in DESIGN_DECISIONS.md.

	Args:
		rel: Repo-relative POSIX path for the doc.
		lines: All lines of the doc.

	Returns:
		list[str]: Violation lines (empty when every bullet fits).
	"""
	violations = []
	for start_line, block in gather_bullets(body_lines(lines)):
		if len(block) <= MAX_BULLET_LINES:
			continue
		opening = block[0].strip()[:60]
		violations.append(
			f"{rel}:{start_line}: bullet runs {len(block)} lines "
			f"(limit {MAX_BULLET_LINES}): {opening}"
		)
	return violations


#============================================
def check_guidance_is_bulleted(rel: str, lines: list[str]) -> list[str]:
	"""
	Check that entries under a section are bullets rather than prose paragraphs.

	This is the sharpest honesty signal available in formatting. Across the local
	corpus, files that kept the human's terse statements run 0 to 7 percent prose,
	while files an agent expanded run 19 to 100 percent. A paragraph under a
	section heading is nearly always the agent narrating; the preference it was
	built from belongs here as a bullet, and the narration belongs in
	DESIGN_DECISIONS.md.

	Prose above the first section heading is left alone: that is where a repository
	states its own scope note.

	Args:
		rel: Repo-relative POSIX path for the doc.
		lines: All lines of the doc.

	Returns:
		list[str]: Violation lines (empty when every entry is a bullet).
	"""
	violations = []
	in_section = False
	in_bullet = False
	reported_line = 0
	for line_number, line in body_lines(lines):
		stripped = line.strip()
		if stripped.startswith('## '):
			in_section = True
			in_bullet = False
			continue
		if stripped.startswith('#'):
			in_bullet = False
			continue
		# A blank line alone does not close a bullet: Markdown allows a bullet to
		# carry a blank-line-separated continuation, and the indent on the next
		# line is what actually says whether the bullet continued.
		if not stripped:
			continue
		if stripped.startswith('- ') or stripped.startswith('* '):
			in_bullet = True
			continue
		# Ordered-list items are entries too.
		if ORDERED_ITEM_PATTERN.match(stripped):
			in_bullet = True
			continue
		# An indented line continues the bullet above it, blank line or not.
		if in_bullet and line.startswith((' ', '\t')):
			continue
		# Table rows are structure, not narration.
		if stripped.startswith('|'):
			in_bullet = False
			continue
		# Anything else under a section heading is a prose paragraph.
		if in_section:
			in_bullet = False
			# Report the paragraph once, at its opening line.
			if reported_line != line_number - 1:
				violations.append(
					f"{rel}:{line_number}: prose paragraph under a section: {stripped[:60]}"
				)
			reported_line = line_number
	return violations


#============================================
def check_decision_entries(rel: str, lines: list[str]) -> list[str]:
	"""
	Check that every DESIGN_DECISIONS entry states its decision and its reason.

	Args:
		rel: Repo-relative POSIX path for the doc.
		lines: All lines of the doc.

	Returns:
		list[str]: Violation lines (empty when every entry carries its fields).
	"""
	violations = []
	for start_line, heading, block in gather_decision_entries(body_lines(lines)):
		body_text = "\n".join(block)
		missing = [field for field in REQUIRED_DECISION_FIELDS if field not in body_text]
		if not missing:
			continue
		violations.append(
			f"{rel}:{start_line}: entry {heading!r} is missing {', '.join(missing)}"
		)
	return violations


#============================================
def check_file(rel: str) -> list[str]:
	"""
	Run the entry-formatting checks for one doc.

	The rules differ per file because the two have deliberately different shapes:
	HUMAN_GUIDANCE.md holds short bullets in the human's own words, while
	DESIGN_DECISIONS.md holds one bold-field entry per decision. Section names are
	left alone; they differ per repository.

	The vendored header region itself is checked by tests/test_vendored_headers.py,
	which covers every file the HEADER bucket touches. Here the region is only
	skipped over, so its wording never counts as an entry.

	Args:
		rel: Repo-relative POSIX path for the doc.

	Returns:
		list[str]: Violation lines (empty when the doc is clean).
	"""
	lines = read_lines(rel)
	violations: list[str] = []
	if rel == GUIDANCE_DOC:
		violations.extend(check_guidance_bullets(rel, lines))
		violations.extend(check_guidance_is_bulleted(rel, lines))
		# Close a guidance failure with the question the formatting rules stand in
		# for. It rides on the last violation rather than becoming its own entry,
		# so the reported violation count stays accurate.
		if violations:
			violations[-1] = f"{violations[-1]}\n  {PROVENANCE_PROMPT}"
	if rel == DECISIONS_DOC:
		violations.extend(check_decision_entries(rel, lines))
	return violations


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
def test_guidance_doc_format(path: str) -> None:
	"""Fail on a damaged vendored header or an entry that breaks the doc's shape."""
	rel = file_utils.rel_to_root(path)
	# Python evaluates an assert's message expression ONLY when the assert fails,
	# so format_violation_assert_message runs on the failing path only -- not per pass.
	assert rel not in VIOLATIONS_BY_FILE, file_utils.format_violation_assert_message(
		rel, VIOLATIONS_BY_FILE.get(rel, []), REPORT_NAME
	)
# Vendored pytest file. Local changes can and will be overwritten.
