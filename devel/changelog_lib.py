# This file is vendored. Local changes can and will be overwritten by propagation.

"""Shared helpers for changelog-oriented developer scripts.

Originally a parser/serializer-only library; expanded by user decision
to absorb the small helper trios (git invocation, console + prompt
primitives) that the three changelog scripts -- devel/commit_changelog.py,
devel/rotate_changelog.py, devel/query_changelog.py -- would otherwise
duplicate. Consolidation into one sibling module is preferred over a
separate git_helpers.py / console_helpers.py to keep moving parts low.

Sections, in order:

- ``# Changelog parsing and serialization`` -- parser API re-exports,
  ``read_changelog`` / ``write_changelog``, ``add_entry`` / ``parse_file``,
  ``newest_date`` / ``find_duplicate_dates``. Parsing implementation lives in
  the focused ``changelog_parse`` companion module.
- ``# Git helpers`` -- ``run_git`` / ``get_git_root`` /
  ``ensure_in_git_repo``.
- ``# Console and prompt helpers`` -- ``build_choice_prompt`` /
  ``confirm`` / ``print_warning`` / ``print_error`` plus the
  module-level ``CONSOLE`` and ``ERR_CONSOLE`` rich consoles they
  print through.

Out of scope (stays in calling scripts): CLI argument parsing,
query-side filtering, and script-specific business logic. Library
parsers return warnings as ``list[str]``, never printed; the caller
controls presentation.

This is a library module: no shebang, no executable bit, no
``if __name__ == '__main__'`` guard.
"""

# Standard Library
import os
import dataclasses
import subprocess

# PIP3 modules
import rich.console

# local repo modules
import changelog_parse

#============================================
#============================================
# Changelog parsing and serialization
#============================================
#============================================

#============================================
# Public parsing API

DATE_RE = changelog_parse.DATE_RE
CATEGORY_RE = changelog_parse.CATEGORY_RE
BULLET_RE = changelog_parse.BULLET_RE
CANONICAL_CATEGORIES = changelog_parse.CANONICAL_CATEGORIES
DayBlock = changelog_parse.DayBlock
Entry = changelog_parse.Entry
_is_valid_iso_date = changelog_parse._is_valid_iso_date
parse_day_blocks = changelog_parse.parse_day_blocks
split_day_block = changelog_parse.split_day_block

#============================================
# File I/O

def read_changelog(path: str) -> str:
	"""Return the full text of a changelog file.

	Args:
		path: Path to the file to read.

	Returns:
		The file contents as a single string.

	Raises:
		FileNotFoundError: When ``path`` does not exist. The caller
			decides whether a missing file is fatal.
	"""
	# open in text mode with explicit utf-8 encoding for cross-platform consistency
	with open(path, "r", encoding="utf-8") as handle:
		text = handle.read()
	return text

#============================================

def write_changelog(path: str, preamble: str, blocks: list) -> None:
	"""Write a changelog file from a preamble and a list of day blocks.

	The day-block ``raw_text`` is preserved byte-for-byte. The final
	file ending is normalized to exactly one trailing newline: zero
	newlines become one; two or more become one; one is left alone.
	No other rewriting is performed.

	Args:
		path: Destination file path.
		preamble: Verbatim text written before the first day block.
		blocks: Ordered list of ``DayBlock`` records whose
			``raw_text`` is written in order.
	"""
	# assemble verbatim: preamble first, then each block's raw text in order
	parts = [preamble]
	for block in blocks:
		parts.append(block.raw_text)
	assembled = "".join(parts)

	# normalize file ending to exactly one trailing newline
	# strip every trailing newline, then add exactly one back
	trimmed = assembled.rstrip("\n")
	normalized = trimmed + "\n"

	# ensure the parent directory exists in case the caller did not pre-create it
	parent = os.path.dirname(path)
	if parent:
		os.makedirs(parent, exist_ok=True)

	with open(path, "w", encoding="utf-8") as handle:
		handle.write(normalized)

#============================================

