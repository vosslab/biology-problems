"""Enforce a maintainable line-count limit for tracked source files."""

# Standard Library
import os
import pathlib

# PIP3 modules
import pytest

# local repo modules
import file_utils


LINE_LIMIT = 1000
OVERRIDE_LIST = "tests/source_file_line_limit_overrides.txt"

# Authored code, templates, queries, and documentation. Generic text/data,
# generated artifacts, configuration, notebooks, and binary formats stay out.
SOURCE_EXTENSIONS = frozenset({
	".ac", ".adoc", ".am", ".asm", ".asciidoc",
	".bash", ".bat", ".bnf",
	".c", ".cc", ".cgi", ".cjs", ".clj", ".cljs", ".cljc", ".cmake",
	".cmd", ".coffee", ".cpp", ".cs", ".css", ".cts", ".cxx",
	".dart", ".dockerfile",
	".el", ".ep", ".erl", ".ex", ".exs",
	".f", ".f03", ".f08", ".f90", ".f95", ".fish", ".fs", ".fsx",
	".go", ".gradle", ".groovy",
	".h", ".hpp", ".hrl", ".hs", ".htm", ".html", ".hxx",
	".i", ".inc",
	".java", ".jl", ".js", ".jst", ".jsx",
	".kt", ".kts",
	".less", ".lhs", ".lisp", ".lua",
	".m", ".markdown", ".maxima", ".md", ".mjs", ".ml", ".mli", ".mm", ".mts",
	".nim", ".nix",
	".pas", ".pg", ".pgml", ".php", ".pl", ".pm", ".pod", ".proto", ".ps1", ".py",
	".qmd", ".qml",
	".r", ".rb", ".rkt", ".rmd", ".rs", ".rst",
	".sass", ".scala", ".scm", ".scss", ".sh", ".sol", ".sql", ".svelte", ".swift",
	".t", ".tcl", ".tcss", ".tex", ".tf", ".ts", ".tsx",
	".v", ".vb", ".vhd", ".vhdl", ".vue",
	".zig", ".zsh",
})

# Common source/build filenames without a useful source extension.
SOURCE_FILENAMES = frozenset({
	"brewfile",
	"cmakelists.txt",
	"dockerfile",
	"gemfile",
	"jenkinsfile",
	"justfile",
	"makefile",
	"meson.build",
	"pkgbuild",
	"rakefile",
	"sconscript",
	"sconstruct",
	"vagrantfile",
})

REPORT_NAME = file_utils.report_name(__file__)
HEADER = "Source file line-limit violations:"
VIOLATIONS_BY_FILE: dict[str, list[str]] = {}


#============================================
def load_override_paths(repo_root: str | None = None) -> frozenset[str]:
	"""
	Load manager-approved exact paths that are outside the line-limit policy.

	The optional list contains one repo-relative POSIX path per non-comment
	line. Missing files are normal because most repos need no overrides.

	Args:
		repo_root: Repository root. Defaults to the active Git repository root.

	Returns:
		frozenset[str]: Exact repo-relative paths approved for exclusion.
	"""
	if repo_root is None:
		repo_root = file_utils.get_repo_root()
	list_path = os.path.join(repo_root, OVERRIDE_LIST)
	if not os.path.isfile(list_path):
		return frozenset()
	overrides = set()
	with open(list_path, "r", encoding="utf-8") as handle:
		for line_number, raw_line in enumerate(handle, start=1):
			entry = raw_line.strip()
			if not entry or entry.startswith("#"):
				continue
			parts = entry.split("/")
			invalid = entry.startswith("/") or "\\" in entry or ".." in parts
			invalid = invalid or any(character in entry for character in "*?[]")
			if invalid:
				raise ValueError(
					f"{OVERRIDE_LIST}:{line_number}: expected an exact repo-relative POSIX path"
				)
			overrides.add(entry)
	result = frozenset(overrides)
	return result


OVERRIDE_PATHS = load_override_paths()


