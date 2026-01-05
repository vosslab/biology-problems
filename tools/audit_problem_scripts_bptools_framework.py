#!/usr/bin/env python3

import re
import stat
import subprocess
from dataclasses import dataclass
from pathlib import Path


MAIN_GUARD_RE = re.compile(r'^[ \t]*if[ \t]+__name__[ \t]*==[ \t]*[\'"]__main__[\'"]:[ \t]*$', re.M)
SCRIPT_CANDIDATE_RE = re.compile(
	r"(argparse\.ArgumentParser|make_arg_parser|collect_and_write_questions|write_questions_to_file|make_outfile|^\s*def\s+main\s*\()",
	re.M,
)
WRITE_QUESTION_BATCH_RE = re.compile(r"^[ \t]*def[ \t]+write_question_batch[ \t]*\(", re.M)
BPT_TOOLS_IMPORT_RE = re.compile(r"^[ \t]*(import[ \t]+bptools\b|from[ \t]+bptools[ \t]+import[ \t]+)", re.M)


def repo_root() -> Path:
	try:
		out = subprocess.check_output(
			["git", "rev-parse", "--show-toplevel"],
			text=True,
			stderr=subprocess.DEVNULL,
		).strip()
		if out:
			return Path(out)
	except Exception:
		pass
	return Path(__file__).resolve().parents[1]


def has_python_shebang(path: Path) -> bool:
	try:
		first = path.open("r", encoding="utf-8", errors="ignore").readline()
	except OSError:
		return False
	return first.startswith("#!") and ("python" in first)


def has_main_guard(text: str) -> bool:
	return MAIN_GUARD_RE.search(text) is not None


def is_script_candidate(text: str) -> bool:
	return SCRIPT_CANDIDATE_RE.search(text) is not None


def is_executable(path: Path) -> bool:
	try:
		mode = path.stat().st_mode
	except OSError:
		return False
	return bool(mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))


def read_text(path: Path) -> str:
	try:
		return path.read_text(encoding="utf-8", errors="ignore")
	except OSError:
		return ""


def is_library_path(path: Path) -> bool:
	if path.name.endswith("lib.py"):
		return True
	for part in path.parts:
		if part.endswith("lib"):
			return True
	return False


@dataclass(frozen=True)
class ScriptInfo:
	rel_path: str
	has_make_arg_parser: bool
	has_collect_and_write: bool
	has_collect_batches: bool
	has_make_outfile: bool
	has_write_questions_to_file: bool
	style: str  # single|batch|other
	new_framework: bool


def classify_style(text: str) -> str:
	has_collect_and_write = "collect_and_write_questions" in text
	has_collect_batches = "collect_question_batches" in text
	has_write_questions_to_file = "write_questions_to_file" in text
	has_write_question_batch_def = WRITE_QUESTION_BATCH_RE.search(text) is not None

	if has_collect_batches or has_write_questions_to_file or has_write_question_batch_def:
		return "batch"
	if has_collect_and_write:
		return "single"
	return "other"


def uses_bptools_framework(text: str) -> bool:
	"""
	Heuristic for scripts using the bptools CLI framework.

	We treat both single-question and batch-question styles as "new framework".
	"""
	has_make_arg_parser = "make_arg_parser" in text
	has_single = "collect_and_write_questions" in text
	has_batch = ("collect_question_batches" in text) or ("write_questions_to_file" in text) or (WRITE_QUESTION_BATCH_RE.search(text) is not None)
	return has_make_arg_parser and (has_single or has_batch)


def imports_bptools(text: str) -> bool:
	return BPT_TOOLS_IMPORT_RE.search(text) is not None


def build_audit(repo: Path) -> tuple[list[ScriptInfo], dict[str, list[str]]]:
	problems = repo / "problems"
	entries: list[ScriptInfo] = []

	bins: dict[str, list[str]] = {
		"missing_shebang": [],
		"missing_main_guard": [],
		"missing_either": [],
		"shebang_not_executable": [],
		"new_framework": [],
		"not_new_framework": [],
		"batch_style": [],
		"single_style": [],
		"no_bptools": [],
	}

	for path in sorted(problems.rglob("*.py"), key=lambda p: str(p)):
		if ".venv" in path.parts:
			continue
		if is_library_path(path):
			continue
		text = read_text(path)
		rel = str(path.relative_to(repo))

		shebang = has_python_shebang(path)
		main_guard = has_main_guard(text)
		candidate = is_script_candidate(text)

		if shebang and (not is_executable(path)):
			bins["shebang_not_executable"].append(f"{rel}\tmain_guard_missing={'yes' if not main_guard else 'no'}")

		if (not shebang) or (not main_guard):
			if candidate:
				if not shebang:
					bins["missing_shebang"].append(rel)
				if not main_guard:
					bins["missing_main_guard"].append(rel)
				bins["missing_either"].append(
					f"{rel}\tshebang_missing={'yes' if not shebang else 'no'}\tmain_guard_missing={'yes' if not main_guard else 'no'}"
				)
			continue

		# Only treat as a "script" if it has both a python shebang and a main guard.
		has_make_arg_parser = "make_arg_parser" in text
		has_collect_and_write = "collect_and_write_questions" in text
		has_collect_batches = "collect_question_batches" in text
		has_make_outfile = "make_outfile" in text
		has_write_questions_to_file = "write_questions_to_file" in text

		style = classify_style(text)
		new_framework = uses_bptools_framework(text)
		has_bptools_import = imports_bptools(text)

		entries.append(
			ScriptInfo(
				rel_path=rel,
				has_make_arg_parser=has_make_arg_parser,
				has_collect_and_write=has_collect_and_write,
				has_collect_batches=has_collect_batches,
				has_make_outfile=has_make_outfile,
				has_write_questions_to_file=has_write_questions_to_file,
				style=style,
				new_framework=new_framework,
			)
		)

		if new_framework:
			bins["new_framework"].append(rel)
		elif has_bptools_import:
			bins["not_new_framework"].append(rel)
		else:
			bins["no_bptools"].append(rel)

		# Style bins are only meaningful for scripts using the bptools framework.
		if new_framework:
			if style == "batch":
				bins["batch_style"].append(rel)
			elif style == "single":
				bins["single_style"].append(rel)

	return entries, bins


