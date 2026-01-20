
import hashlib
import importlib.util
import os
import sys

import pytest


def _repo_root() -> str:
	return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _list_lib_files() -> list[str]:
	root = _repo_root()
	lib_paths: list[str] = []
	for dirpath, dirnames, filenames in os.walk(root):
		dirnames[:] = [
			d for d in dirnames
			if d not in (".git", ".venv", "__pycache__", "old_shell_folder")
		]
		for filename in filenames:
			if not filename.endswith("lib.py"):
				continue
			lib_paths.append(os.path.join(dirpath, filename))
	lib_paths.sort()
	return lib_paths


def _module_name_for_path(path: str) -> str:
	root = _repo_root()
	rel = os.path.relpath(path, root)
	key = rel.encode("utf-8", errors="strict")
	short_hash = hashlib.sha1(key).hexdigest()[:10]
	safe = rel.replace(os.sep, "_").replace("-", "_").replace(".", "_")
	return f"bp_lib_{safe}_{short_hash}"


def _import_from_path(path: str):
	module_dir = os.path.dirname(path)
	added = False
	if module_dir not in sys.path:
		sys.path.insert(0, module_dir)
		added = True

	try:
		module_name = _module_name_for_path(path)
		spec = importlib.util.spec_from_file_location(module_name, path)
		assert spec is not None
		assert spec.loader is not None
		module = importlib.util.module_from_spec(spec)
		sys.modules[module_name] = module
		spec.loader.exec_module(module)
		return module
	finally:
		if added:
			sys.path.pop(0)


LIB_FILES = _list_lib_files()


@pytest.mark.parametrize("lib_path", LIB_FILES, ids=lambda p: os.path.relpath(p, _repo_root()))
def test_import_lib_module(lib_path: str):
	_import_from_path(lib_path)
