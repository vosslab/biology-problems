import ast
import os
import tokenize

import pytest

import git_file_utils

REPO_ROOT = git_file_utils.get_repo_root()
SKIP_DIRS = {".git", ".venv", "__pycache__", "old_shell_folder"}


#============================================
def path_has_skip_dir(path: str) -> bool:
	"""
	Check whether a relative path includes a skipped directory.
	"""
	parts = path.split(os.sep)
	for part in parts:
		if part in SKIP_DIRS:
			return True
	return False


#============================================
def filter_py_files(paths: list[str]) -> list[str]:
	"""
	Filter candidate paths to Python files that exist.
	"""
	matches = []
	seen = set()
	for path in paths:
		if path in seen:
			continue
		seen.add(path)
		if path_has_skip_dir(path):
			continue
		if "TEMPLATE" in path:
			continue
		if not path.endswith(".py"):
			continue
		if not os.path.isfile(path):
			continue
		matches.append(path)
	matches.sort()
	return matches


#============================================
def gather_files(repo_root: str) -> list[str]:
	"""
	Collect tracked Python files.
	"""
	paths = []
	for path in git_file_utils.list_tracked_files(
		repo_root,
		patterns=["*.py"],
		error_message="Failed to list tracked Python files.",
	):
		paths.append(os.path.join(repo_root, path))
	return filter_py_files(paths)


#============================================
def gather_changed_files(repo_root: str) -> list[str]:
	"""
	Collect changed Python files.
	"""
	paths = []
	for path in git_file_utils.list_changed_files(repo_root):
		paths.append(os.path.join(repo_root, path))
	return filter_py_files(paths)


#============================================
def read_source(path: str) -> str:
	"""
	Read Python source using tokenize.open for encoding correctness.
	"""
	with tokenize.open(path) as handle:
		text = handle.read()
	return text


#============================================
def find_import_star(path: str) -> list[tuple[int, str]]:
	"""
	Return line numbers for from-import * statements.
	"""
	source = read_source(path)
	try:
		tree = ast.parse(source, filename=path)
	except SyntaxError:
		return []
	matches = []
	for node in ast.walk(tree):
		if not isinstance(node, ast.ImportFrom):
			continue
		for alias in node.names:
			if alias.name != "*":
				continue
			line_no = getattr(node, "lineno", 0) or 0
			module_name = node.module or ""
			if getattr(node, "level", 0):
				module_name = f"{'.' * node.level}{module_name}"
			matches.append((line_no, module_name))
			break
	return matches


#============================================
def format_issue(rel_path: str, line_no: int, module_name: str) -> str:
	"""
	Format a report line for an import * usage.
	"""
	if module_name:
		return f"{rel_path}:{line_no}: import * from {module_name}"
	return f"{rel_path}:{line_no}: import *"


_FILES = git_file_utils.collect_files(REPO_ROOT, gather_files, gather_changed_files)


#============================================
@pytest.mark.parametrize(
	"file_path", _FILES,
	ids=lambda p: os.path.relpath(p, REPO_ROOT),
)
def test_import_star(file_path: str) -> None:
	"""Report import * usage in a single Python file."""
	matches = find_import_star(file_path)
	if not matches:
		return
	rel_path = os.path.relpath(file_path, REPO_ROOT)
	issues = [format_issue(rel_path, line_no, module_name) for line_no, module_name in matches]
	raise AssertionError("import * usage detected:\n" + "\n".join(issues))