def write_lines(path: Path, lines: list[str], header_comment: str | None = None):
	path.parent.mkdir(parents=True, exist_ok=True)
	out_lines: list[str] = []
	if header_comment:
		out_lines.append(f"# {header_comment}")
	out_lines.extend(lines)
	path.write_text("\n".join(out_lines) + ("\n" if out_lines else ""), encoding="utf-8")


def write_lines_if_nonempty(path: Path, lines: list[str], header_comment: str | None = None):
	"""
	Write a newline-terminated list file, but do not create the file when empty.
	If the file exists from a previous run, delete it when the new result is empty.
	"""
	if not lines:
		path.unlink(missing_ok=True)
		return
	write_lines(path, lines, header_comment=header_comment)


def main():
	repo = repo_root()
	out_dir = repo / "tools"

	entries, bins = build_audit(repo)
	py_files_scanned = len([
		p for p in (repo / "problems").rglob("*.py")
		if ".venv" not in p.parts and not is_library_path(p)
	])
	libs = sorted([
		str(p.relative_to(repo))
		for p in (repo / "problems").rglob("*.py")
		if ".venv" not in p.parts and is_library_path(p)
	], key=str)

	out_new = out_dir / "bptools_scripts_new_framework.txt"
	out_old = out_dir / "bptools_scripts_not_new_framework.txt"
	out_no_bptools = out_dir / "bptools_scripts_no_bptools.txt"
	out_all = out_dir / "bptools_scripts_audit.md"
	out_libs = out_dir / "problem_lib_modules.txt"
	out_missing_shebang = out_dir / "bptools_scripts_missing_shebang.txt"
	out_missing_main_guard = out_dir / "bptools_scripts_missing_main_guard.txt"
	out_missing_either = out_dir / "bptools_scripts_missing_shebang_or_main_guard.txt"
	out_shebang_not_exec = out_dir / "bptools_scripts_shebang_not_executable.txt"
	out_batch = out_dir / "bptools_scripts_batch_style.txt"
	out_single = out_dir / "bptools_scripts_single_style.txt"

	write_lines(
		out_new,
		bins["new_framework"],
		header_comment="Scripts under problems/ that have a python shebang + __main__ guard and use the bptools question CLI framework (make_arg_parser + (collect_and_write_questions OR collect_question_batches/write_question_batch/write_questions_to_file)).",
	)
	write_lines(
		out_old,
		bins["not_new_framework"],
		header_comment="Scripts under problems/ that have a python shebang + __main__ guard and import bptools, but do not match the bptools framework heuristic.",
	)
	write_lines(
		out_no_bptools,
		bins["no_bptools"],
		header_comment="Scripts under problems/ that have a python shebang + __main__ guard but do not import bptools.",
	)
	write_lines(
		out_libs,
		libs,
		header_comment="All *lib.py modules under problems/ (excluded from script binning).",
	)
	write_lines_if_nonempty(
		out_missing_shebang,
		bins["missing_shebang"],
		header_comment="Script-like python files under problems/ that appear runnable but are missing a python shebang line.",
	)
	write_lines_if_nonempty(
		out_missing_main_guard,
		bins["missing_main_guard"],
		header_comment="Script-like python files under problems/ that appear runnable but are missing an if __name__ == \"__main__\": guard.",
	)
	write_lines_if_nonempty(
		out_missing_either,
		bins["missing_either"],
		header_comment="Script-like python files under problems/ missing a python shebang and/or an if __name__ == \"__main__\": guard (tab-separated).",
	)
	write_lines(
		out_shebang_not_exec,
		bins["shebang_not_executable"],
		header_comment="Scripts under problems/ with a python shebang but not executable (+x); tab-separated with main_guard_missing flag.",
	)
	write_lines(
		out_batch,
		bins["batch_style"],
		header_comment="Scripts under problems/ with a python shebang + __main__ guard that look batch-style (collect_question_batches and/or write_question_batch and/or write_questions_to_file).",
	)
	write_lines(
		out_single,
		bins["single_style"],
		header_comment="Scripts under problems/ with a python shebang + __main__ guard that look single-question style (collect_and_write_questions and not batch-style).",
	)
	# Back-compat cleanup: older runs wrote this name.
	(out_dir / "bptools_scripts_other_style.txt").unlink(missing_ok=True)
	(out_dir / "bptools_scripts_audit.txt").unlink(missing_ok=True)

	detailed_lines = []
	for e in entries:
		detailed_lines.append(
			f"{e.rel_path}\t"
			f"make_arg_parser={'yes' if e.has_make_arg_parser else 'no'}\t"
			f"collect_and_write_questions={'yes' if e.has_collect_and_write else 'no'}\t"
			f"collect_question_batches={'yes' if e.has_collect_batches else 'no'}\t"
			f"make_outfile={'yes' if e.has_make_outfile else 'no'}\t"
			f"write_questions_to_file={'yes' if e.has_write_questions_to_file else 'no'}\t"
			f"style={e.style}\t"
			f"new_framework={'yes' if e.new_framework else 'no'}"
		)

	header = [
		"# bptools framework audit",
		"#",
		"# Scope:",
		"# - Under problems/",
		"# - Excludes *lib.py and any *.py under directories ending in 'lib'",
		"#",
		"# Script definition for binning:",
		"# - Has python shebang and __main__ guard",
		"#",
		"# New framework heuristic:",
		"# - contains make_arg_parser and (collect_and_write_questions OR collect_question_batches OR write_questions_to_file OR def write_question_batch(...))",
		"#",
		f"# Files scanned (non-lib .py): {py_files_scanned}",
		f"# Library modules (*lib.py) under problems/: {len(libs)}",
		f"# Scripts found: {len(entries)}",
		f"# Missing shebang or main guard (script-like only): {len(bins['missing_either'])}",
		f"# Has shebang but not executable: {len(bins['shebang_not_executable'])}",
		f"# Imports bptools but not framework: {len(bins['not_new_framework'])}",
		f"# Batch-style scripts: {len(bins['batch_style'])}",
		f"# Single-style scripts: {len(bins['single_style'])}",
		f"# Scripts that do not import bptools: {len(bins['no_bptools'])}",
		"",
		"== Has shebang but not executable (+x) ==",
		* (bins["shebang_not_executable"] if bins["shebang_not_executable"] else ["(none)"]),
		"",
		"== Missing shebang and/or __main__ guard ==",
		* (bins["missing_either"] if bins["missing_either"] else ["(none)"]),
		"",
		"== New framework ==",
		* (bins["new_framework"] if bins["new_framework"] else ["(none)"]),
		"",
		"== Not new framework ==",
		* (bins["not_new_framework"] if bins["not_new_framework"] else ["(none)"]),
		"",
		"== Batch style ==",
		* (bins["batch_style"] if bins["batch_style"] else ["(none)"]),
		"",
		"== Single style ==",
		* (bins["single_style"] if bins["single_style"] else ["(none)"]),
		"",
		"== No bptools ==",
		* (bins["no_bptools"] if bins["no_bptools"] else ["(none)"]),
		"",
		"== Detailed flags (tab-separated) ==",
		*detailed_lines,
		"",
	]
	write_lines(out_all, header)

	print("Wrote:")
	def _print_written(path: Path, entry_count: int | None, always_exists: bool = True):
		rel = path.relative_to(repo)
		if not path.exists():
			if always_exists:
				print(f"  {rel}\t(missing)")
			else:
				print(f"  {rel}\t(skipped; 0 entries)")
			return
		try:
			line_count = sum(1 for _ in path.open("r", encoding="utf-8", errors="ignore"))
		except OSError:
			line_count = -1
		if entry_count is None:
			print(f"  {rel}\t({line_count} lines)")
			return
		print(f"  {rel}\t({entry_count} entries; {line_count} lines)")

	_print_written(out_new, len(bins["new_framework"]))
	_print_written(out_old, len(bins["not_new_framework"]))
	_print_written(out_batch, len(bins["batch_style"]))
	_print_written(out_single, len(bins["single_style"]))
	_print_written(out_no_bptools, len(bins["no_bptools"]))
	_print_written(out_libs, len(libs))
	_print_written(out_all, None)
	_print_written(out_missing_shebang, len(bins["missing_shebang"]), always_exists=False)
	_print_written(out_missing_main_guard, len(bins["missing_main_guard"]), always_exists=False)
	_print_written(out_missing_either, len(bins["missing_either"]), always_exists=False)
	_print_written(out_shebang_not_exec, len(bins["shebang_not_executable"]))


if __name__ == "__main__":
	main()