#============================================
def is_source_file(
	rel: str,
	override_paths: frozenset[str] | None = None,
) -> bool:
	"""
	Select authored source files by extension or conventional filename.

	Args:
		rel: Repo-relative POSIX path.
		override_paths: Exact manager-approved paths. Defaults to the active
			repository's optional override list.

	Returns:
		bool: True when the path is an authored source file covered by the gate.
	"""
	if override_paths is None:
		override_paths = OVERRIDE_PATHS
	basename = os.path.basename(rel).lower()
	extension = os.path.splitext(basename)[1]
	is_source = basename in SOURCE_FILENAMES or extension in SOURCE_EXTENSIONS
	if rel in override_paths:
		return False
	return is_source


FILES = file_utils.discover_files(
	extra_filter=is_source_file,
	test_key="source_file_line_limit",
)


#============================================
def count_file_lines(path: str) -> int:
	"""
	Count physical lines without decoding the source file.

	Args:
		path: Absolute path to a source file.

	Returns:
		int: Physical line count, including a final line without a newline.
	"""
	with open(path, "rb") as handle:
		line_count = sum(1 for _line in handle)
	return line_count


#============================================
def violations_for_line_count(rel: str, line_count: int) -> list[str]:
	"""
	Return a violation when a source file reaches the exclusive limit.

	Args:
		rel: Repo-relative POSIX path used in the violation message.
		line_count: Physical line count for the file.

	Returns:
		list[str]: One violation at 1000 or more lines, otherwise an empty list.
	"""
	if line_count < LINE_LIMIT:
		return []
	message = f"{rel}: {line_count} lines"
	return [message]


#============================================
def check_file(rel: str) -> list[str]:
	"""
	Check one source file against the exclusive line limit.

	Args:
		rel: Repo-relative POSIX path to check.

	Returns:
		list[str]: One formatted violation when the file is too long, otherwise empty.
	"""
	abs_path = os.path.join(file_utils.get_repo_root(), rel)
	line_count = count_file_lines(abs_path)
	violations = violations_for_line_count(rel, line_count)
	return violations


#============================================
@pytest.fixture(scope="module", autouse=True)
def collect_report() -> None:
	"""Collect all line-limit violations and write the complete report when dirty."""
	file_utils.clear_stale_reports()
	VIOLATIONS_BY_FILE.clear()
	VIOLATIONS_BY_FILE.update(file_utils.collect_file_violations(FILES, check_file))
	lines = file_utils.format_violation_report(HEADER, VIOLATIONS_BY_FILE)
	if lines:
		file_utils.write_report_lines(REPORT_NAME, lines)


#============================================
@pytest.mark.parametrize(
	("line_count", "should_fail"),
	((999, False), (1000, True)),
	ids=("999-lines-ok", "1000-lines-fails"),
)
def test_source_file_line_limit_boundary(line_count: int, should_fail: bool) -> None:
	"""Pin the requested exclusive boundary: 999 passes and 1000 fails."""
	violations = violations_for_line_count("sample.py", line_count)
	assert bool(violations) is should_fail


#============================================
def test_source_file_line_limit_override_list(tmp_path: pathlib.Path) -> None:
	"""Load an exact manager-approved path while ignoring comments and blanks."""
	tests_dir = tmp_path / "tests"
	tests_dir.mkdir()
	list_path = tests_dir / "source_file_line_limit_overrides.txt"
	list_path.write_text(
		"# Downloaded normative specification\n\ndocs/QTI_v3_SPEC.md\n",
		encoding="utf-8",
	)
	overrides = load_override_paths(str(tmp_path))
	assert not is_source_file("docs/QTI_v3_SPEC.md", overrides)


#============================================
@pytest.mark.parametrize("path", FILES, ids=file_utils.rel_id)
def test_source_file_line_limit(path: str) -> None:
	"""Fail when a tracked authored source file contains 1000 or more lines."""
	rel = file_utils.rel_to_root(path)
	assert rel not in VIOLATIONS_BY_FILE, file_utils.format_violation_assert_message(
		rel, VIOLATIONS_BY_FILE.get(rel, []), REPORT_NAME
	)
# Vendored pytest file. Local changes can and will be overwritten.
