#!/usr/bin/env python3

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
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
	"description",
	"false_statements",
	"keywords",
	"learning_objective",
	"num_choices",
	"override_question_false",
	"override_question_true",
	"replacement_rules",
	"source",
	"TITLE",
	"title",
	"topic",
	"topic_tag",
	"true_statements",
}

DEFAULT_NUM_CHOICES = 5
STATEMENT_ID_RE = re.compile(r"(?P<kind>truth|false)(?P<group>[0-9]+)[a-z]?\Z")


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
	parser.add_argument(
		"-c", "--num-choices", type=int, default=None,
		help="Override the YAML setting; otherwise use its value or the default of 5.",
	)
	parser.set_defaults(recursive=False, quiet=False)
	args = parser.parse_args()
	if args.num_choices is not None and args.num_choices < 4:
		parser.error("--num-choices must be at least 4")
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


def _statement_group_ids(yaml_path, doc, issues):
	group_ids = {
		"true_statements": {},
		"false_statements": {},
	}
	for field, expected_kind in (
		("true_statements", "truth"),
		("false_statements", "false"),
	):
		statements = doc.get(field)
		if not isinstance(statements, dict):
			continue
		for statement_id in statements:
			if not isinstance(statement_id, str):
				continue
			match = STATEMENT_ID_RE.fullmatch(statement_id)
			if match is None or match.group("kind") != expected_kind:
				issues.append(
					YamlIssue(
						yaml_path=yaml_path,
						severity="ERROR",
						message=(
							f"`{field}` ID {statement_id!r} must use the `{expected_kind}` "
							"prefix and match <prefix><number>[a-z]"
						),
					)
				)
				continue
			group_ids[field][statement_id] = match.group("group")
	return group_ids


def _check_choice_capacity(yaml_path, doc, group_ids, num_choices):
	issues = []
	required_distractors = num_choices - 1
	forms = (
		("override_question_true", "TRUE", "true_statements", "false_statements"),
		("override_question_false", "FALSE", "false_statements", "true_statements"),
	)
	for override_key, form_name, correct_field, opposing_field in forms:
		if doc.get(override_key, "default") is None:
			continue
		correct_statements = doc.get(correct_field)
		opposing_statements = doc.get(opposing_field)
		if not isinstance(correct_statements, dict) or not isinstance(opposing_statements, dict):
			continue
		if (len(group_ids[correct_field]) != len(correct_statements)
			or len(group_ids[opposing_field]) != len(opposing_statements)):
			continue

		opposing_groups = set(group_ids[opposing_field].values())
		available_by_statement = {}
		for statement_id, group_id in group_ids[correct_field].items():
			available_groups = opposing_groups.difference({group_id})
			available_by_statement[statement_id] = len(available_groups)
		blocked = [
			group_count for group_count in available_by_statement.values()
			if group_count < required_distractors
		]
		if not blocked:
			continue

		maximum_for_all = min(available_by_statement.values()) + 1
		if len(blocked) == len(available_by_statement):
			scope = f"all {len(blocked)} {form_name}-form questions"
		else:
			scope = f"{len(blocked)} of {len(available_by_statement)} {form_name}-form questions"
		if maximum_for_all >= 4:
			action = f"run the generator with `-c {maximum_for_all}`"
		else:
			action = "add enough independent distractor groups to support four choices"
		issues.append(
			YamlIssue(
				yaml_path=yaml_path,
				severity="WARN",
				message=(
					f"{scope} cannot reach {num_choices} total choices: the form "
					f"needs {required_distractors} independent distractor groups per "
					f"item, but has at most {maximum_for_all - 1} per item "
					f"(supports {maximum_for_all} total choices); {action}"
				),
			)
		)
	return issues


def _validate_multiple_choice_statements_yaml(yaml_path, doc, num_choices):
	issues = []
	configured_num_choices = doc.get("num_choices", DEFAULT_NUM_CHOICES)
	if "num_choices" in doc and (
		not isinstance(configured_num_choices, int)
		or isinstance(configured_num_choices, bool)
		or configured_num_choices < 4
	):
		issues.append(
			YamlIssue(
				yaml_path=yaml_path,
				severity="ERROR",
				message="`num_choices` must be an integer of at least 4",
			)
		)
		configured_num_choices = DEFAULT_NUM_CHOICES
	if num_choices is None:
		num_choices = configured_num_choices

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

	group_ids = _statement_group_ids(yaml_path, doc, issues)
	issues.extend(_check_choice_capacity(yaml_path, doc, group_ids, num_choices))

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


def _quality_check_docs(yaml_path, docs, raw_text, num_choices):
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
	issues.extend(_validate_multiple_choice_statements_yaml(yaml_path, doc, num_choices))
	return issues


def validate_yaml_path(yaml_path, num_choices=None):
	raw_text = yaml_path.read_text(encoding="utf-8")
	docs = _parse_yaml_all_docs(yaml_path, raw_text)
	return _quality_check_docs(yaml_path, docs, raw_text, num_choices)


def main():
	args = parse_args()
	yaml_files = iter_yaml_files(args.paths, args.recursive)
	errors = 0
	warnings = 0
	for yaml_path in yaml_files:
		issues = validate_yaml_path(yaml_path, num_choices=args.num_choices)
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
