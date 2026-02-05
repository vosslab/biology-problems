#!/usr/bin/env python3

import argparse
from dataclasses import dataclass
from pathlib import Path
import sys

# PIP3 modules
import yaml


@dataclass(frozen=True)
class YamlIssue:
	yaml_path: Path
	severity: str
	message: str
	line: int | None = None

	def format(self) -> str:
		if self.line is None:
			return f"{self.severity}: {self.yaml_path}: {self.message}"
		return f"{self.severity}: {self.yaml_path}:{self.line}: {self.message}"


class UniqueKeyLoader(yaml.SafeLoader):
	pass


def _construct_mapping_no_duplicates(loader, node, deep=False):
	mapping = {}
	for key_node, value_node in node.value:
		key = loader.construct_object(key_node, deep=deep)
		if key in mapping:
			raise yaml.constructor.ConstructorError(
				"while constructing a mapping",
				node.start_mark,
				f"found duplicate key: {key!r}",
				key_node.start_mark,
			)
		value = loader.construct_object(value_node, deep=deep)
		mapping[key] = value
	return mapping


UniqueKeyLoader.add_constructor(
	yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
	_construct_mapping_no_duplicates,
)


ALLOWED_KEYS = {
	"dbsubject",
	"exclude pairs",
	"items to match per question",
	"key description",
	"keys description",
	"learning_objective",
	"matching pairs",
	"question override",
	"replacement_rules",
	"source",
	"topic",
	"topic_tag",
	"value description",
	"values description",
}


def parse_args():
	parser = argparse.ArgumentParser(
		description="Strictly validate matching_sets YAML files."
	)
	parser.add_argument(
		"paths",
		nargs="+",
		help="YAML file(s) to validate, or directories (use --recursive).",
	)
	parser.add_argument(
		"-r", "--recursive", dest="recursive", action="store_true",
		help="If a path is a directory, scan it recursively for *.yml and *.yaml files.",
	)
	parser.add_argument(
		"-q", "--quiet", dest="quiet", action="store_true",
		help="Only print errors (suppress OK lines).",
	)
	parser.set_defaults(recursive=False, quiet=False)
	args = parser.parse_args()
	return args


def iter_yaml_files(paths_list, recursive):
	yaml_files = []
	for path_str in paths_list:
		path_obj = Path(path_str)
		if path_obj.is_file():
			yaml_files.append(path_obj)
			continue
		if path_obj.is_dir():
			if not recursive:
				raise ValueError(f"Directory given without --recursive: {path_obj}")
			for pattern in ("*.yml", "*.yaml"):
				yaml_files.extend(path_obj.rglob(pattern))
			continue
		raise FileNotFoundError(f"Path not found: {path_obj}")

	yaml_files_sorted = sorted({p.resolve() for p in yaml_files}, key=lambda p: str(p))
	return yaml_files_sorted


def _check_for_leading_tabs(yaml_path, raw_text):
	issues = []
	for line_num, line in enumerate(raw_text.splitlines(), start=1):
		if line.startswith("\t"):
			issues.append(
				YamlIssue(
					yaml_path=yaml_path,
					severity="ERROR",
					message="leading tab indentation is not allowed in YAML",
					line=line_num,
				)
			)
	return issues


def _parse_yaml_all_docs(yaml_path, raw_text):
	try:
		return list(yaml.load_all(raw_text, Loader=UniqueKeyLoader))
	except yaml.YAMLError as exc:
		raise ValueError(f"YAML parse error: {exc}") from exc


