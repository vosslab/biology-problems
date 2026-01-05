#!/usr/bin/env python3

import argparse
import datetime
import os
import subprocess


_INCLUDE_ROOTS = (
	"matching_sets",
	"multiple_choice_statements",
	"data",
)

_EXCLUDE_DIR_NAMES = (
	".git",
	".venv",
	"__pycache__",
	"tests",
	"devel",
	"refactor-Jan_2026",
)


def _repo_root() -> str:
	return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _ascii_md(text: str) -> str:
	"""
	Return a strictly-ASCII string suitable for Markdown output.

	- Normalizes common Unicode punctuation to ASCII.
	- Escapes any remaining non-ASCII characters using backslash escapes.
	"""
	text = text.replace("\r", "")
	replacements = {
		"\u2010": "-",  # hyphen
		"\u2011": "-",  # non-breaking hyphen
		"\u2012": "-",  # figure dash
		"\u2013": "-",  # en dash
		"\u2014": "--",  # em dash
		"\u2015": "--",  # horizontal bar
		"\u2212": "-",  # minus sign
		"\u00a0": " ",  # non-breaking space
		"\u2018": "'",  # left single quote
		"\u2019": "'",  # right single quote
		"\u201c": '"',  # left double quote
		"\u201d": '"',  # right double quote
		"\u2026": "...",  # ellipsis
	}
	for src, dst in replacements.items():
		text = text.replace(src, dst)
	return text.encode("ascii", "backslashreplace").decode("ascii")


def _format_date(unix_time: int) -> str:
	return datetime.date.fromtimestamp(unix_time).isoformat()


def _git_head_info(repo_root: str) -> tuple[str, str]:
	short_hash = subprocess.check_output(
		["git", "rev-parse", "--short", "HEAD"],
		cwd=repo_root,
		text=True,
	).strip()
	date = subprocess.check_output(
		["git", "show", "-s", "--format=%cs", "HEAD"],
		cwd=repo_root,
		text=True,
	).strip()
	return short_hash, date


def _worktree_mtime(repo_root: str, rel_path: str) -> tuple[str, int]:
	abs_path = os.path.join(repo_root, rel_path)
	mtime = int(os.path.getmtime(abs_path))
	return ("WORKTREE", mtime)


def _git_last_change(repo_root: str, rel_path: str) -> tuple[str, int] | None:
	try:
		out = subprocess.check_output(
			["git", "log", "--follow", "-1", "--format=%H%x09%at", "--", rel_path],
			cwd=repo_root,
			text=True,
			stderr=subprocess.DEVNULL,
		).strip()
	except subprocess.CalledProcessError:
		return None
	if len(out) == 0:
		return None
	commit_hash, author_time = out.split("\t", 1)
	return commit_hash, int(author_time)


def _git_first_seen(repo_root: str, rel_path: str) -> tuple[str, int] | None:
	def run(args: list[str]) -> str | None:
		try:
			return subprocess.check_output(
				args,
				cwd=repo_root,
				text=True,
				stderr=subprocess.DEVNULL,
			).strip()
		except subprocess.CalledProcessError:
			return None

	# Prefer "add file" commits; take the oldest add.
	out = run(
		[
			"git",
			"log",
			"--follow",
			"--diff-filter=A",
			"--format=%H%x09%at",
			"--",
			rel_path,
		]
	)
	if out:
		last_line = out.splitlines()[-1]
		commit_hash, author_time = last_line.split("\t", 1)
		return commit_hash, int(author_time)

	# Fall back to the oldest commit that touches the file (rename history aware).
	out = run(
		[
			"git",
			"log",
			"--follow",
			"--format=%H%x09%at",
			"--",
			rel_path,
		]
	)
	if out:
		last_line = out.splitlines()[-1]
		commit_hash, author_time = last_line.split("\t", 1)
		return commit_hash, int(author_time)

	return None


