#!/usr/bin/env python3

import importlib.util
import contextlib
import os
import re
import sys


def repo_root() -> str:
	return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def resolve_repo_rel_path(rel_path: str) -> str:
	root = repo_root()
	rel_path = rel_path.lstrip(os.sep)

	candidates: list[str] = []
	candidates.append(rel_path)

	# Backward/forward compatible moves:
	# - `*-problems/` moved under `problems/*-problems/`
	# - `multiple_choice_statements/` may live under `problems/multiple_choice_statements/`
	# - `matching_sets/` may live under `problems/matching_sets/` (if you choose to move it)
	if rel_path.startswith(f"problems{os.sep}"):
		candidates.append(rel_path[len(f"problems{os.sep}"):])
	else:
		candidates.append(os.path.join("problems", rel_path))

	if rel_path.startswith(f"multiple_choice_statements{os.sep}"):
		candidates.append(os.path.join("problems", rel_path))

	if rel_path.startswith(f"matching_sets{os.sep}"):
		candidates.append(os.path.join("problems", rel_path))

	if re.match(r"^[A-Za-z0-9_]+-problems" + re.escape(os.sep), rel_path):
		candidates.append(os.path.join("problems", rel_path))

	seen: set[str] = set()
	for cand in candidates:
		if cand in seen:
			continue
		seen.add(cand)
		abs_path = os.path.join(root, cand)
		if os.path.exists(abs_path):
			return cand

	raise FileNotFoundError(f"Could not resolve repo path: {rel_path}")


def repo_abs_path(rel_path: str) -> str:
	root = repo_root()
	resolved = resolve_repo_rel_path(rel_path)
	return os.path.join(root, resolved)


def import_from_repo_path(rel_path: str):
	root = repo_root()
	rel_path = resolve_repo_rel_path(rel_path)
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
