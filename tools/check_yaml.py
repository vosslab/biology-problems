#!/usr/bin/env python3

import argparse
from pathlib import Path
import sys
import pprint

# PIP3 modules
import yaml


def parse_args():
	"""
	Parse command-line arguments.
	"""
	parser = argparse.ArgumentParser(
		description="Validate YAML files (optionally pretty-print the parsed data)."
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
	parser.set_defaults(recursive=False, print_data=None, quiet=False)
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


def read_yaml_file(yaml_path):
	with open(yaml_path, "r", encoding="utf-8") as yaml_pointer:
		try:
			docs = list(yaml.safe_load_all(yaml_pointer))
		except yaml.YAMLError as exc:
			raise ValueError(f"YAML parse error: {exc}") from exc
	return docs


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

	print_data = args.print_data
	if print_data is None:
		print_data = (len(yaml_files) == 1)

	had_error = False
	for yaml_path in yaml_files:
		try:
			docs = read_yaml_file(yaml_path)
		except ValueError as exc:
			had_error = True
			print(f"ERROR: {yaml_path}: {exc}", file=sys.stderr)
			continue

		if print_data:
			pprint.pprint(docs[0] if len(docs) == 1 else docs)

		if not args.quiet:
			print(f"OK: {yaml_path}")

	return 1 if had_error else 0


if __name__ == "__main__":
	sys.exit(main())
