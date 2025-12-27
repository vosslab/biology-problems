#!/usr/bin/env python3

# Standard Library
import os
import re
import shlex
import subprocess
import sys
import tempfile

CHANGELOG_PATH = "docs/CHANGELOG.md"
VERSION_RE = re.compile(r"^##\s*\[?([^\]\s]+)[^\]]*\]?")

#============================================

def run_git(args: list[str]) -> subprocess.CompletedProcess:
	"""Run a git command and return the completed process."""
	result = subprocess.run(
		["git"] + args,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
		text=True,
	)
	return result

#============================================

def ensure_in_git_repo() -> None:
	"""Raise if not inside a git work tree."""
	result = run_git(["rev-parse", "--is-inside-work-tree"])
	if result.returncode != 0:
		raise RuntimeError("Not inside a git repository.")
	if result.stdout.strip() != "true":
		raise RuntimeError("Not inside a git work tree.")

#============================================

def get_editor_cmd() -> list[str]:
	"""Return the editor command as argv."""
	editor = os.environ.get("GIT_EDITOR") or os.environ.get("EDITOR") or "nano"
	cmd = shlex.split(editor)
	return cmd

#============================================

def edit_file_in_editor(path: str) -> int:
	"""Open a file in the configured editor."""
	cmd = get_editor_cmd() + [path]
	return subprocess.run(cmd).returncode

#============================================

def confirm(prompt: str) -> bool:
	"""Ask the user to confirm."""
	ans = input(prompt).strip().lower()
	return ans in ("y", "yes")

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
	result = run_git(["diff", "--no-color", "--unified=0", "--", path])
	if result.returncode != 0:
		raise RuntimeError(result.stderr.strip() or f"git diff failed for {path}")
	return result.stdout.strip()

#============================================

def extract_added_lines(diff_text: str) -> list[str]:
	"""Extract added lines from a git diff (no headers, no blanks)."""
	added: list[str] = []
	for line in diff_text.splitlines():
		if not line.startswith("+"):
			continue
		if line.startswith("+++"):
			continue
		text = line[1:].rstrip()
		if text.strip() == "":
			continue
		added.append(text)
	return added

#============================================

def build_message(added_lines: list[str], max_body_lines: int) -> str:
	"""Build a subject and body from added changelog lines."""
	version: str | None = None
	for line in added_lines:
		m = VERSION_RE.match(line.strip())
		if m:
			version = m.group(1)
			break

	if version:
		subject = f"docs: update changelog for {version}"
	else:
		subject = "docs: update changelog"

	body_lines: list[str] = []
	for line in added_lines:
		s = line.strip()
		if s.startswith("##"):
			continue
		body_lines.append(s)
		if len(body_lines) >= max_body_lines:
			break

	body = "\n".join(body_lines).strip()
	if body:
		message = subject + "\n\n" + body + "\n"
	else:
		message = subject + "\n"
	return message

#============================================

def make_seed_message() -> str:
	"""Create the initial commit message from the changelog diff."""
	diff_text = get_diff(CHANGELOG_PATH)
	if not diff_text:
		raise RuntimeError(f"No diff for {CHANGELOG_PATH}.")

	added_lines = extract_added_lines(diff_text)
	if not added_lines:
		raise RuntimeError(f"Diff for {CHANGELOG_PATH} had no added lines.")

	message = build_message(added_lines, max_body_lines=25)
	return message

#============================================

def commit_with_editor_gate(seed_message: str) -> int:
	"""Edit the message, confirm, then commit with -a."""
	with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as tf:
		tf.write(seed_message)
		tf.write("\n")
		tf.write("# Save and exit to use this message.\n")
		tf.write("# Exiting without changes will abort by default.\n")
		msg_path = tf.name

	original = strip_git_style_comments(seed_message)

	try:
		rc = edit_file_in_editor(msg_path)
		if rc != 0:
			print("Editor exited non-zero. Aborting.", file=sys.stderr)
			return rc

		with open(msg_path, "r", encoding="utf-8") as f:
			edited_raw = f.read()

		edited = strip_git_style_comments(edited_raw)
		if not edited:
			print("Empty commit message. Aborting.", file=sys.stderr)
			return 2

		if edited == original:
			if not confirm("Message unchanged. Commit anyway? [y/N] "):
				print("Aborted.", file=sys.stderr)
				return 3

		cmd_str = "git commit -a -F " + shlex.quote(msg_path)
		if not confirm(f"Proceed with: {cmd_str} ? [y/N] "):
			print("Aborted.", file=sys.stderr)
			return 4

		return subprocess.run(["git", "commit", "-a", "-F", msg_path]).returncode
	finally:
		os.unlink(msg_path)

#============================================

def main() -> None:
	ensure_in_git_repo()

	seed_message = make_seed_message()
	rc = commit_with_editor_gate(seed_message)
	if rc != 0:
		raise SystemExit(rc)

#============================================

if __name__ == "__main__":
	main()
