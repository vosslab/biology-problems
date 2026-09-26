from pathlib import Path

import yaml

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


def _exclude_pair_set(doc):
	excluded = set()
	for key in ("exclude pairs", "exclude_pairs"):
		raw_pairs = doc.get(key)
		if not raw_pairs:
			continue
		for pair in raw_pairs:
			if isinstance(pair, (list, tuple)) and len(pair) == 2:
				excluded.add(tuple(sorted((str(pair[0]), str(pair[1])))))
	return excluded


def test_matching_choices_are_not_reused_across_prompts():
	"""A choice may be shared only by prompts that an exclude pair keeps apart."""
	failures = []
	for yaml_path in sorted(_iter_yaml_files("problems/matching_sets"), key=lambda p: str(p)):
		doc = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
		if not isinstance(doc, dict):
			continue
		pairs = doc.get("matching pairs")
		if not isinstance(pairs, dict):
			continue
		excluded = _exclude_pair_set(doc)
		choice_prompts = {}
		for prompt, value in pairs.items():
			if not isinstance(prompt, str):
				continue
			choices = value if isinstance(value, list) else [value]
			for choice in choices:
				if isinstance(choice, str):
					choice_prompts.setdefault(choice, set()).add(prompt)
		for choice, prompts in choice_prompts.items():
			prompt_list = sorted(prompts)
			for index, left in enumerate(prompt_list):
				for right in prompt_list[index + 1:]:
					if tuple(sorted((left, right))) not in excluded:
						failures.append(
							f"{yaml_path.name}: {choice!r} is a choice for both {left!r} and {right!r}"
						)
	assert failures == [], "Reused matching choices:\n" + "\n".join(failures)


def test_exclude_pairs_are_fewer_than_prompts():
	"""Exclude pairs stay minimal. A long list means the prompts and choices were flipped."""
	failures = []
	for yaml_path in sorted(_iter_yaml_files("problems/matching_sets"), key=lambda p: str(p)):
		doc = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
		if not isinstance(doc, dict):
			continue
		pairs = doc.get("matching pairs")
		if not isinstance(pairs, dict) or len(pairs) == 0:
			continue
		for key in ("exclude pairs", "exclude_pairs"):
			raw_pairs = doc.get(key)
			if not isinstance(raw_pairs, list):
				continue
			if len(raw_pairs) >= len(pairs):
				failures.append(
					f"{yaml_path.name}: {len(raw_pairs)} exclude pairs for {len(pairs)} prompts"
				)
	assert failures == [], "Exclude pairs are not fewer than prompts:\n" + "\n".join(failures)
