#!/usr/bin/env python3

"""Classify biology-problems generator scripts into textbook topics using a local LLM.

Two-stage classification:
  Stage 1: Assign each script to a subject (biochemistry, genetics, etc.)
  Stage 2: Assign to a specific topic within that subject (topic01, topic02, etc.)

Output: per-subject CSV files in bbq_control format + diff report.
"""

# Standard Library
import os
import time
import random
import shlex
import argparse
import subprocess

# local repo modules
import topic_classifier.index_parser_lib as index_parser
import topic_classifier.csv_handler_lib as csv_handler
import topic_classifier.script_runner_lib as script_runner
import topic_classifier.prompt_builder_lib as prompt_builder
import topic_classifier.classifier_common_lib as common

# Re-exports from common so local references stay readable
llm = common.llm
console = common.console

#============================================
BBQ_CONTROL_DIR = os.path.join(
	os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
	"..", "biology-problems-website", "bbq_control", "task_files",
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
		'-O', '--ollama', dest='use_ollama', action='store_true',
		help="Use Ollama instead of Apple Intelligence (auto-selects model by RAM)",
	)
	parser.add_argument(
		'-m', '--model', dest='model', type=str, default=None,
		help=("Use Ollama with this exact local model (implies --ollama). "
			"Examples: gpt-oss:20b, phi4:14b-q4_K_M, "
			"llama3.2:3b-instruct-q5_K_M, llama3.2:1b-instruct-q4_K_M"),
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
	parser.add_argument(
		'-v', '--verbose', dest='verbose', action='store_true',
		help="Show extra debug output (summary fields, reasoning, keywords)",
	)
	parser.add_argument(
		'-r', '--repeat', dest='repeat', type=int, default=1,
		help="Classify each script N times and report consistency (default: 1)",
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
		tuple of (results_dir, debug_dir)
	"""
	classifier_dir = os.path.join(repo_root, "topic_classifier")
	if output_dir is None:
		results_dir = os.path.join(classifier_dir, "results")
	else:
		results_dir = output_dir
	debug_dir = os.path.join(classifier_dir, "output")

	os.makedirs(results_dir, exist_ok=True)
	os.makedirs(debug_dir, exist_ok=True)

	return results_dir, debug_dir

#============================================
# Thin delegators keep call sites unchanged while the implementations
# live in classifier_common for reuse with classify_yaml.py.
validate_ollama_model = common.validate_ollama_model
create_llm_client = common.create_llm_client
_generate_with_retry = common.generate_with_retry
_parse_confidence = common.parse_confidence

#============================================
def classify_stage1(
	client: llm.LLMClient,
	script_path: str,
	source_code: str,
	all_indexes: dict,
	cross_examples: list,
	verbose: bool = False,
	bbq_output: str = None,
) -> dict:
	"""Run stage 1 classification: determine subject.

	Args:
		client: LLM client
		script_path: relative path to script
		source_code: source code (full or summarized)
		all_indexes: subject index data
		cross_examples: few-shot examples across subjects
		verbose: show failed response details on retry
		bbq_output: cleaned question text from the script, or None

	Returns:
		dict with subject, confidence, reasoning, raw_response
	"""
	messages = prompt_builder.build_stage1_prompt(
		script_path, source_code,
		all_indexes, cross_examples, bbq_output=bbq_output,
	)

	response = _generate_with_retry(
		client, messages, max_tokens=500,
		required_tags=["subject", "confidence"],
		verbose=verbose,
	)

	subject = llm.extract_xml_tag_content(response, "subject")
	confidence_raw = llm.extract_xml_tag_content(response, "confidence")
	reasoning = llm.extract_xml_tag_content(response, "reasoning")

	result = {
		"subject": subject.strip() if subject else None,
		"confidence": _parse_confidence(confidence_raw),
		"reasoning": reasoning.strip() if reasoning else None,
		"raw_response": response,
	}
	return result

#============================================
def classify_stage2(
	client: llm.LLMClient,
	script_path: str,
	source_code: str,
	subject: str,
	topics: list,
	subject_examples: list,
	verbose: bool = False,
	bbq_output: str = None,
) -> dict:
	"""Run stage 2 classification: determine topic within subject.

	Args:
		client: LLM client
		script_path: relative path to script
		source_code: source code (full or summarized)
		subject: predicted subject from stage 1
		topics: topic list for this subject
		subject_examples: few-shot examples from this subject
		verbose: show failed response details on retry
		bbq_output: cleaned question text from the script, or None

	Returns:
		dict with topic, confidence, reasoning, raw_response
	"""
	messages = prompt_builder.build_stage2_prompt(
		script_path, source_code,
		subject, topics, subject_examples, bbq_output=bbq_output,
	)

	response = _generate_with_retry(
		client, messages, max_tokens=800,
		required_tags=["topic", "confidence"],
		verbose=verbose,
	)

	# Parse structured output
	topic = llm.extract_xml_tag_content(response, "topic")
	confidence_raw = llm.extract_xml_tag_content(response, "confidence")
	reasoning = llm.extract_xml_tag_content(response, "reasoning")

	result = {
		"topic": topic.strip() if topic else None,
		"confidence": _parse_confidence(confidence_raw),
		"reasoning": reasoning.strip() if reasoning else None,
		"raw_response": response,
	}
	return result

#============================================
# Shared with classify_yaml.py via classifier_common
compute_confidence_score = common.compute_confidence_score

#============================================
def classify_one_script(
	client: llm.LLMClient,
	script_path: str,
	repo_root: str,
	all_indexes: dict,
	cross_examples: list,
	assignments: dict,
	flags: str = "",
	input_file: str = "",
	source_only: bool = False,
	verbose: bool = False,
) -> dict:
	"""Classify a single script through summarize + subject + topic stages.

	Args:
		client: LLM client
		script_path: relative path to script
		repo_root: repository root
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
	if verbose:
		src_lines = len(source_code.split("\n"))
		llm_lines = len(source_for_llm.split("\n"))
		if src_lines != llm_lines:
			console.print(f"  source: {src_lines} lines -> trimmed to {llm_lines} lines", style="dim")

	# Get bbq output
	bbq_output = None
	execution_status = "skipped"
	if not source_only:
		# Build extra args from explicit flags + input for this variant
		extra_args = _build_run_args(flags, input_file, repo_root)
		if extra_args:
			console.print(f"  Running [cyan]{script_path}[/cyan] {' '.join(extra_args)}", style="dim")
		else:
			console.print(f"  Running [cyan]{script_path}[/cyan]", style="dim")
		run_result = script_runner.run_script(
			script_path, repo_root, extra_args=extra_args,
		)
		if run_result["success"] and run_result["bbq_file"]:
			# Read human-readable output, then clean up the bbq file
			bbq_file = run_result["bbq_file"]
			bbq_output = script_runner.read_bbq_output(bbq_file)
			os.remove(bbq_file)
			execution_status = "success"
			if verbose and bbq_output:
				# Show the question text so the user can see what the LLM is classifying
				console.print("  --- Question text ---", style="dim")
				for line in bbq_output.strip().split("\n"):
					console.print(f"    {line}", style="dim")
				console.print("  --- End question text ---", style="dim")
		else:
			# No bbq file produced -- skip classification
			console.print("  SKIP: no bbq file produced", style="yellow")
			return None

	# Stage 1: subject classification
	console.print("  Classifying subject...", style="dim")
	stage1 = classify_stage1(
		client, script_path, source_for_llm,
		all_indexes, cross_examples, verbose=verbose,
		bbq_output=bbq_output,
	)

	if stage1["subject"] is None:
		console.print("  FAILED: could not determine subject", style="bold red")
		result = _make_failed_result(script_path, execution_status, stage1, flags=flags, input_file=input_file)
		return result

	subject = stage1["subject"]
	# Color confidence level (1-5 scale)
	conf = stage1["confidence"]
	conf_color = "green" if conf >= 4 else ("yellow" if conf >= 3 else "red")
	console.print(f"  Subject: [bold cyan]{subject}[/bold cyan] ([{conf_color}]{conf}/5[/{conf_color}])")
	if verbose:
		console.print(f"    LLM response length: {len(stage1['raw_response'])} chars", style="dim")
		if stage1.get("reasoning"):
			console.print(f"    reasoning: {stage1['reasoning']}", style="dim")

	# Stage 2: topic classification
	subject_data = all_indexes.get(subject, {"topics": []})
	topics = subject_data["topics"]
	subject_examples = csv_handler.get_examples_for_subject(assignments, subject)

	console.print(f"  Classifying topic within [bold cyan]{subject}[/bold cyan]...", style="dim")
	stage2 = classify_stage2(
		client, script_path, source_for_llm,
		subject, topics, subject_examples, verbose=verbose,
		bbq_output=bbq_output,
	)

	if stage2["topic"] is None:
		console.print("  FAILED: could not determine topic", style="bold red")
		result = _make_failed_result(script_path, execution_status, stage1, stage2, flags=flags, input_file=input_file)
		return result

	# Look up topic name for display
	topic_name = _get_topic_name(topics, stage2["topic"])
	conf2 = stage2["confidence"]
	conf2_color = "green" if conf2 >= 4 else ("yellow" if conf2 >= 3 else "red")
	console.print(f"  Topic: [bold cyan]{stage2['topic']}[/bold cyan] {topic_name} ([{conf2_color}]{conf2}/5[/{conf2_color}])")
	if verbose:
		console.print(f"    LLM response length: {len(stage2['raw_response'])} chars", style="dim")
		if stage2.get("reasoning"):
			console.print(f"    reasoning: {stage2['reasoning']}", style="dim")

	# Compute confidence score (max 4 after removing decisive_keywords scoring)
	has_bbq = bbq_output is not None
	confidence_score = compute_confidence_score(stage1, stage2, has_bbq, all_indexes)
	status = "classified" if confidence_score >= 3 else "review"

	# Check against existing assignments for this exact (script, flags) variant
	bp_root_path = "{bp_root}/" + script_path.replace("problems/", "", 1)
	existing_entry = assignments.get(f"{bp_root_path}|{flags}")

	existing_assignment = None
	match = None
	if existing_entry is not None:
		existing_assignment = f"{existing_entry['chapter']}/{existing_entry['topic']}"
		match = (existing_entry["chapter"] == subject and existing_entry["topic"] == stage2["topic"])
		if verbose:
			if match:
				console.print(f"    existing: [green]{existing_assignment} (match)[/green]")
			else:
				console.print(f"    existing: [red]{existing_assignment} (disagree)[/red]")

	result = {
		"script": script_path,
		"chapter": subject,
		"topic": stage2["topic"],
		"flags": flags,
		"input": input_file,
		"notes": "",
		"confidence_score": confidence_score,
		"status": status,
		"execution": execution_status,
		"existing": existing_assignment,
		"match": match,
		# Stage 1 fields
		"stage1_reasoning": stage1["reasoning"],
		"stage1_confidence": stage1["confidence"],
		# Stage 2 fields
		"stage2_reasoning": stage2.get("reasoning"),
		"stage2_confidence": stage2["confidence"],
		"topic_name": topic_name,
	}
	return result

#============================================
def _build_run_args(flags: str, input_file: str, repo_root: str) -> list:
	"""Build CLI args from an explicit (flags, input) variant.

	Args:
		flags: flags string from a CSV row (may be empty)
		input_file: input file token from a CSV row, possibly using
			'{bp_root}/' prefix (may be empty)
		repo_root: repository root for resolving {bp_root}

	Returns:
		list of CLI args, e.g. ['--mc', '-y', '/abs/path/input.yml']
	"""
	args = []
	if flags:
		args.extend(shlex.split(flags))
	if input_file:
		# Resolve the {bp_root}/ placeholder used in the control CSVs
		resolved = input_file.replace("{bp_root}/", "problems/")
		abs_input = os.path.join(repo_root, resolved)
		if os.path.isfile(abs_input):
			args.extend(["-y", abs_input])
	return args

#============================================
# Shared with classify_yaml.py via classifier_common. print_diff_report and
# print_consistency_report in common transparently accept either 'subject'
# or 'chapter' keys on result dicts, so classify_scripts.py can keep writing
# 'chapter' without changes here.
_get_topic_name = common.get_topic_name
write_debug_log = common.write_debug_log
print_diff_report = common.print_diff_report
print_consistency_report = common.print_consistency_report
_format_duration = common.format_duration

#============================================
def _make_failed_result(
	script_path: str,
	execution_status: str,
	stage1: dict,
	stage2: dict = None,
	flags: str = "",
	input_file: str = "",
) -> dict:
	"""Create a failed-classification result dict keyed with 'chapter'.

	A thin wrapper over common.make_failed_result that renames the
	'subject' key back to 'chapter' so the existing classify_scripts.py
	result schema stays unchanged, and overwrites the placeholder
	flags/input fields with the actual variant so failed results from
	different variants of the same script do not collide in dedup.

	Args:
		script_path: relative path to script
		execution_status: success/failed/cached/skipped
		stage1: stage 1 result dict
		stage2: stage 2 result dict or None
		flags: CLI flags string for this variant
		input_file: input file path for this variant

	Returns:
		result dict with status='review' and 'chapter' key
	"""
	result = common.make_failed_result(script_path, execution_status, stage1, stage2)
	result["chapter"] = result.pop("subject")
	result["flags"] = flags
	result["input"] = input_file
	return result

#============================================
def main():
	"""Main entry point for the topic classifier."""
	args = parse_args()
	repo_root = get_repo_root()

	# Set up directories
	results_dir, debug_dir = setup_output_dirs(
		repo_root, args.output_dir,
	)

	# Load subject indexes
	console.print("Loading subject indexes...", style="dim italic")
	all_indexes = index_parser.load_all_indexes()

	# Load existing CSV assignments
	console.print("Loading existing CSV assignments...", style="dim italic")
	bbq_control_dir = os.path.realpath(BBQ_CONTROL_DIR)
	if os.path.isdir(bbq_control_dir):
		assignments = csv_handler.read_existing_assignments(bbq_control_dir)
		console.print(f"  Loaded [bold]{len(assignments)}[/bold] existing assignments")
	else:
		console.print(f"  WARNING: bbq_control dir not found at {bbq_control_dir}", style="yellow")
		assignments = {}

	# Get cross-subject examples for stage 1
	cross_examples = csv_handler.get_cross_subject_examples(assignments)

	# Discover generator scripts
	console.print("Discovering generator scripts...", style="dim italic")
	scripts = script_runner.discover_generator_scripts(repo_root)
	console.print(f"  Found [bold]{len(scripts)}[/bold] generator scripts")

	# Shuffle if requested (useful with --limit for testing variety)
	if args.shuffle:
		random.shuffle(scripts)

	# Apply limit if specified
	if args.limit is not None:
		scripts = scripts[:args.limit]
		console.print(f"  Limited to [bold]{args.limit}[/bold] scripts")

	# Dry run: show expanded (script, flags) work list
	if args.dry_run:
		console.print("\n--- Dry run: variants to classify ---", style="bold")
		dry_total = 0
		for script_path in scripts:
			variants = csv_handler.get_variants_for_script(assignments, script_path)
			for v in variants:
				flags_label = f" [yellow]{v['flags']}[/yellow]" if v["flags"] else ""
				console.print(f"  [cyan]{script_path}[/cyan]{flags_label}")
				dry_total += 1
		console.print(f"\nTotal: [bold]{dry_total}[/bold] variants across [bold]{len(scripts)}[/bold] scripts")
		console.print(f"Subjects available: [cyan]{', '.join(sorted(all_indexes.keys()))}[/cyan]")
		console.print(f"Existing assignments: [bold]{len(assignments)}[/bold]")
		return

	# Create LLM client with strict transport selection
	# --model implies --ollama
	use_ollama = args.use_ollama or (args.model is not None)
	# Validate Ollama model exists locally before starting
	if args.model:
		validate_ollama_model(args.model)
	# Report which transport and model will be used
	if use_ollama:
		ollama_model = args.model if args.model else llm.choose_model(None)
		console.print(f"Using Ollama model: [cyan]{ollama_model}[/cyan]")
	else:
		console.print("Using Apple Intelligence")
	client = create_llm_client(args.model, use_ollama=use_ollama)

	num_repeats = max(1, args.repeat)

	# Expand each discovered script into one work item per CSV variant
	# (script, flags, input). Scripts not in any CSV get a single empty
	# variant so classification still runs once with no flags.
	work_items = []
	for script_path in scripts:
		variants = csv_handler.get_variants_for_script(assignments, script_path)
		for variant in variants:
			work_items.append((script_path, variant["flags"], variant["input"]))

	# Classify all (script, flags, input) work items
	results = []
	no_bbq_scripts = []
	llm_error_scripts = []
	# For repeat mode: collect all runs per (script, flags) variant
	repeat_results = {}
	total_start = time.monotonic()
	for i, (script_path, flags, input_file) in enumerate(work_items):
		# Variant key distinguishes same script with different flags
		variant_key = f"{script_path}|{flags}"
		# Build ETA string from average of completed items
		if i > 0:
			elapsed_so_far = time.monotonic() - total_start
			avg_per_item = elapsed_so_far / i
			remaining = avg_per_item * (len(work_items) - i)
			eta_str = _format_duration(remaining)
			elapsed_str = _format_duration(elapsed_so_far)
			timing_info = f" | elapsed {elapsed_str} | ETA {eta_str}"
		else:
			timing_info = ""
		flags_label = f" [yellow]{flags}[/yellow]" if flags else ""
		console.print(f"\n[bold][{i+1}/{len(work_items)}][/bold] Classifying [cyan]{script_path}[/cyan]{flags_label}{timing_info}")
		script_start = time.monotonic()
		for run_num in range(num_repeats):
			if num_repeats > 1:
				console.print(f"  run {run_num+1}/{num_repeats}", style="dim")
			try:
				result = classify_one_script(
					client, script_path, repo_root,
					all_indexes, cross_examples, assignments,
					flags=flags, input_file=input_file,
					source_only=args.source_only,
					verbose=args.verbose,
				)
			except (RuntimeError, llm.LLMError, subprocess.TimeoutExpired) as exc:
				console.print(f"  ERROR: {exc}", style="bold red")
				if run_num == 0:
					llm_error_scripts.append(variant_key)
				continue

			if result is None:
				if run_num == 0:
					no_bbq_scripts.append(variant_key)
				# No point repeating if no bbq file
				break

			results.append(result)

			# Collect for consistency report keyed by variant
			if variant_key not in repeat_results:
				repeat_results[variant_key] = []
			repeat_results[variant_key].append(result)

			# Write debug log incrementally for crash recovery
			write_debug_log(result, debug_dir)

			topic_label = result.get("topic_name", result["topic"])
			if num_repeats > 1:
				# Condensed one-liner per run in repeat mode
				status_tag = "[green]OK[/green]" if result["status"] == "classified" else "[yellow]??[/yellow]"
				console.print(
					f"    {status_tag} {result['chapter']}/{result['topic']} "
					f"[cyan]{topic_label}[/cyan] ({result['confidence_score']})")
			else:
				if result["status"] == "classified":
					console.print(
						f"  [bold green][OK][/bold green] {result['chapter']}/{result['topic']} "
						f"[cyan]{topic_label}[/cyan] (score: {result['confidence_score']})")
				else:
					console.print(
						f"  [bold yellow][??][/bold yellow] {result['chapter']}/{result['topic']} "
						f"[cyan]{topic_label}[/cyan] (score: {result['confidence_score']})")

		# Per-variant mini-rollup after all repeats
		if num_repeats > 1 and variant_key in repeat_results:
			runs = repeat_results[variant_key]
			# Count votes
			subj_votes = {}
			topic_votes = {}
			for r in runs:
				subj_votes[r["chapter"]] = subj_votes.get(r["chapter"], 0) + 1
				topic_votes[r["topic"]] = topic_votes.get(r["topic"], 0) + 1
			top_subj = max(subj_votes, key=subj_votes.get)
			top_topic = max(topic_votes, key=topic_votes.get)
			top_topic_name = ""
			for r in runs:
				if r["topic"] == top_topic and r.get("topic_name"):
					top_topic_name = r["topic_name"]
					break
			# Stability check
			n = len(runs)
			threshold = (2 * n + 2) // 3
			all_same = (subj_votes[top_subj] == n and topic_votes[top_topic] == n)
			subj_stable = subj_votes[top_subj] >= threshold
			topic_stable = topic_votes[top_topic] >= threshold
			if n < num_repeats:
				status_label = "[dim]INCOMPLETE[/dim]"
			elif all_same:
				status_label = "[green]STABLE[/green]"
			elif subj_stable and topic_stable:
				status_label = "[yellow]MOSTLY_STABLE[/yellow]"
			else:
				status_label = "[red]UNSTABLE[/red]"
			# Format vote strings -- compact when unanimous
			if subj_votes[top_subj] == n:
				subj_str = f"subject {top_subj} {n}/{n}"
			else:
				subj_str = "subject " + ", ".join(
					f"{s} {c}" for s, c in sorted(subj_votes.items(), key=lambda x: -x[1]))
			if topic_votes[top_topic] == n:
				topic_str = f"topic {top_topic} {n}/{n}"
			else:
				# Include subject prefix when subjects differ
				if len(subj_votes) > 1:
					# Build subject/topic pairs from runs
					pair_votes = {}
					for r in runs:
						pair = f"{r['chapter']}/{r['topic']}"
						pair_votes[pair] = pair_votes.get(pair, 0) + 1
					topic_str = "topic " + ", ".join(
						f"{p} {c}" for p, c in sorted(pair_votes.items(), key=lambda x: -x[1]))
				else:
					topic_str = "topic " + ", ".join(
						f"{t} {c}" for t, c in sorted(topic_votes.items(), key=lambda x: -x[1]))
			# Print 2-3 line rollup
			final_label = f"{top_subj}/{top_topic}"
			if top_topic_name:
				final_label += f" {top_topic_name}"
			console.print("  [magenta]--------------------------------------------------[/magenta]")
			console.print(f"  [magenta][{n}x][/magenta] final=[cyan]{final_label}[/cyan] | status={status_label}")
			console.print(f"  [magenta]votes:[/magenta] {subj_str} | {topic_str}")

		# Per-script timing
		script_elapsed = time.monotonic() - script_start
		console.print(f"  completed in {_format_duration(script_elapsed)}", style="dim")

	# Total elapsed time
	total_elapsed = time.monotonic() - total_start
	console.print(f"\nTotal classification time: [bold]{_format_duration(total_elapsed)}[/bold]")

	# Write result CSVs using first run results only (avoid duplicates).
	# Dedup by (script, flags) so each variant is emitted exactly once.
	first_run_results = []
	seen_variants = set()
	for r in results:
		variant_key = (r["script"], r["flags"])
		if variant_key not in seen_variants:
			first_run_results.append(r)
			seen_variants.add(variant_key)

	console.print(f"\nWriting result CSVs to [cyan]{results_dir}[/cyan]...", style="dim italic")
	written = csv_handler.write_result_csvs(first_run_results, results_dir)
	for f in written:
		console.print(f"  Written: [green]{f}[/green]")

	# Write no_bbq_file.csv for scripts that produced no output
	if no_bbq_scripts:
		no_bbq_path = os.path.join(results_dir, "no_bbq_file.csv")
		with open(no_bbq_path, "w") as f:
			f.write("script\n")
			for s in sorted(no_bbq_scripts):
				f.write(f"{s}\n")
		console.print(f"  Written: [green]{no_bbq_path}[/green] ([bold]{len(no_bbq_scripts)}[/bold] scripts)")

	# Write llm_errors.csv for scripts that failed during LLM classification
	if llm_error_scripts:
		error_path = os.path.join(results_dir, "llm_errors.csv")
		with open(error_path, "w") as f:
			f.write("script\n")
			for s in sorted(llm_error_scripts):
				f.write(f"{s}\n")
		console.print(f"  Written: [green]{error_path}[/green] ([bold]{len(llm_error_scripts)}[/bold] scripts)")

	# Show diff report if requested or always show summary
	if args.diff_mode or True:
		console.print("\n--- Classification Report ---", style="bold")
		print_diff_report(first_run_results)

	# Show consistency report for repeat mode
	if num_repeats > 1 and repeat_results:
		print_consistency_report(repeat_results, num_repeats)

#============================================
if __name__ == '__main__':
	main()
