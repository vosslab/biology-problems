#!/usr/bin/env python3

import argparse
from dataclasses import dataclass
import os
from pathlib import Path
import sys
import pprint

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


def parse_args():
	"""
	Parse command-line arguments.
	"""
	parser = argparse.ArgumentParser(
		description="Validate YAML files and report errors."
	)
	parser.add_argument(
		"paths",
		nargs="+",
		help="YAML file(s) to validate, or directories (use --recursive to scan).",
	)
	parser.add_argument(
		"-r", "--recursive", dest="recursive", action="store_true",
		help="If a path is a directory, scan it recursively for *.yml and *.yaml files.",
	)
	parser.add_argument(
		"-p", "--print", dest="print_data", action="store_true",
		help="Pretty-print parsed YAML content (can be verbose).",
	)
	parser.add_argument(
		"--no-print", dest="print_data", action="store_false",
		help="Do not pretty-print parsed YAML content.",
	)
	parser.add_argument(
		"-q", "--quiet", dest="quiet", action="store_true",
		help="Only print errors (suppress OK lines).",
	)
	parser.add_argument(
		"-s", "--strict", dest="strict", action="store_true",
		help="Treat warnings as errors (exit nonzero if any warnings are found).",
	)
	parser.set_defaults(recursive=False, print_data=False, quiet=False, strict=False)
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
				raise ValueError(
					f"Directory given without --recursive: {path_obj}"
				)
			for pattern in ("*.yml", "*.yaml"):
				yaml_files.extend(path_obj.rglob(pattern))
			continue
		raise FileNotFoundError(f"Path not found: {path_obj}")

	yaml_files_sorted = sorted({p.resolve() for p in yaml_files}, key=lambda p: str(p))
	return yaml_files_sorted


def _is_under_dir(yaml_path, first_dir):
	try:
		parts = yaml_path.resolve().parts
	except FileNotFoundError:
		return False
	return first_dir in parts


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

	matching_pairs = doc.get("matching pairs", None)
	if not isinstance(matching_pairs, dict):
		issues.append(
			YamlIssue(
				yaml_path=yaml_path,
				severity="ERROR",
				message="`matching pairs` must be a mapping",
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


def _validate_multiple_choice_statements_yaml(yaml_path, doc):
	issues = []

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
					message="`topic` is ~/empty; consider setting it for discoverability",
				)
			)

	connection_words = doc.get("connection_words", None)
	if connection_words is not None and not isinstance(connection_words, (list, str)):
		issues.append(
			YamlIssue(
				yaml_path=yaml_path,
				severity="ERROR",
				message="`connection_words` must be ~, a string, or a list",
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
				message="`conflict_rules` must be ~, a mapping, or a list when present",
			)
		)

	return issues


def _quality_check_docs(yaml_path, docs, raw_text):
	issues = []
	issues.extend(_check_for_leading_tabs(yaml_path, raw_text))

	resolved = yaml_path.resolve()
	is_matching_set = _is_under_dir(resolved, "matching_sets")
	is_mc_statements = _is_under_dir(resolved, "multiple_choice_statements")

	if is_matching_set or is_mc_statements:
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
		if is_matching_set:
			issues.extend(_validate_matching_sets_yaml(yaml_path, doc))
		if is_mc_statements:
			issues.extend(_validate_multiple_choice_statements_yaml(yaml_path, doc))

	return issues


def read_yaml_file(yaml_path):
	raw_text = Path(yaml_path).read_text(encoding="utf-8")
	docs = _parse_yaml_all_docs(Path(yaml_path), raw_text)
	issues = _quality_check_docs(Path(yaml_path), docs, raw_text)
	return docs, issues


def main():
	args = parse_args()

	try:
		yaml_files = iter_yaml_files(args.paths, recursive=args.recursive)
	except (FileNotFoundError, ValueError) as exc:
		print(f"ERROR: {exc}", file=sys.stderr)
		return 2

	if len(yaml_files) == 0:
		print("ERROR: no YAML files found", file=sys.stderr)
		return 2

	def safe_print_stdout(message):
		try:
			print(message)
		except BrokenPipeError:
			try:
				sys.stdout = open(os.devnull, "w")
			except Exception:
				return

	had_error = False
	had_warning = False
	for yaml_path in yaml_files:
		try:
			docs, issues = read_yaml_file(yaml_path)
		except ValueError as exc:
			had_error = True
			print(f"ERROR: {yaml_path}: {exc}", file=sys.stderr)
			continue

		for issue in issues:
			if issue.severity == "WARN":
				had_warning = True
				if not args.quiet:
					safe_print_stdout(issue.format())
			else:
				had_error = True
				print(issue.format(), file=sys.stderr)

		if args.print_data:
			pprint.pprint(docs[0] if len(docs) == 1 else docs)

		if not args.quiet:
			safe_print_stdout(f"OK: {yaml_path}")

	if had_error:
		return 1
	if had_warning and args.strict:
		return 1
	return 0


if __name__ == "__main__":
	sys.exit(main())
