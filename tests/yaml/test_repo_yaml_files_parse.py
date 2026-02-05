
import os
import sys
from pathlib import Path

import pytest

import yaml

def _ensure_qti_package_maker_on_path():
	repo_root = Path(__file__).resolve().parents[2]
	sibling_root = repo_root.parent
	candidate = sibling_root / "qti_package_maker"
	if candidate.is_dir():
		sys.path.insert(0, str(candidate))


_ensure_qti_package_maker_on_path()

import bptools


def _iter_repo_yaml_files():
	repo_roots = (Path("data"), Path("problems"))
	for repo_root in repo_roots:
		if not repo_root.is_dir():
			continue
		for pattern in ("*.yml", "*.yaml"):
			yield from repo_root.rglob(pattern)


_YAML_FILES = sorted(_iter_repo_yaml_files(), key=lambda p: str(p))

_SAFE_LOAD_ONLY = {
	"data/pubchem_molecules_data.yml",
	"problems/biochemistry-problems/PUBCHEM/cache_pubchem_molecules.yml",
}


@pytest.mark.parametrize("yaml_path", _YAML_FILES)
def test_repo_yaml_files_parse(yaml_path):
	rel_path = yaml_path.as_posix()
	if rel_path in _SAFE_LOAD_ONLY:
		with open(yaml_path, "r", encoding="utf-8") as handle:
			try:
				list(yaml.safe_load_all(handle))
			except yaml.YAMLError as exc:
				msg = f"YAML parse error in {yaml_path}: {exc}"
				mark = getattr(exc, "problem_mark", None)
				if mark is not None:
					msg = f"{msg} (line {mark.line + 1}, column {mark.column + 1})"
				pytest.fail(msg)
		return

	try:
		bptools.readYamlFile(os.fspath(yaml_path))
	except Exception as exc:
		msg = f"YAML parse error in {yaml_path}: {exc}"
		pytest.fail(msg)
