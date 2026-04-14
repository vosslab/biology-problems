#!/usr/bin/env python3

"""Find generator scripts not yet assigned to any bbq_control task CSV.

For each unassigned script, aggregate subject/topic votes from all
topic_classifier/results-*/ directories and suggest where it probably
belongs. No LLM calls; pure reader over existing classifier output.
"""

# Standard Library
import os
import csv
import math
import glob
import argparse

# PIP3 modules
import tabulate

# local repo modules
import script_runner
import compare_results


DEFAULT_TASK_DIR = (
	"/Users/vosslab/nsh/PROBLEMS/biology-problems-website/"
	"bbq_control/task_files"
)

# Script-column sentinels in task CSVs that are not real script paths
NON_SCRIPT_MARKERS = {"YMATCH", "YMCS"}

# Confidence labels
CONF_HIGH = "HIGH"
CONF_MEDIUM = "MEDIUM"
CONF_LOW = "LOW"
CONF_NONE = "NONE"

CONF_ORDER = {CONF_HIGH: 0, CONF_MEDIUM: 1, CONF_LOW: 2, CONF_NONE: 3}


#============================================
def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments."""
	parser = argparse.ArgumentParser(
		description=(
			"Find generator scripts not yet assigned to any "
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
		default="unassigned_report.csv",
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
def load_assigned_scripts(task_dir: str) -> dict:
	"""Collect already-assigned scripts from bbq_control task CSVs.

	Args:
		task_dir: directory containing *.csv task files

	Returns:
		dict mapping bp_root-prefixed script path to a list of
		(subject, topic, source_filename) tuples (a script may appear
		more than once legitimately)
	"""
	assigned = {}
	pattern = os.path.join(task_dir, "*.csv")
	for csv_path in sorted(glob.glob(pattern)):
		source_name = os.path.basename(csv_path)
		with open(csv_path, "r") as handle:
			reader = csv.DictReader(handle)
			for row in reader:
				script = (row.get("script") or "").strip()
				if not script:
					continue
				if script in NON_SCRIPT_MARKERS:
					continue
				if script.startswith("#"):
					continue
				subject = (row.get("subject") or "").strip()
				topic = (row.get("topic") or "").strip()
				assigned.setdefault(script, []).append(
					(subject, topic, source_name)
				)
	return assigned


#============================================
def load_classifier_votes(base_dir: str) -> tuple:
	"""Aggregate subject/topic votes across results-*/ directories.

	Args:
		base_dir: directory containing results-*/ folders

	Returns:
		tuple (subject_votes, topic_votes, models_seen)
		- subject_votes: {script: {subject: count}}
		- topic_votes: {script: {(subject, topic): count}}
		- models_seen: sorted list of model names that were loaded
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
		# Skip yaml-only result dirs for this tool's purpose
		# (we classify scripts here, not yaml content)
		if model_name.startswith("yaml-"):
			continue
		assignments = compare_results.load_results_dir(dir_path)
		if not assignments:
			continue
		models_seen.append(model_name)
		for raw_script, (chapter, topic) in assignments.items():
			# Normalize to {bp_root}/... form for comparison with task CSVs
			norm_script = compare_results._to_bp_root(raw_script)
			chapter = chapter.strip()
			topic = topic.strip()
			if not chapter:
				continue
			subj_bucket = subject_votes.setdefault(norm_script, {})
			subj_bucket[chapter] = subj_bucket.get(chapter, 0) + 1
			topic_bucket = topic_votes.setdefault(norm_script, {})
			key = (chapter, topic)
			topic_bucket[key] = topic_bucket.get(key, 0) + 1
	return subject_votes, topic_votes, sorted(models_seen)


#============================================
def format_votes(vote_dict: dict) -> str:
	"""Compact votes as 'key:count;key:count' sorted by count desc."""
	if not vote_dict:
		return ""
	pairs = sorted(
		vote_dict.items(),
		key=lambda kv: (-kv[1], str(kv[0])),
	)
	parts = []
	for key, count in pairs:
		if isinstance(key, tuple):
			label = "/".join(str(part) for part in key)
		else:
			label = str(key)
		parts.append(f"{label}:{count}")
	joined = ";".join(parts)
	return joined


