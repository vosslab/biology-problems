"""Keep tracked root scripts below the repository-navigation budget."""

# Standard Library
import pathlib
import stat

# PIP3 modules
import pytest

# local repo modules
import file_utils


WARNING_MINIMUM = 5
FAILURE_MINIMUM = 7
REPORT_NAME = file_utils.report_name(__file__)
REPO_ROOT = file_utils.get_repo_root()
COUNTED_ROOT_SCRIPTS: list[str] = []


#============================================
def has_shebang(path: pathlib.Path) -> bool:
	"""Return whether a file begins with a script shebang."""
	with path.open("rb") as handle:
		return handle.read(2) == b"#!"


#============================================
def is_executable(path: pathlib.Path) -> bool:
	"""Return whether any executable mode bit is set on path."""
	mode = path.stat().st_mode
	return bool(mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))


#============================================
def counted_root_scripts(repo_root: str, tracked_paths: list[str]) -> list[str]:
	"""Return sorted tracked root scripts under the documented counting rule."""
	counted = []
	for rel in sorted(tracked_paths):
		if "/" in rel:
			continue
		path = pathlib.Path(repo_root, rel)
		if not path.is_file():
			continue
		if path.suffix in {".py", ".sh"}:
			counted.append(rel)
			continue
		if is_executable(path) and has_shebang(path):
			counted.append(rel)
	return counted


#============================================
def budget_report_lines(scripts: list[str]) -> list[str]:
	"""Return warning or violation lines, or silence below the warning band."""
	count = len(scripts)
	if count < WARNING_MINIMUM:
		return []
	if count >= FAILURE_MINIMUM:
		status = f"VIOLATION: {count} counted root scripts; limit is {FAILURE_MINIMUM - 1}."
	else:
		status = f"WARNING: {count} counted root scripts; warning band is 5-6."
	return [status] + [f"- {script}" for script in scripts]


#============================================
@pytest.fixture(scope="module", autouse=True)
def collect_report() -> None:
	"""Write a complete root-script warning or violation report when needed."""
	file_utils.clear_stale_reports()
	COUNTED_ROOT_SCRIPTS.clear()
	COUNTED_ROOT_SCRIPTS.extend(
		counted_root_scripts(REPO_ROOT, file_utils.list_tracked_files(REPO_ROOT))
	)
	lines = budget_report_lines(COUNTED_ROOT_SCRIPTS)
	if lines:
		file_utils.write_report_lines(REPORT_NAME, lines)


#============================================
def test_root_script_budget() -> None:
	"""Fail only when seven or more documented root scripts are present."""
	assert len(COUNTED_ROOT_SCRIPTS) < FAILURE_MINIMUM, (
		f"{len(COUNTED_ROOT_SCRIPTS)} counted root scripts exceed the limit of "
		f"{FAILURE_MINIMUM - 1}; see {REPORT_NAME}."
	)


#============================================
def make_root_scripts(root: pathlib.Path, count: int) -> list[str]:
	"""Create count tracked-looking root Python scripts for one synthetic root."""
	paths = []
	for index in range(count):
		name = f"script_{index}.py"
		(root / name).write_text("print('script')\n", encoding="utf-8")
		paths.append(name)
	return paths


#============================================
def use_temporary_report_root(
		monkeypatch: pytest.MonkeyPatch,
		tmp_path: pathlib.Path,
) -> None:
	"""Point shared report utilities at tmp_path for an isolated assertion."""
	def temporary_root() -> str:
		"""Return the synthetic repository root for shared report utilities."""
		return str(tmp_path)

	monkeypatch.setattr(file_utils, "get_repo_root", temporary_root)


#============================================
def test_clean_lifecycle_removes_stale_canonical_report(
		tmp_path: pathlib.Path,
		monkeypatch: pytest.MonkeyPatch,
) -> None:
	"""A clean production lifecycle removes its stale canonical report first."""
	tracked_paths = make_root_scripts(tmp_path, 4)
	report_path = tmp_path / REPORT_NAME
	report_path.write_text("stale\n", encoding="utf-8")

	def synthetic_tracked_paths(_repo_root: str) -> list[str]:
		"""Return the synthetic tracked list for the production collector."""
		return tracked_paths

	use_temporary_report_root(monkeypatch, tmp_path)
	monkeypatch.setattr(file_utils, "list_tracked_files", synthetic_tracked_paths)
	monkeypatch.setattr(file_utils, "_STALE_REPORTS_CLEARED", False)
	monkeypatch.setitem(globals(), "REPO_ROOT", str(tmp_path))
	monkeypatch.setitem(globals(), "COUNTED_ROOT_SCRIPTS", [])
	collect_report.__wrapped__()
	assert not report_path.exists()


#============================================
@pytest.mark.parametrize("count", [5, 6])
def test_warning_band_reports_counted_files(
		tmp_path: pathlib.Path,
		monkeypatch: pytest.MonkeyPatch,
		count: int,
) -> None:
	"""Five or six counted scripts pass while naming every script in a report."""
	tracked_paths = make_root_scripts(tmp_path, count)
	scripts = counted_root_scripts(str(tmp_path), tracked_paths)
	use_temporary_report_root(monkeypatch, tmp_path)
	file_utils.write_report_lines(REPORT_NAME, budget_report_lines(scripts))
	report_text = (tmp_path / REPORT_NAME).read_text(encoding="utf-8")
	assert report_text.splitlines()[1:] == [f"- {script}" for script in scripts]
	assert len(scripts) < FAILURE_MINIMUM


#============================================
def test_failure_band_reports_and_fails(
		tmp_path: pathlib.Path,
		monkeypatch: pytest.MonkeyPatch,
) -> None:
	"""Seven counted root scripts create a violation report and fail the budget."""
	tracked_paths = make_root_scripts(tmp_path, 7)
	scripts = counted_root_scripts(str(tmp_path), tracked_paths)
	use_temporary_report_root(monkeypatch, tmp_path)
	file_utils.write_report_lines(REPORT_NAME, budget_report_lines(scripts))
	report_text = (tmp_path / REPORT_NAME).read_text(encoding="utf-8")
	assert report_text.startswith("VIOLATION: 7 counted root scripts; limit is 6.\n")
	assert len(scripts) >= FAILURE_MINIMUM


#============================================
def test_other_extension_requires_executable_shebang(tmp_path: pathlib.Path) -> None:
	"""Count all Python/shell files and only other executable shebang launchers."""
	python_file = tmp_path / "program.py"
	python_file.write_text("print('script')\n", encoding="utf-8")
	shell_file = tmp_path / "source_me.sh"
	shell_file.write_text("source ~/.bashrc\n", encoding="utf-8")
	launcher = tmp_path / "launcher"
	launcher.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
	launcher.chmod(0o755)
	with_suffix = tmp_path / "launcher.command"
	with_suffix.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
	with_suffix.chmod(0o755)
	data = tmp_path / "data"
	data.write_text("not a script\n", encoding="utf-8")
	data.chmod(0o755)
	non_executable = tmp_path / "not_executable"
	non_executable.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
	assert counted_root_scripts(
		str(tmp_path), [
			"data",
			"launcher",
			"launcher.command",
			"not_executable",
			"program.py",
			"source_me.sh",
		]
	) == ["launcher", "launcher.command", "program.py", "source_me.sh"]
# Vendored pytest file. Local changes can and will be overwritten.
