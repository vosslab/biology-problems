# This file is vendored. Local changes can and will be overwritten by propagation.

"""Parse changelog day blocks and entries.

Callers use changelog_lib, which re-exports this module's public records and
parser functions. Keeping parsing here leaves file mutation, Git operations,
and console behavior in changelog_lib.
"""

# Standard Library
import re
import dataclasses


#============================================
# Module constants

# DATE_RE matches structurally well-formed YYYY-MM-DD headings only;
# calendrical validation (e.g. 2026-13-99) is performed in
# parse_day_blocks via datetime.date.fromisoformat().
DATE_RE = re.compile(r"^## (\d{4}-\d{2}-\d{2})\s*$")
CATEGORY_RE = re.compile(r"^###\s+(.+?)\s*$")
BULLET_RE = re.compile(r"^-\s+(.*)$")

CANONICAL_CATEGORIES = [
	"Additions and New Features",
	"Behavior or Interface Changes",
	"Fixes and Maintenance",
	"Removals and Deprecations",
	"Decisions and Failures",
	"Developer Tests and Notes",
]

#============================================
# Dataclasses

@dataclasses.dataclass
class DayBlock:
	"""One ``## YYYY-MM-DD`` day block from a changelog file.

	Attributes:
		date: ISO date string in YYYY-MM-DD form. Calendrically valid
			(passes ``datetime.date.fromisoformat``).
		raw_text: The verbatim slice of the source file, including the
			``## YYYY-MM-DD`` heading line and any trailing newlines
			up to (but not including) the next accepted day heading.
		source: File path the block came from. ``"<unknown>"`` when the
			caller did not supply a source path.
		lineno: 1-based line number of the ``## YYYY-MM-DD`` heading in
			``source``.
		lead_text: Concatenation of non-blank, non-bullet, non-heading
			lines that appear AFTER the ``## YYYY-MM-DD`` heading and
			BEFORE the first ``### Category`` heading or first ``- ``
			bullet. Captures author-attribution lines such as
			``Neil Voss <vossman77@yahoo.com>`` or ``OpenAI Codex``
			that would otherwise be silently dropped by entry-view
			consumers. Empty string when no such line exists. NOT the
			same as the file-level "preamble" returned by
			``parse_day_blocks``, which is text BEFORE the first day
			block.
	"""
	date: str
	raw_text: str
	source: str
	lineno: int
	lead_text: str = ""

#============================================

@dataclasses.dataclass
class Entry:
	"""A single bullet inside a day block.

	Attributes:
		date: ISO date string of the parent day block.
		source: File path of the parent day block.
		category: The ``### Category`` heading the bullet sits under, or
			``"Uncategorized"`` when the bullet appears before any
			category heading.
		title: First line of the bullet, with the leading ``- `` removed
			and trailing whitespace stripped.
		body: Continuation lines joined with ``"\n"``, trailing
			whitespace stripped. Empty string when the bullet is a
			single line.
		text: ``f"{title}. {body}"`` when ``body`` is non-empty,
			otherwise just ``title``. This is the value keyword search
			hits.
		lineno: 1-based line number of the bullet's ``- `` line in
			``source``.
	"""
	date: str
	source: str
	category: str
	title: str
	body: str
	text: str
	lineno: int

#============================================
# Parsing

def _is_valid_iso_date(date_str: str) -> bool:
	"""Return True if ``date_str`` is a calendrically valid YYYY-MM-DD.

	Rejects impossible dates such as ``2026-13-99``. Avoids try/except
	per the repo style guide by validating shape and calendar ranges
	manually.
	"""
	# regex-matched dates are shape-valid YYYY-MM-DD; the only remaining
	# failure mode is calendrical (e.g. month or day out of range).
	# Re-implement the calendar check inline to comply with the
	# no-try/except rule.
	parts = date_str.split("-")
	if len(parts) != 3:
		return False
	year_str, month_str, day_str = parts
	if not (year_str.isdigit() and month_str.isdigit() and day_str.isdigit()):
		return False
	year = int(year_str)
	month = int(month_str)
	day = int(day_str)
	if month < 1 or month > 12:
		return False
	if day < 1 or day > 31:
		return False
	# walk a hardcoded month-length table (with leap-year adjustment for
	# February) so no exception-raising constructor is needed.
	month_lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	# leap-year adjustment for February
	if month == 2:
		is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
		max_day = 29 if is_leap else 28
	else:
		max_day = month_lengths[month - 1]
	if day > max_day:
		return False
	return True

