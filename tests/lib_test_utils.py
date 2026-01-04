#!/usr/bin/env python3

import importlib.util
import contextlib
import os
import sys


def repo_root() -> str:
	return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def import_from_repo_path(rel_path: str):
	root = repo_root()
	abs_path = os.path.join(root, rel_path)
	module_dir = os.path.dirname(abs_path)

	added: list[str] = []
	for path_item in (root, module_dir):
		if path_item not in sys.path:
			sys.path.insert(0, path_item)
			added.append(path_item)

	try:
		module_name = rel_path.replace(os.sep, "_").replace("-", "_").replace(".", "_")
		spec = importlib.util.spec_from_file_location(module_name, abs_path)
		assert spec is not None
		assert spec.loader is not None
		module = importlib.util.module_from_spec(spec)
		sys.modules[module_name] = module
		spec.loader.exec_module(module)
		return module
	finally:
		for _ in added:
			sys.path.pop(0)


@contextlib.contextmanager
def temp_sys_path(*paths: str):
	added_count = 0
	for path_item in paths:
		if path_item in sys.path:
			continue
		sys.path.insert(0, path_item)
		added_count += 1
	try:
		yield
	finally:
		for _ in range(added_count):
			sys.path.pop(0)