def _insert_entry_in_day(raw_text: str, category: str, title: str) -> str:
	"""Insert one bullet into a day block while retaining canonical category order."""
	lines = raw_text.splitlines(keepends=True)
	bullet = f"- {title}\n"
	category_found = False
	end_index = len(lines)
	# Find an existing category and the next section boundary so only that
	# category's raw slice is extended.
	for index, line in enumerate(lines):
		match = CATEGORY_RE.match(line)
		if match is None or match.group(1).strip() != category:
			continue
		category_found = True
		for later_index in range(index + 1, len(lines)):
			if CATEGORY_RE.match(lines[later_index]):
				end_index = later_index
				break
		break

	if category_found:
		# Rebuild exactly one canonical separator around the inserted bullet while
		# preserving every adjacent section line.
		prefix = "".join(lines[:end_index]).rstrip("\n")
		last_line = prefix.splitlines()[-1]
		separator = "\n\n" if CATEGORY_RE.match(last_line) else "\n"
		suffix = "".join(lines[end_index:]).lstrip("\n")
		result = prefix + separator + bullet
		if suffix:
			result += "\n" + suffix
		return result

	target_order = CANONICAL_CATEGORIES.index(category)
	insert_index = len(lines)
	# A missing category belongs before the first later canonical category; unknown
	# legacy categories keep their original relative position.
	for index, line in enumerate(lines):
		match = CATEGORY_RE.match(line)
		if match is None:
			continue
		existing_category = match.group(1).strip()
		if existing_category not in CANONICAL_CATEGORIES:
			continue
		if CANONICAL_CATEGORIES.index(existing_category) > target_order:
			insert_index = index
			break
	# Trim only boundary newlines, then restore canonical blank-line separation.
	prefix = "".join(lines[:insert_index]).rstrip("\n")
	suffix = "".join(lines[insert_index:]).lstrip("\n")
	section = f"### {category}\n\n{bullet}"
	result = prefix + "\n\n" + section
	if suffix:
		result += "\n" + suffix
	return result

#============================================

def add_entry(path: str, date_str: str, category: str, title: str) -> None:
	"""Add one canonical changelog bullet, preserving all existing day blocks.

	Args:
		path: Changelog file to update or create.
		date_str: Valid ISO date used for the day heading.
		category: One of CANONICAL_CATEGORIES.
		title: Single-line bullet text without the leading dash.

	Raises:
		ValueError: The new entry is invalid or the changelog contains an invalid
			or duplicated date heading that makes a lossless rewrite unsafe.
	"""
	if not _is_valid_iso_date(date_str):
		raise ValueError(f"invalid changelog date: {date_str!r}")
	if category not in CANONICAL_CATEGORIES:
		raise ValueError(f"non-canonical changelog category: {category!r}")
	normalized_title = title.strip()
	if not normalized_title or "\n" in normalized_title or "\r" in normalized_title:
		raise ValueError("changelog title must be one non-empty line")

	text = read_changelog(path) if os.path.isfile(path) else ""
	preamble, blocks, warnings = parse_day_blocks(
		text, source=path, duplicate_policy="raise",
	)
	invalid_warnings = [warning for warning in warnings if "invalid date" in warning]
	if invalid_warnings:
		raise ValueError(invalid_warnings[0])

	matched = False
	for index, block in enumerate(blocks):
		if block.date != date_str:
			continue
		new_raw_text = _insert_entry_in_day(
			block.raw_text, category, normalized_title,
		)
		blocks[index] = dataclasses.replace(block, raw_text=new_raw_text)
		matched = True
		break
	if not matched:
		new_raw_text = (
			f"## {date_str}\n\n"
			f"### {category}\n\n"
			f"- {normalized_title}\n\n"
		)
		blocks.insert(0, DayBlock(
			date=date_str, raw_text=new_raw_text, source=path, lineno=1,
		))
	if preamble and not preamble.endswith("\n\n"):
		preamble = preamble.rstrip("\n") + "\n\n"
	write_changelog(path, preamble, blocks)

#============================================
# Convenience

