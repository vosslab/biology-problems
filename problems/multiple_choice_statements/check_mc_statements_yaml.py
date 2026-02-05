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
	"conflict_rules",
	"connection_words",
	"dbsubject",
	"false_statements",
	"learning_objective",
	"override_question_false",
	"override_question_true",
	"replacement_rules",
	"source",
	"topic",
	"topic_tag",
	"true_statements",
}


def parse_args():
	parser = argparse.ArgumentParser(
		description="Strictly validate multiple_choice_statements YAML files."
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


def _validate_multiple_choice_statements_yaml(yaml_path, doc):
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

	topic = doc.get("topic", None)
	override_true = doc.get("override_question_true", None)
	override_false = doc.get("override_question_false", None)

	topic_is_missing = (topic is None or (isinstance(topic, str) and topic.strip() == ""))
	if topic_is_missing:
		has_override = False
		for override_val in (override_true, override_false):
			if isinstance(override_val, str) and override_val.strip() != "":
				has_override = True
				break
		if not has_override:
			issues.append(
				YamlIssue(
					yaml_path=yaml_path,
					severity="ERROR",
					message="missing `topic` and no override question provided",
				)
			)
		else:
			issues.append(
				YamlIssue(
					yaml_path=yaml_path,
					severity="WARN",
					message="`topic` is empty; consider setting it for discoverability",
				)
			)

	connection_words = doc.get("connection_words", None)
	if connection_words is not None and not isinstance(connection_words, (list, str)):
		issues.append(
			YamlIssue(
				yaml_path=yaml_path,
				severity="ERROR",
				message="`connection_words` must be null, a string, or a list",
			)
		)

	for field in ("true_statements", "false_statements"):
		val = doc.get(field, None)
		if not isinstance(val, dict) or len(val) == 0:
			issues.append(
				YamlIssue(
					yaml_path=yaml_path,
					severity="ERROR",
					message=f"missing or empty `{field}` mapping",
				)
			)
			continue
		for stmt_key, stmt_text in val.items():
			if not isinstance(stmt_key, str) or stmt_key.strip() == "":
				issues.append(
					YamlIssue(
						yaml_path=yaml_path,
						severity="ERROR",
						message=f"`{field}` keys must be non-empty strings",
					)
				)
				break
			if not isinstance(stmt_text, str) or stmt_text.strip() == "":
				issues.append(
					YamlIssue(
						yaml_path=yaml_path,
						severity="ERROR",
						message=f"`{field}` values must be non-empty strings",
					)
				)
				break

	replacement_rules = doc.get("replacement_rules", None)
	if replacement_rules is not None and not isinstance(replacement_rules, dict):
		issues.append(
			YamlIssue(
				yaml_path=yaml_path,
				severity="ERROR",
				message="`replacement_rules` must be a mapping when present",
			)
		)

	conflict_rules = doc.get("conflict_rules", None)
	if conflict_rules is not None and not isinstance(conflict_rules, (dict, list)):
		issues.append(
			YamlIssue(
				yaml_path=yaml_path,
				severity="ERROR",
				message="`conflict_rules` must be null, a mapping, or a list when present",
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
	issues.extend(_validate_multiple_choice_statements_yaml(yaml_path, doc))
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
