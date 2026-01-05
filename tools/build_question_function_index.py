#!/usr/bin/env python3

import argparse
import ast
import datetime
import os
import re
import subprocess
from dataclasses import dataclass


_INCLUDE_DIR_NAMES = ()

_EXCLUDE_DIR_NAMES = (
	".git",
	".venv",
	"__pycache__",
	"tests",
	"devel",
	"refactor-Jan_2026",
)


_NAME_PREFIXES = (
	"write_question",
)

_NAME_EXACT = {
	"writeQuestion",
	"write_question_batch",
	"writeProblem",
	"makeQuestion",
	"makeQuestions",
	"makeQuestions2",
	"makeQuestionsFromStatement",
	"makeCompleteQuestion",
	"makeFillInBlankQuestion",
	"makeMultipleChoiceQuestion",
	"permuteMatchingPairs",
	"sortStatements",
	"build_every_statement_items",
	"mc_part_block",
	"single_question_pg",
	"write_pg_multi",
	"write_pg_one_per_file",
}


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


def _repo_root() -> str:
	return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _list_target_py_files(repo_root: str) -> list[str]:
	roots: list[str] = []

	# Preferred layout: all domain generators live under `problems/*-problems/`.
	problems_root = os.path.join(repo_root, "problems")
	if os.path.isdir(problems_root):
		for name in os.listdir(problems_root):
			if name in _INCLUDE_DIR_NAMES or name.endswith("-problems"):
				roots.append(os.path.join(problems_root, name))
	else:
		# Backward-compatible layout: `*-problems/` at repo root.
		for name in os.listdir(repo_root):
			if name in _INCLUDE_DIR_NAMES:
				roots.append(os.path.join(repo_root, name))
				continue
			if name.endswith("-problems"):
				roots.append(os.path.join(repo_root, name))

	paths: list[str] = []
	for root in roots:
		for dirpath, dirnames, filenames in os.walk(root):
			dirnames[:] = [d for d in dirnames if d not in _EXCLUDE_DIR_NAMES]
			for filename in filenames:
				if not filename.endswith(".py"):
					continue
				abs_path = os.path.join(dirpath, filename)
				if os.path.islink(abs_path):
					# Many subfolders contain symlink shims (e.g. bptools.py -> ../bptools.py).
					# Skip them to avoid duplicate entries and incorrect git blame/log results.
					continue
				paths.append(abs_path)
	paths.sort()
	return paths


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


def _git_blame_porcelain(repo_root: str, rel_path: str) -> dict[int, tuple[str, int]]:
	"""
	Return final_line -> (commit_hash, author_time_unix).
	"""
	try:
		out = subprocess.check_output(
			["git", "blame", "--follow", "-M", "-C", "--line-porcelain", "--", rel_path],
			cwd=repo_root,
			text=True,
			stderr=subprocess.DEVNULL,
		)
	except subprocess.CalledProcessError:
		return {}

	line_to_info: dict[int, tuple[str, int]] = {}
	current_hash: str | None = None
	current_final_line: int | None = None
	current_author_time: int | None = None

	for line in out.splitlines():
		parts = line.split()
		if len(parts) >= 3 and re.fullmatch(r"[0-9a-f]{7,40}", parts[0] or ""):
			# Header line formats include:
			#   <hash> <orig_line> <final_line> <group_len>
			#   <hash> <orig_line> <final_line>
			try:
				current_hash = parts[0]
				current_final_line = int(parts[2])
				current_author_time = None
				continue
			except ValueError:
				pass

		if line.startswith("author-time "):
			current_author_time = int(line.split()[1])
			continue

		if line.startswith("\t"):
			if current_hash is None or current_final_line is None or current_author_time is None:
				continue
			line_to_info[current_final_line] = (current_hash, current_author_time)

	return line_to_info


def _format_date(unix_time: int) -> str:
	return datetime.date.fromtimestamp(unix_time).isoformat()


_git_first_def_appearance_cache: dict[tuple[str, str], tuple[str, int] | None] = {}
_git_file_birth_cache: dict[str, tuple[str, int] | None] = {}


