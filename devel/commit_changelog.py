#!/usr/bin/env python3
"""Draft and apply a git commit using docs/CHANGELOG.md as the source.

Reads new entries from docs/CHANGELOG.md (parsed via changelog_lib),
selects those dated at or after the last commit that touched the
changelog file, and uses them to build a seed commit message. The
seed is shown in the user's editor for review before the commit is
applied via ``git commit -a -F``. Interactive: prompts on untracked
files, message review, and final commit confirmation.
"""

# Standard Library
import os
import re
import sys
import time
import shlex
import tempfile
import subprocess

# PIP3 modules
import rich.panel

# local repo modules
import changelog_lib

CHANGELOG_PATHSPEC = "docs/CHANGELOG.md"
VERSION_PATHSPEC = "VERSION"
# upper bound on body lines emitted into the seed editor buffer (covers
# date headings, title bullets, and indented continuations together)
MAX_BODY_LINES = 25
# git convention: subject lines wrap at 72 chars; clean_entry_text trims to fit
SUBJECT_BUDGET = 72
# body bullets wrap at ~100 chars for scannability; not a hard git rule
BODY_LINE_BUDGET = 100

#============================================

def read_version_file() -> str:
	"""Read VERSION file relative to repo_root and return stripped contents.

	Returns:
		Stripped contents of the VERSION file.

	Raises:
		RuntimeError: When the VERSION file does not exist or cannot be read.
	"""
	repo_root = changelog_lib.get_git_root()
	version_path = os.path.join(repo_root, VERSION_PATHSPEC)
	try:
		with open(version_path, "r", encoding="utf-8") as f:
			version_contents = f.read().strip()
	except FileNotFoundError:
		raise RuntimeError(f"VERSION file not found at {version_path}.")
	except IOError as e:
		raise RuntimeError(f"Failed to read VERSION file: {e}")
	if not version_contents:
		raise RuntimeError(f"VERSION file is empty: {version_path}.")
	return version_contents

#============================================

def current_calver_month() -> str:
	"""Return the current calendar month in CalVer format (YY.MM).

	Returns:
		Current month as a zero-padded string in the format YY.MM
		(for example "26.05").
	"""
	return time.strftime("%y.%m")

#============================================

def check_version_freshness() -> bool:
	"""Check if VERSION file matches the current calendar month.

	Returns the result of a user confirmation prompt when the month
	does not match. Returns True immediately when the month matches.

	Returns:
		True if VERSION month matches current month or user confirms to continue.
		False if user declines to continue.
	"""
	version_value = read_version_file()
	current_month = current_calver_month()

	# Extract the first two dotted segments (YY.MM)
	version_parts = version_value.split(".")
	if len(version_parts) < 2:
		raise RuntimeError(f"VERSION format unrecognized: {version_value}")
	version_month = f"{version_parts[0]}.{version_parts[1]}"

	# If months match, freshness is confirmed
	if version_month == current_month:
		return True

	# Months don't match; prompt the user
	prompt = f"VERSION is {version_value}, but current month is {current_month}. Continue?"
	return changelog_lib.confirm(prompt)

#============================================

def get_git_status_lines() -> list[str]:
	"""Return git status porcelain output lines.

	Returns:
		List of status lines.
	"""
	result = changelog_lib.run_git(["status", "--porcelain=1"])
	if result.returncode != 0:
		raise RuntimeError(result.stderr.strip() or "git status failed.")
	lines = [line for line in result.stdout.splitlines() if line.strip()]
	return lines

#============================================

def get_untracked_files() -> list[str]:
	"""Return a list of untracked file paths."""
	status_lines = get_git_status_lines()
	untracked: list[str] = []
	for line in status_lines:
		if line.startswith("?? "):
			untracked.append(line[3:])
	return untracked

#============================================

def get_unmerged_paths() -> list[str]:
	"""Return a list of paths with merge conflicts."""
	result = changelog_lib.run_git(["diff", "--name-only", "--diff-filter=U"])
	if result.returncode != 0:
		raise RuntimeError(result.stderr.strip() or "git diff failed.")
	lines = [line for line in result.stdout.splitlines() if line.strip()]
	return lines

#============================================