# Simple assert for format_votes
assert format_votes({}) == ""
assert format_votes({"a": 3, "b": 1}) == "a:3;b:1"
assert format_votes({("x", "t1"): 2}) == "x/t1:2"


#============================================
def compute_suggestion(
	script: str,
	subject_votes: dict,
	topic_votes: dict,
) -> dict:
	"""Build one report row for a single unassigned script.

	Args:
		script: bp_root-prefixed script path
		subject_votes: full {script: {subject: count}} mapping
		topic_votes: full {script: {(subject, topic): count}} mapping

	Returns:
		dict with report columns
	"""
	subj_bucket = subject_votes.get(script, {})
	topic_bucket = topic_votes.get(script, {})
	total_models = sum(subj_bucket.values())

	if total_models == 0:
		row = {
			"script": script,
			"top_subject": "",
			"top_topic": "",
			"subject_votes": "",
			"topic_votes": "",
			"total_models": 0,
			"agreement_score": 0.0,
			"confidence": CONF_NONE,
			"runner_up_subject": "",
			"runner_up_votes": 0,
		}
		return row

	# Rank subjects by vote count, break ties alphabetically
	ranked_subjects = sorted(
		subj_bucket.items(),
		key=lambda kv: (-kv[1], kv[0]),
	)
	top_subject, top_subject_votes = ranked_subjects[0]
	runner_up_subject = ""
	runner_up_votes = 0
	if len(ranked_subjects) > 1:
		runner_up_subject, runner_up_votes = ranked_subjects[1]

	# Top topic is the most-voted (subject, topic) whose subject matches top_subject
	topics_in_top = {
		key[1]: count
		for key, count in topic_bucket.items()
		if key[0] == top_subject
	}
	if topics_in_top:
		ranked_topics = sorted(
			topics_in_top.items(),
			key=lambda kv: (-kv[1], kv[0]),
		)
		top_topic, top_topic_votes = ranked_topics[0]
	else:
		top_topic = ""
		top_topic_votes = 0

	agreement_score = top_subject_votes / total_models
	half = math.ceil(total_models / 2)
	if agreement_score >= 0.8 and top_topic_votes >= half:
		confidence = CONF_HIGH
	elif agreement_score >= 0.5:
		confidence = CONF_MEDIUM
	else:
		confidence = CONF_LOW

	row = {
		"script": script,
		"top_subject": top_subject,
		"top_topic": top_topic,
		"subject_votes": format_votes(subj_bucket),
		"topic_votes": format_votes(topic_bucket),
		"total_models": total_models,
		"agreement_score": round(agreement_score, 3),
		"confidence": confidence,
		"runner_up_subject": runner_up_subject,
		"runner_up_votes": runner_up_votes,
	}
	return row


# Simple assert for compute_suggestion with no votes
_empty_row = compute_suggestion("x", {}, {})
assert _empty_row["confidence"] == CONF_NONE
assert _empty_row["total_models"] == 0


#============================================
def sort_rows(rows: list) -> list:
	"""Sort report rows: confidence, agreement_score desc, script."""
	ordered = sorted(
		rows,
		key=lambda r: (
			CONF_ORDER.get(r["confidence"], 99),
			-r["agreement_score"],
			r["script"],
		),
	)
	return ordered


#============================================
def write_report(rows: list, output_path: str) -> None:
	"""Write the unassigned report CSV."""
	columns = [
		"script",
		"top_subject",
		"top_topic",
		"subject_votes",
		"topic_votes",
		"total_models",
		"agreement_score",
		"confidence",
		"runner_up_subject",
		"runner_up_votes",
	]
	with open(output_path, "w", newline="") as handle:
		writer = csv.DictWriter(handle, fieldnames=columns)
		writer.writeheader()
		for row in rows:
			writer.writerow(row)


#============================================
def short_script(script: str) -> str:
	"""Drop '{bp_root}/' and '-problems/' noise for display."""
	clean = script
	if clean.startswith("{bp_root}/"):
		clean = clean[len("{bp_root}/"):]
	clean = clean.replace("-problems/", "/")
	return clean