def _git_first_def_appearance(repo_root: str, rel_path: str, fn_name: str) -> tuple[str, int] | None:
	"""
	Return (commit_hash, author_time_unix) for the first commit that introduces a
	`def <fn_name>` line in `rel_path`, following renames.
	"""
	cache_key = (rel_path, fn_name)
	if cache_key in _git_first_def_appearance_cache:
		return _git_first_def_appearance_cache[cache_key]

	# Use POSIX character classes because `git log -G` uses the diff regex engine.
	# Avoid `\b`/PCRE features; require a non-identifier character after the name.
	pattern = rf"^[[:space:]]*def[[:space:]]+{re.escape(fn_name)}[^[:alnum:]_]"
	try:
		out = subprocess.check_output(
			[
				"git",
				"log",
				"--follow",
				"-M",
				"-C",
				"--reverse",
				"--format=%H%x09%at",
				"-G",
				pattern,
				"--",
				rel_path,
			],
			cwd=repo_root,
			text=True,
			stderr=subprocess.DEVNULL,
		).strip()
	except subprocess.CalledProcessError:
		_git_first_def_appearance_cache[cache_key] = None
		return None

	if len(out) == 0:
		_git_first_def_appearance_cache[cache_key] = None
		return None

	first_line = out.splitlines()[0]
	commit_hash, author_time = first_line.split("\t", 1)
	result = (commit_hash, int(author_time))
	_git_first_def_appearance_cache[cache_key] = result
	return result