def format_status_entry(status_code: str, path: str) -> str:
	"""Format a git status entry.

	Args:
		status_code: Single-letter status code.
		path: File path portion.

	Returns:
		Formatted status entry.
	"""
	status_map = {
		"A": "new file",
		"M": "modified",
		"D": "deleted",
		"R": "renamed",
		"C": "copied",
		"U": "unmerged",
	}
	# unknown status codes (T type-change, future git additions, etc.)
	# fall back to showing the raw character so the user sees the
	# actual signal instead of a mislabeled "modified"
	if status_code in status_map:
		label = status_map[status_code]
	else:
		label = f"({status_code})"
	entry = f"{label}: {path}"
	return entry

#============================================

def build_git_status_block() -> str:
	"""Build a git status comment block for the commit message.

	Returns:
		Git status block as a string (may be empty).
	"""
	status_lines = get_git_status_lines()
	if not status_lines:
		return ""

	tracked: list[str] = []
	tracked_seen: set[str] = set()
	untracked: list[str] = []

	for line in status_lines:
		if line.startswith("?? "):
			untracked.append(line[3:])
			continue

		if len(line) < 3:
			continue

		index_status = line[0]
		worktree_status = line[1]
		path = line[3:]

		status_code = worktree_status
		if status_code in (" ", "?"):
			status_code = index_status
		if status_code in (" ", "?"):
			continue
		if path in tracked_seen:
			continue
		tracked_seen.add(path)
		tracked.append(format_status_entry(status_code, path))

	block_lines: list[str] = []
	block_lines.append("#")
	if tracked:
		block_lines.append("# Changes to be committed:")
		for entry in tracked:
			block_lines.append(f"#\t{entry}")

	if untracked:
		block_lines.append("#")
		block_lines.append("# Untracked files:")
		for entry in untracked:
			block_lines.append(f"#\t{entry}")

	block = "\n".join(block_lines).rstrip() + "\n"
	return block

#============================================

def get_editor_cmd() -> list[str]:
	"""Return the editor command as argv.

	Tries ``GIT_EDITOR``, then ``EDITOR``, then falls back to ``nano``.
	Explicit lookup avoids the ``a or b or c`` chain (which would also
	collapse empty strings, hiding a real misconfiguration in those
	env vars).
	"""
	editor = os.environ.get("GIT_EDITOR")
	if not editor:
		editor = os.environ.get("EDITOR")
	if not editor:
		editor = "nano"
	cmd = shlex.split(editor)
	return cmd

#============================================

def edit_file_in_editor(path: str) -> int:
	"""Open a file in the configured editor."""
	cmd = get_editor_cmd() + [path]
	result = subprocess.run(cmd).returncode
	return result

#============================================

def build_action_prompt(prompt: str) -> str:
	"""Build a colored prompt string with yes/no/commit choices.

	Args:
		prompt: Base prompt text.

	Returns:
		The prompt with colored choices appended.
	"""
	yes_text = "[bold green]yes[/bold green]"
	no_text = "[bold red]no[/bold red]"
	commit_text = "[bold cyan]commit[/bold cyan]"
	choice_prompt = f"{prompt} [{yes_text}/{no_text}/{commit_text}] "
	return choice_prompt

#============================================

def prompt_message_action(prompt: str) -> str:
	"""Ask whether to edit, exit, or commit.

	Args:
		prompt: Prompt text shown before the choices.

	Returns:
		One of: "yes", "no", or "commit".
	"""
	choice_prompt = build_action_prompt(prompt)
	while True:
		ans = changelog_lib.CONSOLE.input(choice_prompt).strip().lower()
		if ans == "":
			return "yes"
		if ans in ("y", "yes"):
			return "yes"
		if ans in ("n", "no"):
			return "no"
		if ans in ("c", "commit"):
			return "commit"
		changelog_lib.print_warning("Please enter yes, no, or commit.")

#============================================

def strip_git_style_comments(message: str) -> str:
	"""Remove comment lines (starting with '#'), then trim."""
	out_lines: list[str] = []
	for line in message.splitlines():
		if line.startswith("#"):
			continue
		out_lines.append(line)
	cleaned = "\n".join(out_lines).strip()
	return cleaned

#============================================

def get_diff(path: str) -> str:
	"""Get diff for a path with minimal context and no color."""
	result = changelog_lib.run_git(["diff", "--no-color", "--unified=0", "--", path])
	if result.returncode != 0:
		raise RuntimeError(result.stderr.strip() or f"git diff failed for {path}")
	return result.stdout.strip()

#============================================