def _list_yaml_files(repo_root: str) -> list[str]:
	paths: list[str] = []
	for root_name in _INCLUDE_ROOTS:
		root_path = os.path.join(repo_root, root_name)
		if not os.path.isdir(root_path):
			continue
		for dirpath, dirnames, filenames in os.walk(root_path):
			dirnames[:] = [d for d in dirnames if d not in _EXCLUDE_DIR_NAMES]
			for filename in filenames:
				if not (filename.endswith(".yml") or filename.endswith(".yaml")):
					continue
				abs_path = os.path.join(dirpath, filename)
				if os.path.islink(abs_path):
					continue
				paths.append(os.path.relpath(abs_path, repo_root))
	paths.sort()
	return paths


class YamlBankFile:
	def __init__(self, rel_path: str, created: tuple[str, int], updated: tuple[str, int]):
		self.rel_path = rel_path
		self.created_commit, self.created_time = created
		self.updated_commit, self.updated_time = updated

	@property
	def created_date(self) -> str:
		return _format_date(self.created_time)

	@property
	def updated_date(self) -> str:
		return _format_date(self.updated_time)


def build_index(repo_root: str) -> list[YamlBankFile]:
	entries: list[YamlBankFile] = []
	for rel_path in _list_yaml_files(repo_root):
		first = _git_first_seen(repo_root, rel_path)
		last = _git_last_change(repo_root, rel_path)
		if first is None or last is None:
			worktree = _worktree_mtime(repo_root, rel_path)
			if first is None:
				first = worktree
			if last is None:
				last = worktree
		entries.append(YamlBankFile(rel_path, first, last))

	# newest updates first
	entries.sort(key=lambda e: (e.updated_time, e.rel_path), reverse=True)
	return entries


def write_markdown(repo_root: str, entries: list[YamlBankFile], out_path: str):
	head_hash, head_date = _git_head_info(repo_root)

	lines: list[str] = []
	lines.append("# YAML Question Bank Index")
	lines.append("")
	lines.append("This file lists YAML-driven question banks and their Git dates.")
	lines.append("")
	lines.append("- Source: `tools/build_yaml_question_bank_index.py`")
	lines.append(f"- Git HEAD: `{head_hash}` ({head_date})")
	lines.append("- Updated date source: `git log --follow -1` (author date)")
	lines.append("- Created date source: oldest `git log --follow --diff-filter=A` entry (fallback: oldest `git log --follow`)")
	lines.append("- Uncommitted/untracked files use file mtime (commit `WORKTREE`).")
	lines.append("")

	current_date = None
	for entry in entries:
		if entry.updated_date != current_date:
			current_date = entry.updated_date
			lines.append(f"## {current_date}")

		created_note = f"created {entry.created_date} (commit `{entry.created_commit[:10]}`)"
		updated_note = f"updated {entry.updated_date} (commit `{entry.updated_commit[:10]}`)"
		line = f"- `{entry.rel_path}` - {updated_note} - {created_note}"
		lines.append(_ascii_md(line))

	lines.append("")

	abs_out = os.path.join(repo_root, out_path)
	os.makedirs(os.path.dirname(abs_out), exist_ok=True)
	with open(abs_out, "w", encoding="utf-8") as f:
		ascii_lines = [_ascii_md(line) for line in lines]
		f.write("\n".join(ascii_lines))


def parse_args():
	parser = argparse.ArgumentParser(description="Build an index of YAML question bank files and their dates.")
	parser.add_argument(
		"-o", "--output",
		dest="output",
		default="docs/YAML_QUESTION_BANK_INDEX.md",
		help="Output Markdown path (repo-relative).",
	)
	return parser.parse_args()


def main():
	args = parse_args()
	repo_root = _repo_root()
	entries = build_index(repo_root)
	write_markdown(repo_root, entries, args.output)
	print(f"Wrote {len(entries)} entries to {args.output}")


if __name__ == "__main__":
	main()
