#!/usr/bin/env python3

"""Find YAML content banks not yet assigned to any bbq_control task CSV.

Companion to find_unassigned_scripts.py. Operates on the YAML universe under
problems/multiple_choice_statements/*/*.yml and
problems/matching_sets/*/*.yml. Uses the same notion of "assigned":
a yaml is considered assigned if its path appears in the `input`
column of any task CSV.

For each unassigned YAML, aggregate subject/topic votes from all
topic_classifier/results-*/ directories (limited to entries whose
script-column path ends with .yml/.yaml, which captures
results-yaml*/ runs from classify_yaml.py). No LLM calls.
"""

# Standard Library
import os
import csv
import glob
import argparse

# local repo modules
import script_runner_lib as script_runner
import classify_yaml
import compare_results
import find_unassigned_scripts as find_unassigned


DEFAULT_TASK_DIR = (
	"/Users/vosslab/nsh/PROBLEMS/biology-problems-website/"
	"bbq_control/task_files"
)

YAML_SUFFIXES = (".yml", ".yaml")


#============================================
def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments."""
	parser = argparse.ArgumentParser(
		description=(
			"Find YAML content banks not yet assigned to any "
			"bbq_control task CSV and suggest assignments from "
			"classifier results."
		),
	)
	parser.add_argument(
		"-t", "--task-dir", dest="task_dir",
		default=DEFAULT_TASK_DIR,
		help="Directory containing bbq_control task CSVs.",
	)
	parser.add_argument(
		"-b", "--base-dir", dest="base_dir",
		default=os.path.dirname(os.path.abspath(__file__)),
		help="Directory containing results-*/ folders.",
	)
	parser.add_argument(
		"-o", "--output", dest="output_file",
		default="unassigned_yaml_report.csv",
		help="Path to write the report CSV.",
	)
	parser.add_argument(
		"-m", "--min-votes", dest="min_votes",
		type=int, default=0,
		help="Only include rows where total model votes >= this.",
	)
	parser.add_argument(
		"-l", "--limit", dest="limit",
		type=int, default=0,
		help="Cap printed rows for quick triage (0 = no cap).",
	)
	args = parser.parse_args()
	return args


#============================================
def _is_yaml_path(path: str) -> bool:
	"""Return True when the path string ends with a YAML extension."""
	lower = path.lower()
	matched = lower.endswith(YAML_SUFFIXES)
	return matched


# Simple assert for _is_yaml_path
assert _is_yaml_path("foo.yml") is True
assert _is_yaml_path("FOO.YAML") is True
assert _is_yaml_path("foo.py") is False


#============================================
def load_assigned_yaml(task_dir: str) -> dict:
	"""Collect already-assigned YAMLs from bbq_control task CSVs.

	Args:
		task_dir: directory containing *.csv task files

	Returns:
		dict mapping normalized {bp_root}/... yaml path to a list of
		(subject, topic, source_csv_basename) tuples (a yaml may
		appear more than once legitimately)
	"""
	assigned: dict = {}
	pattern = os.path.join(task_dir, "*.csv")
	for csv_path in sorted(glob.glob(pattern)):
		source_name = os.path.basename(csv_path)
		with open(csv_path, "r") as handle:
			reader = csv.DictReader(handle)
			for row in reader:
				# 'input' is the column that holds yaml paths
				raw_input = (row.get("input") or "").strip()
				if not raw_input:
					continue
				if raw_input.startswith("#"):
					continue
				if not _is_yaml_path(raw_input):
					continue
				# Always normalize - do not trust that the CSV value
				# is already in {bp_root}/... form
				norm_path = compare_results._to_bp_root(raw_input)
				subject = (row.get("subject") or "").strip()
				topic = (row.get("topic") or "").strip()
				assigned.setdefault(norm_path, []).append(
					(subject, topic, source_name)
				)
	return assigned


#============================================
def load_yaml_classifier_votes(base_dir: str) -> tuple:
	"""Aggregate yaml subject/topic votes across results-*/ dirs.

	Mirrors find_unassigned.load_classifier_votes but inverts the
	filter: only entries whose script path ends with .yml/.yaml are
	counted. This naturally captures results-yaml*/ directories.

	Args:
		base_dir: directory containing results-*/ folders

	Returns:
		tuple (subject_votes, topic_votes, models_seen)
	"""
	subject_votes: dict = {}
	topic_votes: dict = {}
	models_seen = []
	pattern = os.path.join(base_dir, "results-*/")
	for dir_path in sorted(glob.glob(pattern)):
		if not os.path.isdir(dir_path):
			continue
		model_name = os.path.basename(dir_path.rstrip("/")).replace(
			"results-", ""
		)
		assignments = compare_results.load_results_dir(dir_path)
		if not assignments:
			continue
		# Did this directory contribute any yaml votes?
		contributed = False
		for raw_script, (chapter, topic) in assignments.items():
			# Filter: only yaml entries
			if not _is_yaml_path(raw_script):
				continue
			# Normalize so it matches universe + assigned keys
			norm_path = compare_results._to_bp_root(raw_script)
			chapter = chapter.strip()
			topic = topic.strip()
			if not chapter:
				continue
			subj_bucket = subject_votes.setdefault(norm_path, {})
			subj_bucket[chapter] = subj_bucket.get(chapter, 0) + 1
			topic_bucket = topic_votes.setdefault(norm_path, {})
			key = (chapter, topic)
			topic_bucket[key] = topic_bucket.get(key, 0) + 1
			contributed = True
		if contributed:
			models_seen.append(model_name)
	return subject_votes, topic_votes, sorted(models_seen)


#============================================
def main() -> None:
	args = parse_args()

	repo_root = script_runner.get_repo_root()

	# 1. Build yaml universe via classify_yaml's discovery helper
	rel_yaml_paths = classify_yaml.discover_yaml_files(repo_root)
	universe = set()
	for rel_path in rel_yaml_paths:
		# rel_path is repo-relative, e.g. 'problems/matching_sets/.../foo.yml'
		bp_path = compare_results._to_bp_root(rel_path)
		universe.add(bp_path)

	# 2. Load assigned yamls from task CSVs
	assigned = load_assigned_yaml(args.task_dir)

	# 3. Unassigned = universe - assigned
	unassigned = sorted(universe - set(assigned.keys()))

	# 4. Load classifier votes (yaml-only entries)
	subject_votes, topic_votes, models = load_yaml_classifier_votes(
		args.base_dir
	)

	# 5. Build rows by reusing find_unassigned.compute_suggestion
	rows = []
	for yaml_path in unassigned:
		row = find_unassigned.compute_suggestion(
			yaml_path, subject_votes, topic_votes
		)
		if row["total_models"] < args.min_votes:
			continue
		rows.append(row)

	rows = find_unassigned.sort_rows(rows)

	# 6. Write CSV (same schema as the .py companion)
	find_unassigned.write_report(rows, args.output_file)

	# 7. Console output
	topic_lookup = compare_results.build_topic_lookup()

	print(f"Task CSV dir: {args.task_dir}")
	print(f"Results base: {args.base_dir}")
	print(f"Models loaded: {len(models)}  ({', '.join(models) or '-'})")
	print(f"Universe of YAML files: {len(universe)}")
	print(f"Already assigned: {len(assigned)}")
	print(f"Unassigned: {len(unassigned)}")
	print(
		f"Rows in report (after --min-votes={args.min_votes}): "
		f"{len(rows)}"
	)

	find_unassigned.print_console_table(rows, topic_lookup, args.limit)

	counts = {
		find_unassigned.CONF_HIGH: 0,
		find_unassigned.CONF_MEDIUM: 0,
		find_unassigned.CONF_LOW: 0,
		find_unassigned.CONF_NONE: 0,
	}
	for row in rows:
		counts[row["confidence"]] = counts.get(row["confidence"], 0) + 1
	print()
	print(
		f"Summary: HIGH={counts[find_unassigned.CONF_HIGH]}  "
		f"MEDIUM={counts[find_unassigned.CONF_MEDIUM]}  "
		f"LOW={counts[find_unassigned.CONF_LOW]}  "
		f"NONE={counts[find_unassigned.CONF_NONE]}"
	)
	print(f"Report written to: {args.output_file}")


if __name__ == "__main__":
	main()