def get_cached_diff(path: str) -> str:
	"""Get cached (staged) diff for a path with minimal context and no color."""
	result = changelog_lib.run_git(
		["diff", "--cached", "--no-color", "--unified=0", "--", path]
	)
	if result.returncode != 0:
		raise RuntimeError(result.stderr.strip() or f"git diff --cached failed for {path}")
	return result.stdout.strip()

#============================================

def get_last_changelog_commit_sha() -> str | None:
	"""Return the full SHA of the last commit touching docs/CHANGELOG.md.

	Returns ``None`` when the changelog has no prior commit (first-time
	use).
	"""
	result = changelog_lib.run_git(
		["log", "-1", "--format=%H", "--", CHANGELOG_PATHSPEC]
	)
	if result.returncode != 0:
		raise RuntimeError(result.stderr.strip() or "git log failed.")
	stdout = result.stdout.strip()
	if not stdout:
		return None
	return stdout

#============================================

def get_changelog_text_at(sha: str) -> str:
	"""Return docs/CHANGELOG.md contents at ``sha`` via git show.

	Raises:
		RuntimeError: When git show fails (missing object, shallow
			clone that does not contain the SHA, etc.). The caller
			must not silently fall back to "all entries are new" --
			that would resurrect the bug this helper exists to fix.
	"""
	result = changelog_lib.run_git(
		["show", f"{sha}:{CHANGELOG_PATHSPEC}"]
	)
	if result.returncode != 0:
		raise RuntimeError(
			result.stderr.strip()
			or f"git show failed for {sha}:{CHANGELOG_PATHSPEC}"
		)
	return result.stdout

#============================================

def select_new_entries(prior_sha: str | None) -> tuple[list, list[str]]:
	"""Return entries present in current CHANGELOG but not at ``prior_sha``.

	Replaces the prior date-window filter (which re-emitted bullets that
	had already been committed earlier the same day when the user added
	more bullets under the same ``## YYYY-MM-DD`` heading). Selection
	now diffs the parsed entry set against the entry set in the file at
	the last changelog-touching commit, keyed by ``(date, title)``.

	Args:
		prior_sha: Full SHA of the last commit touching
			docs/CHANGELOG.md, or ``None`` for first-time use.

	Returns:
		A tuple ``(entries, warnings)``. ``entries`` is a list of
		``changelog_lib.Entry`` records in current-file order.
		``warnings`` is the deduplicated list of parser warnings on the
		CURRENT file; prior-file warnings are intentionally suppressed
		(they would re-print stale parse complaints on every commit).
	"""
	_blocks, current_entries, warnings = changelog_lib.parse_file(
		CHANGELOG_PATHSPEC
	)
	# deduplicate warning messages on identical text
	seen: set[str] = set()
	unique_warnings: list[str] = []
	for warning in warnings:
		if warning in seen:
			continue
		seen.add(warning)
		unique_warnings.append(warning)
	if prior_sha is None:
		return (current_entries, unique_warnings)
	prior_text = get_changelog_text_at(prior_sha)
	_p_blocks, prior_entries, _p_warnings = changelog_lib.parse_text(
		prior_text, source=f"{prior_sha[:8]}:{CHANGELOG_PATHSPEC}"
	)
	new_entries = compute_new_entries(current_entries, prior_entries)
	return (new_entries, unique_warnings)

#============================================

def compute_new_entries(current_entries: list, prior_entries: list) -> list:
	"""Return current_entries whose (date, title) is not in prior_entries.

	Preserves current-entry order. Identity key is ``(date, title)``;
	bullets may be rephrased per repo norms, so a title edit looks "new"
	here and the user prunes in the editor buffer.
	"""
	prior_keys: set[tuple[str, str]] = {
		(entry.date, entry.title) for entry in prior_entries
	}
	new_entries = [
		entry for entry in current_entries
		if (entry.date, entry.title) not in prior_keys
	]
	return new_entries

#============================================

def strip_markdown_links(text: str) -> str:
	"""Convert ``[label](url)`` to ``label``."""
	return re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)

#============================================

def strip_markdown_bold(text: str) -> str:
	"""Convert ``**bold**`` and ``__bold__`` to ``bold``."""
	text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
	text = re.sub(r"__([^_]+)__", r"\1", text)
	return text

#============================================

def collapse_whitespace(text: str) -> str:
	"""Collapse runs of whitespace (including newlines) into single spaces."""
	return re.sub(r"\s+", " ", text).strip()

#============================================

