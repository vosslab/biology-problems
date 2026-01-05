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
		"other_style": [],
	}

	for path in sorted(problems.rglob("*.py"), key=lambda p: str(p)):
		if ".venv" in path.parts:
			continue
		if path.name.endswith("lib.py"):
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
		new_framework = has_make_arg_parser and has_collect_and_write

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
		else:
			bins["not_new_framework"].append(rel)

		if style == "batch":
			bins["batch_style"].append(rel)
		elif style == "single":
			bins["single_style"].append(rel)
		else:
			bins["other_style"].append(rel)

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
		if ".venv" not in p.parts and not p.name.endswith("lib.py")
	])

	out_new = out_dir / "bptools_scripts_new_framework.txt"
	out_old = out_dir / "bptools_scripts_not_new_framework.txt"
	out_all = out_dir / "bptools_scripts_audit.txt"
	out_missing_shebang = out_dir / "bptools_scripts_missing_shebang.txt"
	out_missing_main_guard = out_dir / "bptools_scripts_missing_main_guard.txt"
	out_missing_either = out_dir / "bptools_scripts_missing_shebang_or_main_guard.txt"
	out_shebang_not_exec = out_dir / "bptools_scripts_shebang_not_executable.txt"
	out_batch = out_dir / "bptools_scripts_batch_style.txt"
	out_single = out_dir / "bptools_scripts_single_style.txt"
	out_other = out_dir / "bptools_scripts_other_style.txt"

	write_lines(
		out_new,
		bins["new_framework"],
		header_comment="Scripts under problems/ that have a python shebang + __main__ guard and use make_arg_parser + collect_and_write_questions.",
	)
	write_lines(
		out_old,
		bins["not_new_framework"],
		header_comment="Scripts under problems/ that have a python shebang + __main__ guard but do not match the new bptools framework heuristic.",
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
	write_lines(
		out_other,
		bins["other_style"],
		header_comment="Scripts under problems/ with a python shebang + __main__ guard that do not match batch-style or single-question bptools patterns (often utilities or non-bptools scripts).",
	)

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
		"# - Excludes *lib.py",
		"#",
		"# Script definition for binning:",
		"# - Has python shebang and __main__ guard",
		"#",
		"# New framework heuristic:",
		"# - contains make_arg_parser and collect_and_write_questions",
		"#",
		f"# Files scanned (non-lib .py): {py_files_scanned}",
		f"# Scripts found: {len(entries)}",
		f"# Missing shebang or main guard (script-like only): {len(bins['missing_either'])}",
		f"# Has shebang but not executable: {len(bins['shebang_not_executable'])}",
		f"# Batch-style scripts: {len(bins['batch_style'])}",
		f"# Single-style scripts: {len(bins['single_style'])}",
		f"# Other-style scripts: {len(bins['other_style'])}",
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
		"== Other style ==",
		* (bins["other_style"] if bins["other_style"] else ["(none)"]),
		"",
		"== Detailed flags (tab-separated) ==",
		*detailed_lines,
		"",
	]
	write_lines(out_all, header)

	print("Wrote:")
	print(f"  {out_new.relative_to(repo)}")
	print(f"  {out_old.relative_to(repo)}")
	print(f"  {out_batch.relative_to(repo)}")
	print(f"  {out_single.relative_to(repo)}")
	print(f"  {out_other.relative_to(repo)}")
	print(f"  {out_all.relative_to(repo)}")
	print(f"  {out_missing_shebang.relative_to(repo)}")
	print(f"  {out_missing_main_guard.relative_to(repo)}")
	print(f"  {out_missing_either.relative_to(repo)}")
	print(f"  {out_shebang_not_exec.relative_to(repo)}")


if __name__ == "__main__":
	main()