#============================================

def parse_day_blocks(text: str, source: str = "<unknown>",
		duplicate_policy: str = "warn"
		) -> tuple:
	"""Parse changelog text into a preamble and a list of day blocks.

	A day block runs from a ``## YYYY-MM-DD`` heading up to (but not
	including) the next ``## YYYY-MM-DD`` heading or end of file.
	The ``raw_text`` field on each ``DayBlock`` preserves the source
	bytes verbatim, including all trailing newlines.

	Tolerance:

	- A ``## YYYY-MM-DD`` heading that matches ``DATE_RE`` but whose
	  date is calendrically invalid (rejected by
	  ``datetime.date.fromisoformat``) causes the entire block under
	  that heading to be skipped. A warning of the form
	  ``"{source}:{lineno}: invalid date '{date_str}', skipping block"``
	  is appended. A leading bad-date block is folded into the preamble
	  of the first accepted block, because the preamble is defined as
	  "everything before the first accepted heading".
	- ``duplicate_policy='warn'`` (default) keeps the first occurrence
	  of any date and emits a warning of the form
	  ``"{source}:{lineno}: duplicate date '{date_str}', skipping block"``
	  for each later duplicate.
	- ``duplicate_policy='raise'`` raises ``ValueError`` on the first
	  duplicate, naming the date and the duplicate heading lineno.
	- ``duplicate_policy='keep'`` retains every accepted block, including
	  duplicates, without emitting warnings. Suitable for callers that
	  want to detect duplicates themselves via ``find_duplicate_dates``.

	Args:
		text: Full changelog file contents.
		source: File path used in warning messages and on each
			resulting ``DayBlock.source``. Defaults to ``"<unknown>"``.
		duplicate_policy: ``"warn"``, ``"raise"``, or ``"keep"``.

	Returns:
		A tuple ``(preamble, blocks, warnings)`` where ``preamble`` is
		a string, ``blocks`` is a list of ``DayBlock`` records, and
		``warnings`` is a list of warning strings.

	Raises:
		ValueError: When ``duplicate_policy='raise'`` and a duplicate
			date is encountered.
	"""
	# validate the policy argument at the function boundary; this is input
	# validation, not exception-handling business logic
	if duplicate_policy not in ("warn", "raise", "keep"):
		raise ValueError("duplicate_policy must be 'warn', 'raise', or 'keep'")
	warnings: list = []
	# split with keepends so each line carries its own newline character;
	# joining preserves the original file bytes
	lines = text.splitlines(keepends=True)

	# first pass: find heading positions so we can carve raw_text slices
	# each entry: (lineno_1based, date_str, is_valid_iso)
	heading_positions: list = []
	for index, line in enumerate(lines):
		match = DATE_RE.match(line)
		if not match:
			continue
		date_str = match.group(1)
		lineno = index + 1
		is_valid = _is_valid_iso_date(date_str)
		heading_positions.append((lineno, date_str, is_valid, index))

	# if no headings at all, the entire file is preamble
	if not heading_positions:
		preamble = "".join(lines)
		return (preamble, [], warnings)

	# find the line_index of the first accepted (valid-date) heading; the
	# preamble spans every line before that heading
	first_accepted_index = None
	for pos in heading_positions:
		hp_lineno, hp_date, hp_valid, hp_line_index = pos
		if hp_valid:
			first_accepted_index = hp_line_index
			break

	if first_accepted_index is None:
		# no accepted headings at all: every heading is bad-date; whole file is preamble
		preamble = "".join(lines)
		# emit a warning for each bad heading
		for bad_pos in heading_positions:
			bad_lineno, bad_date_str, bad_valid, bad_line_index = bad_pos
			warning = f"{source}:{bad_lineno}: invalid date '{bad_date_str}', skipping block"
			warnings.append(warning)
		return (preamble, [], warnings)

	preamble = "".join(lines[:first_accepted_index])

	# build blocks, walking heading positions and slicing raw_text up to the
	# next heading (good or bad)
	blocks: list = []
	seen_dates: dict = {}
	# precompute total line count for the trailing-slice case
	total = len(lines)
	for hp_idx, pos in enumerate(heading_positions):
		lineno, date_str, is_valid, line_index = pos
		# end of slice: next heading's line_index, or total
		if hp_idx + 1 < len(heading_positions):
			end_index = heading_positions[hp_idx + 1][3]
		else:
			end_index = total
		# skip headings whose date is before the first accepted heading;
		# their text already lives in the preamble
		if line_index < first_accepted_index:
			# emit a warning for the bad-date heading (the text is in preamble)
			warning = f"{source}:{lineno}: invalid date '{date_str}', skipping block"
			warnings.append(warning)
			continue
		if not is_valid:
			# bad-date block in the middle or end: discard the slice entirely
			warning = f"{source}:{lineno}: invalid date '{date_str}', skipping block"
			warnings.append(warning)
			continue
		# duplicate detection on accepted (valid-date) headings only
		if date_str in seen_dates:
			if duplicate_policy == "raise":
				raise ValueError(
					f"duplicate date '{date_str}' at {source}:{lineno} "
					f"(first seen at line {seen_dates[date_str]})"
				)
			if duplicate_policy == "warn":
				# warn policy: append warning and skip this block
				warning = f"{source}:{lineno}: duplicate date '{date_str}', skipping block"
				warnings.append(warning)
				continue
			# keep policy: fall through and append the duplicate block
		else:
			seen_dates[date_str] = lineno
		raw_text = "".join(lines[line_index:end_index])
		# compute lead_text: non-blank, non-bullet, non-heading lines between
		# the ## heading (lines[line_index]) and the first ### or - line. This
		# captures author-attribution day-block annotations that would
		# otherwise be silently dropped by entry-view consumers.
		lead_text_parts: list = []
		for scan_idx in range(line_index + 1, end_index):
			scan_line = lines[scan_idx]
			if BULLET_RE.match(scan_line) or CATEGORY_RE.match(scan_line):
				break
			if DATE_RE.match(scan_line):
				break
			scan_stripped = scan_line.strip()
			if scan_stripped:
				lead_text_parts.append(scan_stripped)
		lead_text = "\n".join(lead_text_parts)
		if lead_text:
			# excerpt: first line only, truncated, for the warning preview
			first_line = lead_text.split("\n", 1)[0]
			excerpt = first_line if len(first_line) <= 80 else first_line[:77] + "..."
			warning = (
				f"{source}:{lineno}: lead text under day heading: "
				f"{excerpt}"
			)
			warnings.append(warning)
		block = DayBlock(
			date=date_str, raw_text=raw_text, source=source, lineno=lineno,
			lead_text=lead_text,
		)
		blocks.append(block)

	return (preamble, blocks, warnings)