def truncate_text(text: str, max_length: int) -> str:
	"""Truncate ``text`` to ``max_length`` chars, appending ``...`` when cut."""
	if len(text) <= max_length:
		return text
	return text[: max_length - 3] + "..."

#============================================

def clean_entry_text(text: str, max_length: int = SUBJECT_BUDGET) -> str:
	"""Strip markdown links, bold, collapse whitespace, then truncate.

	Deterministic; no LLM. Used to format both subject and body lines
	in commit messages built from parsed Entry records.
	"""
	text = strip_markdown_links(text)
	text = strip_markdown_bold(text)
	text = collapse_whitespace(text)
	text = truncate_text(text, max_length)
	return text

#============================================

def make_seed_message_from_entries(entries: list) -> str | None:
	"""Build a seed commit message from parsed Entry records.

	Args:
		entries: List of ``changelog_lib.Entry`` records (already
			date-filtered by ``select_new_entries``).

	Returns:
		The seed message text or ``None`` when entries is empty.
	"""
	if not entries:
		return None

	num_entries = len(entries)
	first_title = entries[0].title

	# subject line: single-entry vs multi-entry shape
	if num_entries == 1:
		subject = clean_entry_text(first_title, SUBJECT_BUDGET)
	else:
		# build the "(+N more)" suffix and re-truncate to SUBJECT_BUDGET
		# so the suffix never gets cut off mid-word
		suffix = f" (+{num_entries - 1} more)"
		head_budget = SUBJECT_BUDGET - len(suffix)
		head = clean_entry_text(first_title, head_budget)
		subject = head + suffix
		subject = truncate_text(subject, SUBJECT_BUDGET)

	# body: group by entry.date with ## YYYY-MM-DD headings when multiple
	# distinct dates are present; cap total emitted body lines.
	distinct_dates: list[str] = []
	seen_dates: set[str] = set()
	for entry in entries:
		if entry.date in seen_dates:
			continue
		seen_dates.add(entry.date)
		distinct_dates.append(entry.date)
	emit_date_headings = len(distinct_dates) > 1

	body_lines: list[str] = []
	# single-entry special case: the subject already states the title, so
	# repeating it as a `- title` bullet is pure noise. Emit only the
	# entry body (when present) as a wrapped paragraph; otherwise no body
	# block at all. Multi-entry seeds keep the bulleted list shape so each
	# entry is individually scannable in the editor buffer.
	if num_entries == 1:
		only_entry = entries[0]
		if only_entry.body:
			body_lines.append(clean_entry_text(only_entry.body, BODY_LINE_BUDGET))
	else:
		for entry in entries:
			if len(body_lines) >= MAX_BODY_LINES:
				break
			if emit_date_headings:
				# entries may arrive interleaved by date; scan all prior body
				# lines (not just the last) to ensure exactly one `## DATE`
				# heading per distinct date across the whole body
				heading = f"## {entry.date}"
				prior_heading_present = any(
					line.startswith(heading) for line in body_lines
				)
				if not prior_heading_present:
					body_lines.append(heading)
					if len(body_lines) >= MAX_BODY_LINES:
						break
			# title line
			title_line = "- " + clean_entry_text(entry.title, BODY_LINE_BUDGET)
			body_lines.append(title_line)
			if len(body_lines) >= MAX_BODY_LINES:
				break
			# body continuation, if present
			if entry.body:
				body_line = "  " + clean_entry_text(entry.body, BODY_LINE_BUDGET)
				body_lines.append(body_line)

	body = "\n".join(body_lines).strip()
	if body:
		message = subject + "\n\n" + body + "\n"
	else:
		message = subject + "\n"
	return message

#============================================

def write_message_file(seed_message: str, include_comments: bool) -> str:
	"""Write a commit message file and return its path.

	Args:
		seed_message: Initial commit message text.
		include_comments: True to include editor guidance and status.

	Returns:
		Path to the message file.
	"""
	with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as tf:
		tf.write(seed_message)
		tf.write("\n")
		if include_comments:
			tf.write("# Save and exit to use this message.\n")
			tf.write("# You will confirm the commit after editing.\n")
			status_block = build_git_status_block()
			if status_block:
				tf.write(status_block)
		return tf.name

#============================================

