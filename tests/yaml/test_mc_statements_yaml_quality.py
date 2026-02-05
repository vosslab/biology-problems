from pathlib import Path

from lib_test_utils import import_from_repo_path, repo_abs_path


def _iter_yaml_files(rel_dir):
	root = Path(repo_abs_path(rel_dir))
	for pattern in ("*.yml", "*.yaml"):
		yield from root.rglob(pattern)


def test_mc_statements_yaml_quality():
	checker = import_from_repo_path("problems/multiple_choice_statements/check_mc_statements_yaml.py")
	errors = []
	for yaml_path in sorted(_iter_yaml_files("problems/multiple_choice_statements"), key=lambda p: str(p)):
		issues = checker.validate_yaml_path(yaml_path)
		for issue in issues:
			if issue.severity == "ERROR":
				errors.append(issue.format())
	assert errors == [], "MC statements YAML errors:\n" + "\n".join(errors)
