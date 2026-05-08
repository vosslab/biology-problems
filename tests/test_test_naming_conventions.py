import os
import fnmatch

import git_file_utils

REPO_ROOT = git_file_utils.get_repo_root()


#============================================
def get_e2e_dir() -> str:
	"""
	Return the tests/e2e directory path.
	"""
	return os.path.join(REPO_ROOT, "tests", "e2e")


#============================================
def get_playwright_dir() -> str:
	"""
	Return the tests/playwright directory path.
	"""
	return os.path.join(REPO_ROOT, "tests", "playwright")


#============================================
def e2e_dir_exists() -> bool:
	"""
	Check whether the tests/e2e directory exists.
	"""
	return os.path.isdir(get_e2e_dir())


#============================================
def playwright_dir_exists() -> bool:
	"""
	Check whether the tests/playwright directory exists.
	"""
	return os.path.isdir(get_playwright_dir())


#============================================
def list_files_recursive(directory: str) -> list[str]:
	"""
	List all files under a directory recursively, returning relative paths.
	"""
	files = []
	for root, dirs, filenames in os.walk(directory):
		for filename in filenames:
			full_path = os.path.join(root, filename)
			rel_path = os.path.relpath(full_path, directory)
			files.append(rel_path)
	return sorted(files)


#============================================
def list_e2e_files() -> list[str]:
	"""
	List all files under tests/e2e/ recursively, returning relative paths.
	"""
	e2e_dir = get_e2e_dir()
	return list_files_recursive(e2e_dir)


#============================================
def list_playwright_files() -> list[str]:
	"""
	List all files under tests/playwright/ recursively, returning relative paths.
	"""
	playwright_dir = get_playwright_dir()
	return list_files_recursive(playwright_dir)


#============================================
def test_no_test_prefix_in_e2e() -> None:
	"""
	Verify no test_*.py files exist under tests/e2e/.

	Such files are silently skipped by pytest (due to collect_ignore in
	conftest), which is a trap: the name promises pytest collection but
	the location revokes it. Forbid the contradiction.
	"""
	if not e2e_dir_exists():
		return
	files = list_e2e_files()
	violations = []
	for filename in files:
		basename = os.path.basename(filename)
		if fnmatch.fnmatch(basename, "test_*.py"):
			violations.append(filename)
	if violations:
		raise AssertionError(
			f"Found test_*.py files under tests/e2e/ "
			f"(silently skipped by pytest): {violations}"
		)


#============================================
def test_no_test_prefix_in_playwright() -> None:
	"""
	Verify no test_*.py files exist under tests/playwright/.

	Such files are silently skipped by pytest (due to collect_ignore in
	conftest), which is a trap: the name promises pytest collection but
	the location revokes it. This includes tests/playwright/e2e/ and
	any other subtree. Forbid the contradiction.
	"""
	if not playwright_dir_exists():
		return
	files = list_playwright_files()
	violations = []
	for filename in files:
		basename = os.path.basename(filename)
		if fnmatch.fnmatch(basename, "test_*.py"):
			violations.append(filename)
	if violations:
		raise AssertionError(
			f"Found test_*.py files under tests/playwright/ "
			f"(silently skipped by pytest): {violations}"
		)


#============================================
def test_python_files_use_e2e_prefix() -> None:
	"""
	Verify all Python files under tests/e2e/ use e2e_*.py prefix.

	This is a readability convention: a file named e2e_*.py clearly
	indicates it is an end-to-end runner and should not be collected
	by pytest even if it were in tests/ directly.
	"""
	if not e2e_dir_exists():
		return
	files = list_e2e_files()
	violations = []
	for filename in files:
		if filename.endswith(".py"):
			if not fnmatch.fnmatch(filename, "e2e_*.py"):
				violations.append(filename)
	if violations:
		raise AssertionError(
			f"Python files under tests/e2e/ must use e2e_*.py prefix: "
			f"{violations}"
		)


#============================================
def test_shell_files_use_e2e_prefix() -> None:
	"""
	Verify all shell files under tests/e2e/ use e2e_*.sh prefix.

	This is a readability convention to match the Python rule and
	make the tier and tier membership clear to readers.
	"""
	if not e2e_dir_exists():
		return
	files = list_e2e_files()
	violations = []
	for filename in files:
		if filename.endswith(".sh"):
			if not fnmatch.fnmatch(filename, "e2e_*.sh"):
				violations.append(filename)
	if violations:
		raise AssertionError(
			f"Shell files under tests/e2e/ must use e2e_*.sh prefix: "
			f"{violations}"
		)


#============================================
def has_playwright_import(file_path: str) -> bool:
	"""
	Check whether a file imports Playwright.

	Looks for any of the standard import forms:
	  - from 'playwright' or from "playwright"
	  - from '@playwright/test' or from "@playwright/test"
	  - require('playwright') or require("playwright")
	  - require('@playwright/test') or require("@playwright/test")
	"""
	try:
		with open(file_path, "r", encoding="utf-8") as handle:
			content = handle.read()
	except (OSError, UnicodeDecodeError):
		return False
	playwright_patterns = [
		"from 'playwright'",
		'from "playwright"',
		"from '@playwright/test'",
		'from "@playwright/test"',
		"require('playwright')",
		'require("playwright")',
		"require('@playwright/test')",
		'require("@playwright/test")',
	]
	for pattern in playwright_patterns:
		if pattern in content:
			return True
	return False


#============================================
def list_mjs_files_outside_playwright() -> list[str]:
	"""
	List all .mjs files under tests/, excluding tests/playwright/ subtree.

	Returns relative paths from repo root.
	"""
	tests_dir = os.path.join(REPO_ROOT, "tests")
	playwright_dir = get_playwright_dir()
	files = []
	for root, dirs, filenames in os.walk(tests_dir):
		if root.startswith(playwright_dir):
			continue
		for filename in filenames:
			if filename.endswith(".mjs"):
				full_path = os.path.join(root, filename)
				rel_path = os.path.relpath(full_path, REPO_ROOT)
				files.append(rel_path)
	return sorted(files)


#============================================
def test_playwright_imports_in_playwright_folder() -> None:
	"""
	Verify Playwright imports only appear in .mjs files under tests/playwright/.

	Playwright browser tests must live under the browser tier
	(tests/playwright/, including tests/playwright/e2e/) to avoid
	confusion with fast-running pure Node tests or whole-system E2E.
	"""
	mjs_files = list_mjs_files_outside_playwright()
	violations = []
	for mjs_file in mjs_files:
		full_path = os.path.join(REPO_ROOT, mjs_file)
		if has_playwright_import(full_path):
			violations.append(mjs_file)
	if violations:
		raise AssertionError(
			f"Playwright imports found in .mjs files outside tests/playwright/. "
			f"Move these files to tests/playwright/: {violations}"
		)
