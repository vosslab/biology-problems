#!/usr/bin/env python3

"""Classify biology-problems generator scripts into textbook topics using a local LLM.

Two-stage classification:
  Stage 1: Assign each script to a subject (biochemistry, genetics, etc.)
  Stage 2: Assign to a specific topic within that subject (topic01, topic02, etc.)

Output: per-subject CSV files in bbq_control format + diff report.
"""

# Standard Library
import os
import sys
import json
import random
import shlex
import argparse
import subprocess

# Add local-llm-wrapper to path if not already importable
_LLM_WRAPPER_DIR = os.path.join(os.path.expanduser("~"), "nsh", "local-llm-wrapper")
if _LLM_WRAPPER_DIR not in sys.path:
	sys.path.insert(0, _LLM_WRAPPER_DIR)

# PIP3 modules
import local_llm_wrapper.llm as llm

# local repo modules
import topic_classifier.index_parser as index_parser
import topic_classifier.csv_handler as csv_handler
import topic_classifier.script_runner as script_runner
import topic_classifier.prompt_builder as prompt_builder

#============================================
BBQ_CONTROL_DIR = os.path.join(
	os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
	"..", "biology-problems-website", "bbq_control",
)

#============================================
def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments."""
	parser = argparse.ArgumentParser(
		description="Classify generator scripts into textbook topics using a local LLM.",
	)
	parser.add_argument(
		'-o', '--output', dest='output_dir', type=str,
		default=None,
		help="Output directory for result CSVs (default: topic_classifier/results/)",
	)
	parser.add_argument(
		'-d', '--diff', dest='diff_mode', action='store_true',
		help="Compare generated results against existing bbq_control CSVs",
	)
	parser.add_argument(
		'-m', '--model', dest='model', type=str,
		default=None,
		help="Override Ollama model (default: auto-select based on RAM)",
	)
	parser.add_argument(
		'-n', '--dry-run', dest='dry_run', action='store_true',
		help="Show what would be classified without calling LLM",
	)
	parser.add_argument(
		'-l', '--limit', dest='limit', type=int,
		default=None,
		help="Process only first N scripts (for testing)",
	)
	parser.add_argument(
		'-s', '--shuffle', dest='shuffle', action='store_true',
		help="Shuffle script order before processing (useful with --limit)",
	)
	parser.add_argument(
		'--source-only', dest='source_only', action='store_true',
		help="Skip script execution, classify from source code only",
	)
	args = parser.parse_args()
	return args

#============================================
def get_repo_root() -> str:
	"""Get the repository root directory via git."""
	result = subprocess.run(
		["git", "rev-parse", "--show-toplevel"],
		capture_output=True, text=True, check=True,
	)
	repo_root = result.stdout.strip()
	return repo_root

#============================================
def setup_output_dirs(repo_root: str, output_dir: str) -> tuple:
	"""Set up output and cache directories.

	Args:
		repo_root: repository root path
		output_dir: user-specified output dir or None

	Returns:
		tuple of (results_dir, cache_dir, debug_dir)
	"""
	classifier_dir = os.path.join(repo_root, "topic_classifier")
	if output_dir is None:
		results_dir = os.path.join(classifier_dir, "results")
	else:
		results_dir = output_dir
	cache_dir = os.path.join(classifier_dir, "output")
	debug_dir = cache_dir

	os.makedirs(results_dir, exist_ok=True)
	os.makedirs(cache_dir, exist_ok=True)

	return results_dir, cache_dir, debug_dir

#============================================
def create_llm_client(model: str = None) -> llm.LLMClient:
	"""Create an LLM client with Apple + Ollama fallback.

	Args:
		model: optional Ollama model override

	Returns:
		configured LLMClient
	"""
	transports = []
	# Try Apple first (fastest, on-device)
	if llm.apple_models_available():
		transports.append(llm.AppleTransport())
	# Ollama as fallback
	ollama_model = llm.choose_model(model)
	transports.append(llm.OllamaTransport(model=ollama_model))

	client = llm.LLMClient(transports=transports, quiet=True)
	return client

#============================================
def classify_stage1(
	client: llm.LLMClient,
	script_path: str,
	source_code: str,
	bbq_output: str,
	all_indexes: dict,
	cross_examples: list,
) -> dict:
	"""Run stage 1 classification: determine subject.

	Args:
		client: LLM client
		script_path: relative path to script
		source_code: source code (full or summarized)
		bbq_output: sample output or None
		all_indexes: subject index data
		cross_examples: few-shot examples across subjects

	Returns:
		dict with subject, confidence, reasoning, raw_response
	"""
	messages = prompt_builder.build_stage1_prompt(
		script_path, source_code, bbq_output,
		all_indexes, cross_examples,
	)

	response = client.generate(messages=messages, max_tokens=500)

	subject = llm.extract_xml_tag_content(response, "subject")
	confidence = llm.extract_xml_tag_content(response, "confidence")
	reasoning = llm.extract_xml_tag_content(response, "reasoning")

	result = {
		"subject": subject.strip() if subject else None,
		"confidence": confidence.strip() if confidence else None,
		"reasoning": reasoning.strip() if reasoning else None,
		"raw_response": response,
	}
	return result

#============================================
def classify_stage2(
	client: llm.LLMClient,
	script_path: str,
	source_code: str,
	bbq_output: str,
	subject: str,
	topics: list,
	subject_examples: list,
) -> dict:
	"""Run stage 2 classification: determine topic within subject.

	Args:
		client: LLM client
		script_path: relative path to script
		source_code: source code (full or summarized)
		bbq_output: sample output or None
		subject: predicted subject from stage 1
		topics: topic list for this subject
		subject_examples: few-shot examples from this subject

	Returns:
		dict with topic, confidence, reasoning, raw_response
	"""
	messages = prompt_builder.build_stage2_prompt(
		script_path, source_code, bbq_output,
		subject, topics, subject_examples,
	)

	response = client.generate(messages=messages, max_tokens=500)

	topic = llm.extract_xml_tag_content(response, "topic")
	confidence = llm.extract_xml_tag_content(response, "confidence")
	reasoning = llm.extract_xml_tag_content(response, "reasoning")

	result = {
		"topic": topic.strip() if topic else None,
		"confidence": confidence.strip() if confidence else None,
		"reasoning": reasoning.strip() if reasoning else None,
		"raw_response": response,
	}
	return result

#============================================
def compute_confidence_score(
	stage1: dict,
	stage2: dict,
	has_bbq: bool,
	all_indexes: dict,
) -> int:
	"""Compute a heuristic confidence score (0-5).

	Args:
		stage1: stage 1 classification result
		stage2: stage 2 classification result
		has_bbq: whether bbq output was available
		all_indexes: subject index data for validation

	Returns:
		integer score 0-5
	"""
	score = 0

	# +1 for bbq output available
	if has_bbq:
		score += 1

	# +1 for clean XML parsing (both stages)
	if stage1["subject"] is not None and stage2["topic"] is not None:
		score += 1

	# +1 for predicted topic existing in subject index
	subject = stage1["subject"]
	topic = stage2["topic"]
	if subject in all_indexes:
		valid_topics = [t["topic_id"] for t in all_indexes[subject]]
		if topic in valid_topics:
			score += 1

	# +1 for reasoning containing topic keywords
	if stage2["reasoning"] and subject in all_indexes:
		topic_entry = None
		for t in all_indexes[subject]:
			if t["topic_id"] == topic:
				topic_entry = t
				break
		if topic_entry is not None:
			# Check if reasoning mentions topic name or description words
			reasoning_lower = stage2["reasoning"].lower()
			topic_words = topic_entry["name"].lower().split()
			keyword_match = any(w in reasoning_lower for w in topic_words if len(w) > 3)
			if keyword_match:
				score += 1

	# +1 for LLM self-reported high confidence (both stages)
	if stage1["confidence"] == "high" and stage2["confidence"] == "high":
		score += 1

	return score

#============================================
def classify_one_script(
	client: llm.LLMClient,
	script_path: str,
	repo_root: str,
	cache_dir: str,
	all_indexes: dict,
	cross_examples: list,
	assignments: dict,
	source_only: bool = False,
) -> dict:
	"""Classify a single script through both stages.

	Args:
		client: LLM client
		script_path: relative path to script
		repo_root: repository root
		cache_dir: directory for caching bbq output
		all_indexes: subject index data
		cross_examples: cross-subject few-shot examples
		assignments: existing CSV assignments
		source_only: skip execution if True

	Returns:
		dict with full classification result
	"""
	# Read source code
	source_code = script_runner.read_source_code(script_path, repo_root)
	source_for_llm = prompt_builder.summarize_source(source_code)

	# Get bbq output
	bbq_output = None
	execution_status = "skipped"
	if not source_only:
		# Check cache first
		cached = script_runner.get_cached_bbq(script_path, cache_dir)
		if cached is not None:
			bbq_output = script_runner.read_bbq_output(cached)
			execution_status = "cached"
		else:
			# Build extra args from existing CSV assignment (flags, input)
			extra_args = _get_run_args(script_path, assignments)
			if extra_args:
				print(f"  Running {script_path} {' '.join(extra_args)}...")
			else:
				print(f"  Running {script_path}...")
			run_result = script_runner.run_script(
				script_path, repo_root, extra_args=extra_args,
			)
			if run_result["success"] and run_result["bbq_file"]:
				cached_path = script_runner.cache_bbq_file(
					run_result["bbq_file"], cache_dir,
				)
				bbq_output = script_runner.read_bbq_output(cached_path)
				execution_status = "success"
			else:
				# No bbq file produced -- skip classification
				print("  SKIP: no bbq file produced")
				return None

	# Stage 1: subject classification
	print("  Stage 1: classifying subject...")
	stage1 = classify_stage1(
		client, script_path, source_for_llm, bbq_output,
		all_indexes, cross_examples,
	)

	if stage1["subject"] is None:
		# Failed to classify subject
		result = _make_failed_result(script_path, execution_status, stage1)
		return result

	subject = stage1["subject"]
	print(f"  Stage 1 result: {subject} ({stage1['confidence']})")

	# Get topics and examples for stage 2
	topics = all_indexes.get(subject, [])
	subject_examples = csv_handler.get_examples_for_subject(assignments, subject)

	# Stage 2: topic classification
	print(f"  Stage 2: classifying topic within {subject}...")
	stage2 = classify_stage2(
		client, script_path, source_for_llm, bbq_output,
		subject, topics, subject_examples,
	)

	if stage2["topic"] is None:
		result = _make_failed_result(script_path, execution_status, stage1, stage2)
		return result

	# Look up topic name for display
	topic_name = _get_topic_name(topics, stage2["topic"])
	print(f"  Stage 2 result: {stage2['topic']} {topic_name} ({stage2['confidence']})")

	# Compute confidence score
	has_bbq = bbq_output is not None
	confidence_score = compute_confidence_score(stage1, stage2, has_bbq, all_indexes)
	status = "classified" if confidence_score >= 4 else "review"

	# Check against existing assignments
	bp_root_path = "{bp_root}/" + script_path.replace("problems/", "", 1)
	existing_entry = None
	for key, entry in assignments.items():
		entry_script = csv_handler.get_script_path_from_key(key)
		if entry_script == bp_root_path:
			existing_entry = entry
			break

	existing_assignment = None
	match = None
	if existing_entry is not None:
		existing_assignment = f"{existing_entry['chapter']}/{existing_entry['topic']}"
		match = (existing_entry["chapter"] == subject and existing_entry["topic"] == stage2["topic"])

	result = {
		"script": script_path,
		"chapter": subject,
		"topic": stage2["topic"],
		"flags": "",
		"input": "",
		"notes": "",
		"confidence_score": confidence_score,
		"status": status,
		"execution": execution_status,
		"existing": existing_assignment,
		"match": match,
		"stage1_reasoning": stage1["reasoning"],
		"stage2_reasoning": stage2["reasoning"],
		"stage1_confidence": stage1["confidence"],
		"stage2_confidence": stage2["confidence"],
		"topic_name": topic_name,
	}
	return result

#============================================
def _get_run_args(script_path: str, assignments: dict) -> list:
	"""Look up flags and input file from existing CSV assignments for a script.

	Args:
		script_path: relative path to the script
		assignments: existing CSV assignments dict

	Returns:
		list of CLI args, e.g. ['-y', '/path/to/input.yml', '--mc']
	"""
	# Convert relative path to {bp_root} format used in CSVs
	bp_root_path = "{bp_root}/" + script_path.replace("problems/", "", 1)

	# Find first matching assignment
	for key, entry in assignments.items():
		entry_script = csv_handler.get_script_path_from_key(key)
		if entry_script != bp_root_path:
			continue
		args = []
		# Add flags from CSV
		flags = entry.get("flags", "").strip()
		if flags:
			args.extend(shlex.split(flags))
		# Add input file from CSV
		input_file = entry.get("input", "").strip()
		if input_file:
			# Resolve {bp_root} placeholder
			repo_root = script_runner.get_repo_root()
			resolved = input_file.replace("{bp_root}/", "problems/")
			abs_input = os.path.join(repo_root, resolved)
			if os.path.isfile(abs_input):
				args.extend(["-y", abs_input])
		return args
	return []

#============================================
def _get_topic_name(topics: list, topic_id: str) -> str:
	"""Look up the human-readable topic name from a topic_id.

	Args:
		topics: list of topic dicts from index_parser
		topic_id: e.g. 'topic04'

	Returns:
		topic name string, or empty string if not found
	"""
	for t in topics:
		if t["topic_id"] == topic_id:
			return t["name"]
	return ""

#============================================
def _make_failed_result(
	script_path: str,
	execution_status: str,
	stage1: dict,
	stage2: dict = None,
) -> dict:
	"""Create a result dict for a failed classification.

	Args:
		script_path: relative path to script
		execution_status: success/failed/cached/skipped
		stage1: stage 1 result dict
		stage2: stage 2 result dict or None

	Returns:
		result dict with status='review'
	"""
	result = {
		"script": script_path,
		"chapter": stage1.get("subject", "unknown"),
		"topic": stage2["topic"] if stage2 else "unknown",
		"flags": "",
		"input": "",
		"notes": "classification failed",
		"confidence_score": 0,
		"status": "review",
		"execution": execution_status,
		"existing": None,
		"match": None,
		"stage1_reasoning": stage1.get("reasoning", ""),
		"stage2_reasoning": stage2.get("reasoning", "") if stage2 else "",
		"stage1_confidence": stage1.get("confidence", ""),
		"stage2_confidence": stage2.get("confidence", "") if stage2 else "",
	}
	return result

#============================================
def write_debug_log(result: dict, debug_dir: str) -> None:
	"""Append a result to the JSONL debug log for crash recovery.

	Args:
		result: classification result dict
		debug_dir: directory for debug files
	"""
	log_path = os.path.join(debug_dir, "classification_log.jsonl")
	with open(log_path, "a") as f:
		f.write(json.dumps(result) + "\n")

#============================================
def print_diff_report(results: list) -> None:
	"""Print a diff report comparing results against existing assignments.

	Args:
		results: list of classification result dicts
	"""
	matches = 0
	disagreements = 0
	new_scripts = 0
	reviews = 0

	for r in results:
		script_name = os.path.basename(r["script"])
		topic_name = r.get("topic_name", "")
		if topic_name:
			predicted = f"{r['chapter']}/{r['topic']} ({topic_name})"
		else:
			predicted = f"{r['chapter']}/{r['topic']}"

		if r["status"] == "review":
			print(f"REVIEW:   {script_name} -> {predicted} "
				f"(score: {r['confidence_score']}, exec: {r['execution']})")
			reviews += 1
		elif r["existing"] is None:
			print(f"NEW:      {script_name} -> {predicted}")
			new_scripts += 1
		elif r["match"]:
			print(f"MATCH:    {script_name} -> {predicted}")
			matches += 1
		else:
			print(f"DISAGREE: {script_name} -> {predicted} "
				f"(existing: {r['existing']})")
			disagreements += 1

	print(f"\nSummary: {matches} matches, {new_scripts} new, "
		f"{disagreements} disagreements, {reviews} review")

#============================================
def main():
	"""Main entry point for the topic classifier."""
	args = parse_args()
	repo_root = get_repo_root()

	# Set up directories
	results_dir, cache_dir, debug_dir = setup_output_dirs(
		repo_root, args.output_dir,
	)

	# Load subject indexes
	print("Loading subject indexes...")
	all_indexes = index_parser.load_all_indexes()

	# Load existing CSV assignments
	print("Loading existing CSV assignments...")
	bbq_control_dir = os.path.realpath(BBQ_CONTROL_DIR)
	if os.path.isdir(bbq_control_dir):
		assignments = csv_handler.read_existing_assignments(bbq_control_dir)
		print(f"  Loaded {len(assignments)} existing assignments")
	else:
		print(f"  WARNING: bbq_control dir not found at {bbq_control_dir}")
		assignments = {}

	# Get cross-subject examples for stage 1
	cross_examples = csv_handler.get_cross_subject_examples(assignments)

	# Discover generator scripts
	print("Discovering generator scripts...")
	scripts = script_runner.discover_generator_scripts(repo_root)
	print(f"  Found {len(scripts)} generator scripts")

	# Shuffle if requested (useful with --limit for testing variety)
	if args.shuffle:
		random.shuffle(scripts)

	# Apply limit if specified
	if args.limit is not None:
		scripts = scripts[:args.limit]
		print(f"  Limited to {args.limit} scripts")

	# Dry run: just show what would be classified
	if args.dry_run:
		print("\n--- Dry run: scripts to classify ---")
		for s in scripts:
			print(f"  {s}")
		print(f"\nTotal: {len(scripts)} scripts")
		print(f"Subjects available: {', '.join(sorted(all_indexes.keys()))}")
		print(f"Existing assignments: {len(assignments)}")
		return

	# Create LLM client
	print("Initializing LLM client...")
	client = create_llm_client(args.model)

	# Classify all scripts
	results = []
	no_bbq_scripts = []
	for i, script_path in enumerate(scripts):
		print(f"\n[{i+1}/{len(scripts)}] Classifying {script_path}")
		result = classify_one_script(
			client, script_path, repo_root, cache_dir,
			all_indexes, cross_examples, assignments,
			source_only=args.source_only,
		)
		if result is None:
			# Script produced no bbq file -- record for no_bbq_file.csv
			no_bbq_scripts.append(script_path)
			continue

		results.append(result)

		# Write debug log incrementally for crash recovery
		write_debug_log(result, debug_dir)

		status_icon = "OK" if result["status"] == "classified" else "??"
		topic_label = result.get("topic_name", result["topic"])
		print(f"  [{status_icon}] {result['chapter']}/{result['topic']} {topic_label} "
			f"(score: {result['confidence_score']})")

	# Write result CSVs in one pass
	print(f"\nWriting result CSVs to {results_dir}...")
	written = csv_handler.write_result_csvs(results, results_dir)
	for f in written:
		print(f"  Written: {f}")

	# Write no_bbq_file.csv for scripts that produced no output
	if no_bbq_scripts:
		no_bbq_path = os.path.join(results_dir, "no_bbq_file.csv")
		with open(no_bbq_path, "w") as f:
			f.write("script\n")
			for s in sorted(no_bbq_scripts):
				f.write(f"{s}\n")
		print(f"  Written: {no_bbq_path} ({len(no_bbq_scripts)} scripts)")

	# Show diff report if requested or always show summary
	if args.diff_mode or True:
		print("\n--- Classification Report ---")
		print_diff_report(results)

#============================================
if __name__ == '__main__':
	main()
