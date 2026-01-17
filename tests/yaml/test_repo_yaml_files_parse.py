#!/usr/bin/env python3

from pathlib import Path

import pytest

# PIP3 modules
import yaml


def _iter_repo_yaml_files():
	repo_roots = (Path("data"), Path("problems"))
	for repo_root in repo_roots:
		if not repo_root.is_dir():
			continue
		for pattern in ("*.yml", "*.yaml"):
			yield from repo_root.rglob(pattern)


_YAML_FILES = sorted(_iter_repo_yaml_files(), key=lambda p: str(p))


@pytest.mark.parametrize("yaml_path", _YAML_FILES)
def test_repo_yaml_files_parse(yaml_path):
	with open(yaml_path, "r", encoding="utf-8") as handle:
		try:
			list(yaml.safe_load_all(handle))
		except yaml.YAMLError as exc:
			msg = f"YAML parse error in {yaml_path}: {exc}"
			# Try to include 1-based location information when available.
			mark = getattr(exc, "problem_mark", None)
			if mark is not None:
				msg = f"{msg} (line {mark.line + 1}, column {mark.column + 1})"
			pytest.fail(msg)
