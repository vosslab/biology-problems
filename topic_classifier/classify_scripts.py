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
import urllib.error
import urllib.request

# PIP3 modules
import rich.console

# Add local-llm-wrapper to path if not already importable
_LLM_WRAPPER_DIR = os.path.join(os.path.expanduser("~"), "nsh", "local-llm-wrapper")
if _LLM_WRAPPER_DIR not in sys.path:
	sys.path.insert(0, _LLM_WRAPPER_DIR)

# PIP3 modules
import local_llm_wrapper.llm as llm

console = rich.console.Console(highlight=False)

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
def validate_ollama_model(model: str, base_url: str = "http://localhost:11434") -> None:
	"""Verify that model is installed locally in Ollama.

	Args:
		model: exact Ollama model name to check
		base_url: Ollama server URL

	Raises:
		RuntimeError: if model is not available locally
	"""
	url = f"{base_url}/api/tags"
	request = urllib.request.Request(url)
	try:
		response = urllib.request.urlopen(request, timeout=15)
	except (urllib.error.URLError, TimeoutError):
		raise RuntimeError(
			f"Cannot connect to Ollama at {base_url}\n"
			"Start Ollama first: ollama serve")
	data = json.loads(response.read().decode("utf-8"))
	# Extract model names from Ollama API response
	local_models = [m["name"] for m in data.get("models", [])]
	if model not in local_models:
		installed_str = ", ".join(local_models) if local_models else "none"
		msg = (f"Requested Ollama model not available locally: {model}\n"
			f"Installed models: {installed_str}\n"
			f"Install with: ollama pull {model}\n"
			"Or run with --ollama to use the default RAM-selected model.")
		raise RuntimeError(msg)

#============================================
def create_llm_client(model: str | None = None, use_ollama: bool = False) -> llm.LLMClient:
	"""Create an LLM client with strict transport selection.

	Args:
		model: exact Ollama model name (requires use_ollama=True)
		use_ollama: if True, use Ollama only; if False, use Apple only

	Returns:
		configured LLMClient
	"""
	if use_ollama:
		# Use exact model if specified, otherwise auto-select by RAM
		ollama_model = model if model else llm.choose_model(None)
		transport = llm.OllamaTransport(model=ollama_model)
	else:
		# Apple Intelligence only, no fallback
		transport = llm.AppleTransport()
	client = llm.LLMClient(transports=[transport], quiet=True)
	return client

MAX_RESPONSE_LENGTH = 2000

#============================================
def _check_response(response: str, required_tags: list = None) -> list:
	"""Check an LLM response for quality problems.

	Args:
		response: raw LLM response text
		required_tags: XML tag names that must have non-empty content

	Returns:
		list of problem description strings (empty if OK)
	"""
	problems = []
	if len(response) > MAX_RESPONSE_LENGTH:
		problems.append(f"too long ({len(response)} chars)")
	if required_tags:
		missing = [
			tag for tag in required_tags
			if not llm.extract_xml_tag_content(response, tag)
		]
		if missing:
			problems.append(f"missing tags: {', '.join(missing)}")
	return problems

#============================================
def _generate_with_retry(
	client: llm.LLMClient,
	messages: list,
	max_tokens: int,
	required_tags: list = None,
	max_retries: int = 3,
	verbose: bool = False,
) -> str:
	"""Call client.generate and retry on bad responses.

	Retries with a fresh call (no conversation stacking) since
	small local models do not reliably self-correct from their
	own broken output.

	Args:
		client: LLM client
		messages: chat message list
		max_tokens: token limit for generation
		required_tags: list of XML tag names that must be present
		max_retries: total number of attempts
		verbose: show full failed response text

	Returns:
		LLM response string (best attempt)
	"""
	best_response = None
	fewest_problems = None
	for attempt in range(max_retries):
		response = client.generate(messages=messages, max_tokens=max_tokens)
		problems = _check_response(response, required_tags)
		# Track the best response (fewest problems)
		if fewest_problems is None or len(problems) < fewest_problems:
			best_response = response
			fewest_problems = len(problems)
		if not problems:
			return response
		console.print(f"  {', '.join(problems)}", style="yellow")
		if verbose:
			# Show less for length-only failures, more for missing tags
			is_length_only = len(problems) == 1 and "too long" in problems[0]
			trim = 250 if is_length_only else 1500
			display = response[:trim] if len(response) > trim else response
			console.print(f"  failed response ({len(response)} chars):", style="dim")
			console.print(f"    {display}", style="dim")
		console.print(f"  retrying... {attempt + 1} of {max_retries}", style="yellow")
	# Return best attempt
	return best_response