def parse_text(text: str, source: str = "<unknown>", strict: bool = False,
		duplicate_policy: str = "warn") -> tuple:
	"""Parse and split a changelog from an in-memory string.

	Same return shape as ``parse_file``. Use this when the source text
	comes from somewhere other than a filesystem path (for example
	``git show <sha>:docs/CHANGELOG.md`` output).

	Args:
		text: Full changelog file contents.
		source: Label used in warning messages and on each resulting
			record. Defaults to ``"<unknown>"``.
		strict: Passed to ``split_day_block``.
		duplicate_policy: Passed to ``parse_day_blocks``.

	Returns:
		A tuple ``(blocks, entries, warnings)``. ``warnings`` is the
		concatenation of the parse-time warnings and every block's
		split-time warnings. Legacy-flat per-block warnings are
		collapsed into a single per-source summary line.

	Raises:
		ValueError: Passthrough from ``parse_day_blocks`` when
			``duplicate_policy='raise'`` and a duplicate
			``## YYYY-MM-DD`` heading is encountered.
	"""
	_preamble, blocks, parse_warnings = parse_day_blocks(
		text, source=source, duplicate_policy=duplicate_policy,
	)
	entries: list = []
	split_warnings: list = []
	for block in blocks:
		block_entries, block_warnings = split_day_block(block, strict=strict)
		entries.extend(block_entries)
		split_warnings.extend(block_warnings)
	# collapse per-block LEGACY_FLAT warnings into one per-file summary line.
	# the dominant corpus shape (94%+ of the old "bullets before any category"
	# warnings) is legacy flat changelogs; surfacing one summary per file keeps
	# signal-to-noise reasonable. Other warning shapes survive untouched.
	legacy_marker = "legacy flat block (no category heading)"
	non_legacy = [w for w in split_warnings if legacy_marker not in w]
	legacy_count = len(split_warnings) - len(non_legacy)
	combined_warnings = parse_warnings + non_legacy
	if legacy_count > 0:
		combined_warnings.append(
			f"{source}: legacy flat changelog: {legacy_count} day blocks have "
			f"bullets with no category heading (treated as Uncategorized)"
		)
	return (blocks, entries, combined_warnings)

#============================================

def parse_file(path: str, strict: bool = False,
		duplicate_policy: str = "warn") -> tuple:
	"""Read, parse, and split a changelog file in a single call.

	Thin wrapper around ``parse_text``: reads ``path``, then delegates.

	Args:
		path: Path to the changelog file.
		strict: Passed to ``split_day_block``.
		duplicate_policy: Passed to ``parse_day_blocks``.

	Returns:
		A tuple ``(blocks, entries, warnings)``. ``warnings`` is the
		concatenation of the parse-time warnings and every block's
		split-time warnings.

	Raises:
		FileNotFoundError: When ``path`` does not exist.
		ValueError: Passthrough from ``parse_day_blocks`` when
			``duplicate_policy='raise'`` and a duplicate
			``## YYYY-MM-DD`` heading is encountered.
	"""
	text = read_changelog(path)
	return parse_text(text, source=path, strict=strict,
		duplicate_policy=duplicate_policy)

#============================================

def newest_date(blocks: list) -> str | None:
	"""Return the date of the first day block, or ``None`` if empty.

	This is a pure inspector: it does not read any file. The caller
	composes ``read_changelog`` + ``parse_day_blocks`` + ``newest_date``
	when archive boundary detection is needed.

	Args:
		blocks: List of ``DayBlock`` records, typically the second
			element of a ``parse_day_blocks`` return tuple.

	Returns:
		The date string of ``blocks[0]`` when ``blocks`` is non-empty,
		otherwise ``None``.
	"""
	if not blocks:
		return None
	first = blocks[0]
	return first.date

#============================================

def find_duplicate_dates(blocks: list) -> list:
	"""Return dates that appear two or more times in ``blocks``.

	The returned list is in input order and deduplicated (a date that
	appears three times is reported once). An empty list signals that
	the input is clean. Used as a preflight by rotation so the script
	never needs ``try/except`` around the parser.

	Args:
		blocks: List of ``DayBlock`` records.

	Returns:
		List of duplicated date strings in input order.
	"""
	seen: set = set()
	dup_set: set = set()
	dup_order: list = []
	for block in blocks:
		date_str = block.date
		if date_str in seen and date_str not in dup_set:
			dup_set.add(date_str)
			dup_order.append(date_str)
			continue
		seen.add(date_str)
	return dup_order

