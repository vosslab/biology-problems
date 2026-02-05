from pathlib import Path

from lib_test_utils import import_from_repo_path, repo_abs_path


def _iter_yaml_files(rel_dir):
	root = Path(repo_abs_path(rel_dir))
	for pattern in ("*.yml", "*.yaml"):
		yield from root.rglob(pattern)


def test_matching_sets_yaml_quality():
	checker = import_from_repo_path("problems/matching_sets/check_matching_yaml.py")
	errors = []
	for yaml_path in sorted(_iter_yaml_files("problems/matching_sets"), key=lambda p: str(p)):
		issues = checker.validate_yaml_path(yaml_path)
		for issue in issues:
			if issue.severity == "ERROR":
				errors.append(issue.format())
	assert errors == [], "Matching sets YAML errors:\n" + "\n".join(errors)