#============================================
def _parse_confidence(raw: str) -> int:
	"""Parse LLM confidence string to an integer 1-5, default 1.

	Args:
		raw: raw string from LLM (e.g. '4', 'high', etc.)

	Returns:
		integer 1-5
	"""
	if not raw:
		return 1
	cleaned = raw.strip()
	# Extract first digit if present
	for ch in cleaned:
		if ch.isdigit():
			val = int(ch)
			# Clamp to 1-5
			return max(1, min(5, val))
	# Fallback for legacy categorical values
	mapping = {"high": 4, "medium": 3, "low": 2}
	return mapping.get(cleaned.lower(), 1)

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
		valid_topics = [t["topic_id"] for t in all_indexes[subject]["topics"]]
		if topic in valid_topics:
			score += 1

	# +1 for LLM self-reported high confidence (both stages >= 4)
	if stage1["confidence"] >= 4 and stage2["confidence"] >= 4:
		score += 1

	return score

#============================================
def classify_one_script(
	client: llm.LLMClient,
	script_path: str,
	repo_root: str,
	all_indexes: dict,
	cross_examples: list,
	assignments: dict,
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
		# Build extra args from existing CSV assignment (flags, input)
		extra_args = _get_run_args(script_path, assignments)
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
		result = _make_failed_result(script_path, execution_status, stage1)
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
		result = _make_failed_result(script_path, execution_status, stage1, stage2)
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
		if verbose:
			if match:
				console.print(f"    existing: [green]{existing_assignment} (match)[/green]")
			else:
				console.print(f"    existing: [red]{existing_assignment} (disagree)[/red]")

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
		"stage1_confidence": stage1.get("confidence", 1),
		"stage2_reasoning": stage2.get("reasoning", "") if stage2 else "",
		"stage2_confidence": stage2.get("confidence", 1) if stage2 else 1,
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
			console.print(f"[yellow]REVIEW[/yellow]   {script_name} -> {predicted} "
				f"(score: {r['confidence_score']}, exec: {r['execution']})")
			reviews += 1
		elif r["existing"] is None:
			console.print(f"[cyan]NEW[/cyan]      {script_name} -> {predicted}")
			new_scripts += 1
		elif r["match"]:
			console.print(f"[green]MATCH[/green]    {script_name} -> {predicted}")
			matches += 1
		else:
			console.print(f"[red]DISAGREE[/red] {script_name} -> {predicted} "
				f"(existing: {r['existing']})")
			disagreements += 1

	console.print(f"\nSummary: [green]{matches} matches[/green], "
		f"[cyan]{new_scripts} new[/cyan], "
		f"[red]{disagreements} disagreements[/red], "
		f"[yellow]{reviews} review[/yellow]")

#============================================
def print_consistency_report(repeat_results: dict, num_repeats: int) -> None:
	"""Print a condensed per-script rollup for repeated classification runs.

	Shows one block per script with vote counts, topic name, existing
	assignment comparison, and stability status.

	Args:
		repeat_results: dict mapping script_path to list of result dicts
		num_repeats: number of repeats per script
	"""
	console.print(f"\n--- Consistency Report ({num_repeats} runs per script) ---", style="bold")
	stable_count = 0
	flagged_count = 0
	total_scripts = len(repeat_results)

	for script_path, run_results in sorted(repeat_results.items()):
		script_name = os.path.basename(script_path)

		# Count subject and topic votes
		subject_votes = {}
		topic_votes = {}
		confidences = []
		topic_names = {}
		existing = None
		for r in run_results:
			subj = r["chapter"]
			subject_votes[subj] = subject_votes.get(subj, 0) + 1
			top = r["topic"]
			topic_votes[top] = topic_votes.get(top, 0) + 1
			confidences.append(r["confidence_score"])
			# Track topic names for display
			if r.get("topic_name"):
				topic_names[top] = r["topic_name"]
			if r.get("existing") and existing is None:
				existing = r["existing"]

		# Find majority subject and topic
		top_subject = max(subject_votes, key=subject_votes.get)
		top_subject_count = subject_votes[top_subject]
		top_topic = max(topic_votes, key=topic_votes.get)
		top_topic_count = topic_votes[top_topic]
		top_topic_name = topic_names.get(top_topic, "")

		# Check stability threshold (2/3 agreement)
		threshold = (2 * num_repeats + 2) // 3
		subject_stable = top_subject_count >= threshold
		topic_stable = top_topic_count >= threshold
		is_stable = subject_stable and topic_stable

		# Format confidence range
		conf_min = min(confidences)
		conf_max = max(confidences)
		conf_str = f"{conf_min}" if conf_min == conf_max else f"{conf_min}-{conf_max}"

		# Build final assignment string
		final_label = f"{top_subject}/{top_topic}"
		if top_topic_name:
			final_label += f" ({top_topic_name})"

		# Status tag
		if is_stable:
			stable_count += 1
			tag = "[green]STABLE[/green]  "
		else:
			flagged_count += 1
			tag = "[red]UNSTABLE[/red]"

		# One-line rollup
		console.print(f"  {tag} {script_name}")
		# Subject votes
		subj_parts = [f"{s}: {c}/{num_repeats}" for s, c in sorted(subject_votes.items(), key=lambda x: -x[1])]
		console.print(f"    subject: {', '.join(subj_parts)}", style="dim")
		# Topic votes
		topic_parts = []
		for t, c in sorted(topic_votes.items(), key=lambda x: -x[1]):
			tname = topic_names.get(t, "")
			tlabel = f"{t} {tname}" if tname else t
			topic_parts.append(f"{tlabel}: {c}/{num_repeats}")
		console.print(f"    topic:   {', '.join(topic_parts)}", style="dim")
		# Final and confidence
		console.print(f"    final:   [cyan]{final_label}[/cyan]  conf: {conf_str}")
		# Existing comparison
		if existing:
			match_str = "[green]match[/green]" if existing == f"{top_subject}/{top_topic}" else "[red]disagree[/red]"
			console.print(f"    existing: {existing} ({match_str})")

	# Summary
	console.print(
		f"\n  [green]{stable_count}[/green]/{total_scripts} stable, "
		f"[red]{flagged_count}[/red] flagged")

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

	# Dry run: just show what would be classified
	if args.dry_run:
		console.print("\n--- Dry run: scripts to classify ---", style="bold")
		for s in scripts:
			console.print(f"  [cyan]{s}[/cyan]")
		console.print(f"\nTotal: [bold]{len(scripts)}[/bold] scripts")
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

	# Classify all scripts
	results = []
	no_bbq_scripts = []
	llm_error_scripts = []
	# For repeat mode: collect all runs per script
	repeat_results = {}
	for i, script_path in enumerate(scripts):
		console.print(f"\n[bold][{i+1}/{len(scripts)}][/bold] Classifying [cyan]{script_path}[/cyan]")
		for run_num in range(num_repeats):
			if num_repeats > 1:
				console.print(f"  run {run_num+1}/{num_repeats}", style="dim")
			try:
				result = classify_one_script(
					client, script_path, repo_root,
					all_indexes, cross_examples, assignments,
					source_only=args.source_only,
					verbose=args.verbose,
				)
			except (RuntimeError, llm.LLMError, subprocess.TimeoutExpired) as exc:
				console.print(f"  ERROR: {exc}", style="bold red")
				if run_num == 0:
					llm_error_scripts.append(script_path)
				continue

			if result is None:
				if run_num == 0:
					no_bbq_scripts.append(script_path)
				# No point repeating if no bbq file
				break

			results.append(result)

			# Collect for consistency report
			if script_path not in repeat_results:
				repeat_results[script_path] = []
			repeat_results[script_path].append(result)

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

		# Per-script mini-rollup after all repeats
		if num_repeats > 1 and script_path in repeat_results:
			runs = repeat_results[script_path]
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

	# Write result CSVs using first run results only (avoid duplicates)
	first_run_results = []
	seen_scripts = set()
	for r in results:
		if r["script"] not in seen_scripts:
			first_run_results.append(r)
			seen_scripts.add(r["script"])

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