def edit_message(seed_message: str) -> str | None:
	"""Edit a commit message and return the message file path."""
	msg_path = write_message_file(seed_message, include_comments=True)
	rc = edit_file_in_editor(msg_path)
	if rc != 0:
		changelog_lib.print_error("Editor exited non-zero. Aborting.")
		os.unlink(msg_path)
		return None

	with open(msg_path, "r", encoding="utf-8") as f:
		edited_raw = f.read()

	edited = strip_git_style_comments(edited_raw)
	if not edited:
		changelog_lib.print_error("Empty commit message. Aborting.")
		os.unlink(msg_path)
		return None

	with open(msg_path, "w", encoding="utf-8") as f:
		f.write(edited)
		f.write("\n")

	return msg_path

#============================================

def commit_with_message_file(msg_path: str) -> int:
	"""Commit with a prepared message file."""
	result = subprocess.run(["git", "commit", "-a", "-F", msg_path]).returncode
	return result

#============================================

def main() -> None:
	changelog_lib.ensure_in_git_repo()
	repo_root = changelog_lib.get_git_root()
	os.chdir(repo_root)
	changelog_path = CHANGELOG_PATHSPEC

	unmerged = get_unmerged_paths()
	if unmerged:
		changelog_lib.print_error("Merge conflicts detected. Resolve before committing.")
		for path in unmerged:
			sys.stderr.write(f"  {path}\n")
		return

	untracked = get_untracked_files()
	if untracked:
		sys.stderr.write("Untracked files:\n")
		for path in untracked:
			sys.stderr.write(f"  {path}\n")
		if not changelog_lib.confirm("Keep untracked files untracked?"):
			changelog_lib.print_warning("Aborted.")
			return

	if not check_version_freshness():
		changelog_lib.print_warning("Aborted.")
		return

	# short-circuit on a clean tree before parsing the whole changelog:
	# if there is nothing in the working tree or the index for
	# docs/CHANGELOG.md, there is nothing to commit regardless of which
	# entries the date filter would have picked up.
	diff_text = get_diff(CHANGELOG_PATHSPEC)
	if not diff_text:
		diff_text = get_cached_diff(CHANGELOG_PATHSPEC)
	if not diff_text:
		message = f"No changes in {changelog_path}. Nothing to commit."
		changelog_lib.CONSOLE.print(message, style="yellow")
		return

	# parse-based new-entry selection: build the seed from current entries
	# whose (date, title) does not appear in the changelog at the last
	# commit that touched it. This avoids re-emitting bullets that were
	# already committed earlier the same day when more bullets land under
	# the same ## YYYY-MM-DD heading.
	prior_sha = get_last_changelog_commit_sha()
	new_entries, warnings = select_new_entries(prior_sha)
	# print parse warnings once (deduplicated upstream)
	for warning in warnings:
		changelog_lib.print_warning(warning)

	if not new_entries:
		if prior_sha is None:
			message = f"No entries in {changelog_path}. Nothing to commit."
		else:
			message = (
				f"No new entries since commit {prior_sha[:8]}. "
				"Nothing to commit."
			)
		changelog_lib.CONSOLE.print(message, style="yellow")
		return

	# build the seed message from parsed entries before any preview output
	seed_message = make_seed_message_from_entries(new_entries)
	if seed_message is None:
		return

	# show the seed message in a bordered panel so the editor preview
	# is visually distinct from surrounding console output (warnings,
	# git status, prompts). title="Seed commit message"; rstrip on the
	# panel body to prevent rich from rendering a trailing blank row.
	panel = rich.panel.Panel(
		seed_message.rstrip("\n"),
		title="Seed commit message",
		title_align="left",
		border_style="cyan",
		expand=False,
	)
	changelog_lib.CONSOLE.print(panel, markup=False)

	action = prompt_message_action("Add to the commit message?")
	if action == "no":
		changelog_lib.print_warning("Aborted.")
		return

	if action == "yes":
		msg_path = edit_message(seed_message)
		if msg_path is None:
			return
		if not changelog_lib.confirm("Commit now?"):
			changelog_lib.print_warning("Aborted.")
			os.unlink(msg_path)
			return
		rc = commit_with_message_file(msg_path)
		os.unlink(msg_path)
	elif action == "commit":
		msg_path = write_message_file(seed_message, include_comments=False)
		rc = commit_with_message_file(msg_path)
		os.unlink(msg_path)
	else:
		changelog_lib.print_error("Unknown action. Aborting.")
		return

	if rc != 0:
		raise RuntimeError(f"git commit failed (exit code {rc}).")
	changelog_lib.CONSOLE.print("Reminder: run git pull and git push.", style="yellow")

#============================================

if __name__ == "__main__":
	main()