def _validate_matching_sets_yaml(yaml_path, doc):
	issues = []

	unknown_keys = sorted({k for k in doc.keys() if k not in ALLOWED_KEYS})
	if unknown_keys:
		issues.append(
			YamlIssue(
				yaml_path=yaml_path,
				severity="ERROR",
				message=f"unknown top-level keys: {unknown_keys}",
			)
		)

	matching_pairs = doc.get("matching pairs", None)
	if not isinstance(matching_pairs, dict) or len(matching_pairs) == 0:
		issues.append(
			YamlIssue(
				yaml_path=yaml_path,
				severity="ERROR",
				message="`matching pairs` must be a non-empty mapping",
			)
		)
		return issues

	if doc.get("question override", None) is None:
		for required_key in ("keys description", "values description"):
			if required_key not in doc or not isinstance(doc.get(required_key), str) or doc.get(required_key).strip() == "":
				issues.append(
					YamlIssue(
						yaml_path=yaml_path,
						severity="ERROR",
						message=f"missing or empty `{required_key}` (required unless `question override` is set)",
					)
				)

	items_to_match = doc.get("items to match per question", None)
	if items_to_match is not None:
		if not isinstance(items_to_match, int) or items_to_match <= 0:
			issues.append(
				YamlIssue(
					yaml_path=yaml_path,
					severity="ERROR",
					message="`items to match per question` must be a positive integer",
				)
			)
		elif items_to_match > len(matching_pairs):
			issues.append(
				YamlIssue(
					yaml_path=yaml_path,
					severity="WARN",
					message="`items to match per question` exceeds the number of keys in `matching pairs`",
				)
			)

	replacement_rules = doc.get("replacement_rules", None)
	if replacement_rules is not None and not isinstance(replacement_rules, dict):
		issues.append(
			YamlIssue(
				yaml_path=yaml_path,
				severity="ERROR",
				message="`replacement_rules` must be a mapping when present",
			)
		)

	exclude_pairs = doc.get("exclude pairs", None)
	if exclude_pairs is not None:
		if not isinstance(exclude_pairs, list):
			issues.append(
				YamlIssue(
					yaml_path=yaml_path,
					severity="ERROR",
					message="`exclude pairs` must be a list when present",
				)
			)
		else:
			for idx, pair in enumerate(exclude_pairs, start=1):
				if not isinstance(pair, (list, tuple)) or len(pair) != 2:
					issues.append(
						YamlIssue(
							yaml_path=yaml_path,
							severity="ERROR",
							message=f"`exclude pairs` entry {idx} must be a 2-item list",
						)
					)

	for key, value in matching_pairs.items():
		if isinstance(key, str):
			if key.strip() != key:
				issues.append(
					YamlIssue(
						yaml_path=yaml_path,
						severity="WARN",
						message=f"`matching pairs` key has leading/trailing whitespace: {key!r}",
					)
				)
		elif not isinstance(key, list):
			issues.append(
				YamlIssue(
					yaml_path=yaml_path,
					severity="ERROR",
					message="`matching pairs` keys must be strings (or a list of strings)",
				)
			)

		if isinstance(value, str):
			if value.strip() == "":
				issues.append(
					YamlIssue(
						yaml_path=yaml_path,
						severity="ERROR",
						message="`matching pairs` values must not be empty strings",
					)
				)
		elif isinstance(value, list):
			if len(value) == 0:
				issues.append(
					YamlIssue(
						yaml_path=yaml_path,
						severity="ERROR",
						message="`matching pairs` list values must be non-empty",
					)
				)
			elif any((not isinstance(v, str) or v.strip() == "") for v in value):
				issues.append(
					YamlIssue(
						yaml_path=yaml_path,
						severity="ERROR",
						message="`matching pairs` list values must be non-empty strings",
					)
				)
		else:
			issues.append(
				YamlIssue(
					yaml_path=yaml_path,
					severity="ERROR",
					message="`matching pairs` values must be a string or list of strings",
				)
			)

	return issues


def _quality_check_docs(yaml_path, docs, raw_text):
	issues = []
	issues.extend(_check_for_leading_tabs(yaml_path, raw_text))
	if len(docs) != 1:
		issues.append(
			YamlIssue(
				yaml_path=yaml_path,
				severity="ERROR",
				message="expected exactly one YAML document",
			)
		)
		return issues
	doc = docs[0]
	if not isinstance(doc, dict):
		issues.append(
			YamlIssue(
				yaml_path=yaml_path,
				severity="ERROR",
				message="top-level YAML must be a mapping",
			)
		)
		return issues
	issues.extend(_validate_matching_sets_yaml(yaml_path, doc))
	return issues


def validate_yaml_path(yaml_path):
	raw_text = yaml_path.read_text(encoding="utf-8")
	docs = _parse_yaml_all_docs(yaml_path, raw_text)
	return _quality_check_docs(yaml_path, docs, raw_text)


def main():
	args = parse_args()
	yaml_files = iter_yaml_files(args.paths, args.recursive)
	errors = 0
	warnings = 0
	for yaml_path in yaml_files:
		issues = validate_yaml_path(yaml_path)
		if not issues:
			if not args.quiet:
				print(f"OK: {yaml_path}")
			continue
		for issue in issues:
			if issue.severity == "ERROR":
				errors += 1
			else:
				warnings += 1
			print(issue.format())
	if errors > 0 or warnings > 0:
		print(f"Found {errors} errors and {warnings} warnings")
	if errors > 0:
		sys.exit(1)


if __name__ == "__main__":
	main()