#============================================

def split_day_block(block: DayBlock, strict: bool = False) -> tuple:
	"""Split one ``DayBlock`` into ``Entry`` records.

	Walks the block's raw text and emits one ``Entry`` per ``- ``
	bullet. Bullets are grouped by the most recent ``### Category``
	heading; bullets that appear before any category heading are
	classified ``"Uncategorized"``.

	Two warning shapes are emitted, at most one per block:

	- ``LEGACY_FLAT`` -- ``"legacy flat block (no category heading)"``
	  fires once when the block contains zero ``### Category`` headings
	  AND at least one bullet. ``parse_file`` post-processes these into
	  a single per-file summary line.
	- ``ORPHAN_BULLETS`` -- ``"orphan bullets before first category
	  heading"`` fires once when the block has at least one ``###``
	  heading but a bullet appears before the first one. Per-block
	  actionable; never collapsed.

	The third warning shape (``"lead text under day heading"``) is
	emitted by ``parse_day_blocks`` when it captures ``DayBlock.lead_text``;
	this function does not emit it.

	Bullet body collection rule: a bullet starts at a line matching
	``BULLET_RE``. Continuation lines belong to the bullet if they
	are indented (start with whitespace) or blank. A new bullet
	(``- `` at column 0), a new ``### `` heading, or a new ``## ``
	heading ends the current bullet.

	Args:
		block: The ``DayBlock`` to split.
		strict: When True, emit a warning for any category heading
			that is not in ``CANONICAL_CATEGORIES``.

	Returns:
		A tuple ``(entries, warnings)`` where ``entries`` is a list
		of ``Entry`` records (in source order) and ``warnings`` is a
		list of warning strings.
	"""
	warnings: list = []
	entries: list = []

	# split into lines without keepends; we are emitting structured data, not bytes
	raw_lines = block.raw_text.splitlines()

	# pre-scan: count categories and find first-category vs first-bullet positions
	# so we can decide which uncategorized warning shape (if any) to emit
	pre_first_cat_idx = None
	pre_first_bullet_idx = None
	pre_cat_count = 0
	for pre_idx, pre_line in enumerate(raw_lines):
		if pre_idx == 0 and DATE_RE.match(pre_line):
			continue
		if CATEGORY_RE.match(pre_line):
			pre_cat_count += 1
			if pre_first_cat_idx is None:
				pre_first_cat_idx = pre_idx
		elif BULLET_RE.match(pre_line):
			if pre_first_bullet_idx is None:
				pre_first_bullet_idx = pre_idx

	# state machine: current_category, current_bullet
	current_category: str | None = None
	bullet_title: str | None = None
	bullet_body_lines: list = []
	bullet_lineno: int = 0
	uncategorized_warned = False

	# the block's ## heading is raw_lines[0]; bullets and ### headings begin at
	# raw_lines[1]; file lineno for raw_lines[offset] is block.lineno + offset
	def flush_bullet(title: str | None, body_lines: list, lineno: int) -> None:
		"""Build and append an Entry from the bullet state. Returns nothing."""
		if title is None:
			return
		# strip trailing whitespace on the joined body, preserve internal whitespace
		body_joined = "\n".join(body_lines)
		body = body_joined.rstrip()
		if body:
			text = f"{title}. {body}"
		else:
			text = title
		entry = Entry(
			date=block.date,
			source=block.source,
			category=current_category if current_category is not None else "Uncategorized",
			title=title,
			body=body,
			text=text,
			lineno=lineno,
		)
		entries.append(entry)

	for offset, line in enumerate(raw_lines):
		file_lineno = block.lineno + offset

		# the ## heading itself is skipped from entry collection
		if offset == 0 and DATE_RE.match(line):
			continue

		cat_match = CATEGORY_RE.match(line)
		if cat_match:
			# flush any pending bullet before switching category
			flush_bullet(bullet_title, bullet_body_lines, bullet_lineno)
			bullet_title = None
			bullet_body_lines = []
			heading = cat_match.group(1).strip()
			current_category = heading
			if strict and heading not in CANONICAL_CATEGORIES:
				warnings.append(
					f"{block.source}:{file_lineno}: non-canonical category '{heading}'"
				)
			continue

		bullet_match = BULLET_RE.match(line)
		if bullet_match:
			# flush previous bullet
			flush_bullet(bullet_title, bullet_body_lines, bullet_lineno)
			bullet_title = bullet_match.group(1).rstrip()
			bullet_body_lines = []
			bullet_lineno = file_lineno
			# emit a single per-block uncategorized warning at the first such bullet.
			# warning text depends on whether ANY ### Category exists in the block:
			#   - zero categories -> LEGACY_FLAT (collapsed per-file by parse_file)
			#   - at least one category -> ORPHAN_BULLETS (per-block actionable)
			if current_category is None and not uncategorized_warned:
				uncategorized_warned = True
				if pre_cat_count == 0:
					warnings.append(
						f"{block.source}:{block.lineno}: "
						f"legacy flat block (no category heading)"
					)
				else:
					warnings.append(
						f"{block.source}:{block.lineno}: "
						f"orphan bullets before first category heading"
					)
			continue

		# continuation candidate for the current bullet
		if bullet_title is None:
			# nothing to attach to; skip
			continue

		# blank line: soft separator inside the bullet body
		stripped = line.strip()
		if stripped == "":
			bullet_body_lines.append("")
			continue

		# indented continuation: append the stripped form
		if line.startswith(" ") or line.startswith("\t"):
			bullet_body_lines.append(stripped)
			continue

		# non-indented, non-bullet, non-heading content terminates the bullet
		flush_bullet(bullet_title, bullet_body_lines, bullet_lineno)
		bullet_title = None
		bullet_body_lines = []

	# flush a trailing bullet at end of block
	flush_bullet(bullet_title, bullet_body_lines, bullet_lineno)
	return (entries, warnings)