#============================================
#============================================
# Git helpers
#============================================
#============================================
#
# Lifted out of devel/commit_changelog.py, devel/rotate_changelog.py,
# and devel/query_changelog.py to eliminate three-way duplication. All
# three scripts already import this module for parser access; sharing
# the git trio here avoids a separate devel/git_helpers.py module per
# user decision.

def run_git(args: list[str]) -> subprocess.CompletedProcess:
	"""Run a git command and return the completed process.

	Args:
		args: Argument list passed to git (no leading "git" token).

	Returns:
		The ``subprocess.CompletedProcess`` with text-mode stdout/stderr.
	"""
	result = subprocess.run(
		["git"] + args,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
		text=True,
	)
	return result

#============================================

def get_git_root() -> str:
	"""Return the absolute path of the git repository root.

	Returns:
		Absolute path of the git repository root, as reported by
		``git rev-parse --show-toplevel``.

	Raises:
		RuntimeError: When git rev-parse fails or returns an empty path
			(not a git work tree, git binary missing, etc.).
	"""
	result = run_git(["rev-parse", "--show-toplevel"])
	if result.returncode != 0:
		raise RuntimeError("Unable to determine git repository root.")
	root = result.stdout.strip()
	if not root:
		raise RuntimeError("Git repository root is empty.")
	return root

#============================================

def ensure_in_git_repo() -> None:
	"""Raise if the current working directory is not inside a git work tree.

	Raises:
		RuntimeError: When git rev-parse cannot confirm an inside-work-tree
			environment.
	"""
	result = run_git(["rev-parse", "--is-inside-work-tree"])
	if result.returncode != 0:
		raise RuntimeError("Not inside a git repository.")
	if result.stdout.strip() != "true":
		raise RuntimeError("Not inside a git work tree.")

#============================================
#============================================
# Console and prompt helpers
#============================================
#============================================
#
# Lifted out of devel/commit_changelog.py and devel/rotate_changelog.py
# to eliminate duplicated rich-console primitives. The two module-level
# Console instances below are the canonical CONSOLE / ERR_CONSOLE handles
# the helpers below print through; calling scripts that want raw access
# (e.g. CONSOLE.print(...) with their own styles) may either reference
# changelog_lib.CONSOLE directly or keep their own local Console handles.

# highlight=False stops rich from auto-coloring numbers, paths, and
# similar tokens in plain printed text (the "pink lemonade" effect on
# some terminals); markup tags like [bold red] still work because
# markup defaults to True. Per-call markup=False on print_warning /
# print_error keeps literal [brackets] in user-supplied messages from
# being interpreted as markup.
CONSOLE = rich.console.Console(highlight=False)
ERR_CONSOLE = rich.console.Console(stderr=True, highlight=False)

#============================================

def build_choice_prompt(prompt: str) -> str:
	"""Build a colored y/N prompt string.

	Args:
		prompt: Base prompt text.

	Returns:
		The prompt with a colored ``[y/N]`` suffix appended.
	"""
	yes_text = "[bold green]y[/bold green]"
	no_text = "[bold red]N[/bold red]"
	choice_prompt = f"{prompt} [{yes_text}/{no_text}] "
	return choice_prompt

#============================================

def confirm(prompt: str) -> bool:
	"""Ask the user to confirm via a y/N prompt.

	Args:
		prompt: Prompt text shown before the choices.

	Returns:
		True when the answer is ``y`` or ``yes`` (case-insensitive).
	"""
	choice_prompt = build_choice_prompt(prompt)
	ans = CONSOLE.input(choice_prompt).strip().lower()
	confirmed = ans in ("y", "yes")
	return confirmed

#============================================

def print_warning(message: str) -> None:
	"""Print a warning message in yellow on stdout.

	``highlight=False`` and ``markup=False`` keep rich from auto-coloring
	numbers/paths or interpreting ``[brackets]`` in arbitrary user-facing
	text. Matches the unified print-helper convention across devel/.
	"""
	CONSOLE.print(message, style="yellow", highlight=False, markup=False)

#============================================

def print_error(message: str) -> None:
	"""Print an error message in bold red on stderr.

	Same ``highlight=False`` / ``markup=False`` discipline as
	``print_warning``; see that docstring.
	"""
	ERR_CONSOLE.print(message, style="bold red", highlight=False, markup=False)