#============================================
def format_topic_display(
	subject: str,
	topic: str,
	topic_lookup: dict,
) -> str:
	"""Format '(subject, topic)' as 'topic03 Enzymes' for display."""
	if not topic:
		return ""
	topic_name = topic_lookup.get((subject, topic), "")
	if topic_name:
		display = f"{topic} {topic_name}"
	else:
		display = topic
	return display


#============================================
def print_console_table(
	rows: list,
	topic_lookup: dict,
	limit: int,
) -> None:
	"""Print a grouped console table of unassigned scripts."""
	if not rows:
		print("No unassigned scripts found.")
		return
	groups = [CONF_HIGH, CONF_MEDIUM, CONF_LOW, CONF_NONE]
	headers = ["script", "subject", "topic", "votes", "runner-up"]
	printed = 0
	for label in groups:
		group_rows = [r for r in rows if r["confidence"] == label]
		if not group_rows:
			continue
		print()
		print(f"=== {label} ({len(group_rows)}) ===")
		table_data = []
		for row in group_rows:
			if limit and printed >= limit:
				break
			votes_str = (
				f"{row['total_models']}"
				if row["total_models"]
				else "-"
			)
			if row["confidence"] != CONF_NONE:
				votes_str = (
					f"{row['total_models']}"
					f" ({row['agreement_score']:.2f})"
				)
			runner = ""
			if row["runner_up_subject"]:
				runner = (
					f"{row['runner_up_subject']}:"
					f"{row['runner_up_votes']}"
				)
			table_data.append([
				short_script(row["script"]),
				row["top_subject"] or "-",
				format_topic_display(
					row["top_subject"],
					row["top_topic"],
					topic_lookup,
				) or "-",
				votes_str,
				runner or "-",
			])
			printed += 1
		if table_data:
			print(tabulate.tabulate(
				table_data,
				headers=headers,
				tablefmt="simple",
			))
		if limit and printed >= limit:
			break


#============================================
def main() -> None:
	args = parse_args()

	repo_root = script_runner.get_repo_root()

	# 1. Build script universe
	raw_scripts = script_runner.discover_generator_scripts(repo_root)
	universe = set()
	for raw in raw_scripts:
		try:
			universe.add(compare_results._to_bp_root(raw))
		except ValueError:
			# Skip unexpectedly-shaped paths; surface loudly on stderr
			print(f"WARN: skipping unrecognized path: {raw}")

	# 2. Load assigned scripts
	assigned = load_assigned_scripts(args.task_dir)

	# 3. Unassigned = universe - assigned
	unassigned = sorted(universe - set(assigned.keys()))

	# 4. Load classifier votes
	subject_votes, topic_votes, models = load_classifier_votes(
		args.base_dir
	)

	# 5. Build rows
	rows = []
	for script in unassigned:
		row = compute_suggestion(script, subject_votes, topic_votes)
		if row["total_models"] < args.min_votes:
			continue
		rows.append(row)

	rows = sort_rows(rows)

	# 6. Write CSV
	write_report(rows, args.output_file)

	# 7. Console output
	topic_lookup = compare_results.build_topic_lookup()

	print(f"Task CSV dir: {args.task_dir}")
	print(f"Results base: {args.base_dir}")
	print(f"Models loaded: {len(models)}  ({', '.join(models) or '-'})")
	print(f"Universe of generator scripts: {len(universe)}")
	print(f"Already assigned: {len(assigned)}")
	print(f"Unassigned: {len(unassigned)}")
	print(f"Rows in report (after --min-votes={args.min_votes}): {len(rows)}")

	print_console_table(rows, topic_lookup, args.limit)

	counts = {CONF_HIGH: 0, CONF_MEDIUM: 0, CONF_LOW: 0, CONF_NONE: 0}
	for row in rows:
		counts[row["confidence"]] = counts.get(row["confidence"], 0) + 1
	print()
	print(
		f"Summary: HIGH={counts[CONF_HIGH]}  "
		f"MEDIUM={counts[CONF_MEDIUM]}  "
		f"LOW={counts[CONF_LOW]}  "
		f"NONE={counts[CONF_NONE]}"
	)
	print(f"Report written to: {args.output_file}")


if __name__ == "__main__":
	main()