def _git_file_birth(repo_root: str, rel_path: str) -> tuple[str, int] | None:
	"""
	Return (commit_hash, author_time_unix) for the commit that first adds the file
	in its rename history (`git log --follow --diff-filter=A`).
	"""
	if rel_path in _git_file_birth_cache:
		return _git_file_birth_cache[rel_path]

	def _run(args: list[str]) -> str | None:
		try:
			return subprocess.check_output(
				args,
				cwd=repo_root,
				text=True,
				stderr=subprocess.DEVNULL,
			).strip()
		except subprocess.CalledProcessError:
			return None

	# Prefer true file birth (commit that adds the file in its rename history).
	#
	# Note: `git log --follow --reverse --diff-filter=A ...` can unexpectedly return
	# empty output for some rename histories; use default ordering and take the
	# oldest "A" commit instead.
	out = _run(
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
		result = (commit_hash, int(author_time))
		_git_file_birth_cache[rel_path] = result
		return result

	# Some clones/history shapes don't contain an explicit "add" commit for the file
	# (e.g., history truncation or file already present when history begins). Fall back
	# to the oldest commit that touches the file, following renames.
	out = _run(
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
		result = (commit_hash, int(author_time))
		_git_file_birth_cache[rel_path] = result
		return result

	_git_file_birth_cache[rel_path] = None
	return None


def _worktree_mtime(repo_root: str, rel_path: str) -> tuple[str, int]:
	abs_path = os.path.join(repo_root, rel_path)
	mtime = int(os.path.getmtime(abs_path))
	return ("WORKTREE", mtime)


def _calls_format_bb(fn_node: ast.AST) -> bool:
	for node in ast.walk(fn_node):
		if not isinstance(node, ast.Call):
			continue
		func = node.func
		if isinstance(func, ast.Attribute):
			if func.attr.startswith("formatBB_"):
				return True
			if isinstance(func.value, ast.Name) and func.value.id == "bptools" and func.attr.startswith("formatBB_"):
				return True
		elif isinstance(func, ast.Name):
			if func.id.startswith("formatBB_"):
				return True
	return False


def _is_question_function_name(name: str) -> bool:
	if name in _NAME_EXACT:
		return True
	for prefix in _NAME_PREFIXES:
		if name.startswith(prefix):
			return True
	return False


@dataclass(frozen=True)
class QuestionFunction:
	rel_path: str
	qualname: str
	lineno: int
	date: str
	commit: str
	file_date: str
	file_commit: str
	doc: str | None


def _extract_question_functions(repo_root: str, rel_path: str) -> list[QuestionFunction]:
	abs_path = os.path.join(repo_root, rel_path)
	with open(abs_path, "r", encoding="utf-8") as f:
		source = f.read()

	try:
		tree = ast.parse(source, filename=rel_path)
	except SyntaxError:
		return []

	blame = _git_blame_porcelain(repo_root, rel_path)
	file_birth = _git_file_birth(repo_root, rel_path)
	if file_birth is not None:
		file_commit, file_author_time = file_birth
	else:
		file_commit, file_author_time = _worktree_mtime(repo_root, rel_path)
	file_date = _format_date(file_author_time)
	file_commit_short = file_commit[:10] if file_commit not in ("", "WORKTREE") else file_commit

	out: list[QuestionFunction] = []

	def handle_fn(node: ast.FunctionDef | ast.AsyncFunctionDef, qualname: str):
		name = node.name
		if name in ("main", "parse_arguments", "parse_args"):
			return

		is_candidate = _is_question_function_name(name) or _calls_format_bb(node)
		if not is_candidate:
			return

		lineno = int(getattr(node, "lineno", 1))
		git_origin = _git_first_def_appearance(repo_root, rel_path, name)
		if git_origin is not None:
			commit, author_time = git_origin
		else:
			commit, author_time = blame.get(lineno, ("", 0))
			if author_time == 0:
				commit, author_time = _worktree_mtime(repo_root, rel_path)
		doc = ast.get_docstring(node)
		if doc is not None:
			doc = doc.strip().splitlines()[0].strip() if doc.strip() else None
		if doc is not None and len(doc) > 120:
			doc = doc[:117].rstrip() + "..."
		if doc is not None:
			doc = _ascii_md(doc)

		out.append(
			QuestionFunction(
				rel_path=rel_path,
				qualname=qualname,
				lineno=lineno,
				date=_format_date(author_time),
				commit=commit[:10] if commit not in ("", "WORKTREE") else commit,
				file_date=file_date,
				file_commit=file_commit_short,
				doc=doc,
			)
		)

	for node in tree.body:
		if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
			handle_fn(node, node.name)
			continue
		if isinstance(node, ast.ClassDef):
			for child in node.body:
				if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
					handle_fn(child, f"{node.name}.{child.name}")

	return out


def build_index(repo_root: str) -> list[QuestionFunction]:
	entries: list[QuestionFunction] = []
	paths = _list_target_py_files(repo_root)
	for abs_path in paths:
		rel_path = os.path.relpath(abs_path, repo_root)
		entries.extend(_extract_question_functions(repo_root, rel_path))

	# newest first
	entries.sort(key=lambda e: (e.date, e.rel_path, e.lineno), reverse=True)
	return entries


def write_markdown(repo_root: str, entries: list[QuestionFunction], out_path: str):
	head_hash, head_date = _git_head_info(repo_root)

	lines: list[str] = []
	lines.append("# Question-Creator Function Index")
	lines.append("")
	lines.append(
		"This file lists key functions that create quiz/homework questions (or question items) "
		"and the date they first appeared in Git history."
	)
	lines.append("")
	lines.append("- Source: `tools/build_question_function_index.py`")
	lines.append(f"- Git HEAD: `{head_hash}` ({head_date})")
	lines.append("- Date source: earliest commit that introduces `def <name>` in that file (`git log --follow -G ...`)")
	lines.append("- Also shown: file birth date (`git log --follow --diff-filter=A`)")
	lines.append("- Fallbacks: `git blame` on the `def ...` line; uncommitted/untracked files use file mtime (commit `WORKTREE`)")
	lines.append("- YAML-driven banks are tracked separately in `docs/YAML_QUESTION_BANK_INDEX.md`.")
	lines.append("")

	current_date = None
	for entry in entries:
		if entry.date != current_date:
			current_date = entry.date
			lines.append(f"## {current_date}")
		doc = f' - "{entry.doc}"' if entry.doc else ""
		file_note = ""
		if entry.file_date != entry.date:
			file_note = f" - file {entry.file_date} (commit `{entry.file_commit}`)"
		line = (
			f"- {entry.date} - `{entry.rel_path}:{entry.lineno}` - `{entry.qualname}` "
			f"(commit `{entry.commit}`){file_note}{doc}"
		)
		lines.append(_ascii_md(line))
	lines.append("")

	abs_out = os.path.join(repo_root, out_path)
	os.makedirs(os.path.dirname(abs_out), exist_ok=True)
	with open(abs_out, "w", encoding="utf-8") as f:
		ascii_lines = [_ascii_md(line) for line in lines]
		f.write("\n".join(ascii_lines))


def parse_args():
	parser = argparse.ArgumentParser(
		description="Build an index of question-creator functions and their creation dates."
	)
	parser.add_argument(
		"-o", "--output",
		dest="output",
		default="docs/QUESTION_FUNCTION_INDEX.md",
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
