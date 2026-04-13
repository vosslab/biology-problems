#!/usr/bin/env python3

"""Classify multiple-choice-statement and matching-set YAML files into topics.

Mirrors topic_classifier/classify_scripts.py for the 99 yaml content files
under problems/multiple_choice_statements/ and problems/matching_sets/.
Uses the same two-stage local-LLM pipeline (subject -> topic) and writes
per-subject result CSVs in bbq_control YMCS/YMATCH row format so they can
be consumed directly by run_bbq_tasks.py.
"""

# Standard Library
import os
import re
import glob
import time
import random
import argparse
import subprocess

# PIP3 modules
import yaml

# local repo modules
import topic_classifier.index_parser as index_parser
import topic_classifier.csv_handler as csv_handler
import topic_classifier.prompt_builder as prompt_builder
import topic_classifier.classifier_common as common

llm = common.llm
console = common.console

#============================================
BBQ_CONTROL_DIR = os.path.join(
	os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
	"..", "biology-problems-website", "bbq_control",
)

# Cap rendered yaml content so very long matching sets do not blow prompt budget
MAX_CONTENT_CHARS = 2000

_HTML_TAG_RE = re.compile(r"<[^>]+>")

#============================================
def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments."""
	parser = argparse.ArgumentParser(
		description="Classify YAML content files into textbook topics using a local LLM.",
	)
	parser.add_argument(
		'-o', '--output', dest='output_dir', type=str,
		default=None,
		help="Output directory for result CSVs (default: ./results-yaml/ in CWD)",
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
			"Examples: gpt-oss:20b, phi4:14b-q4_K_M"),
	)
	parser.add_argument(
		'-n', '--dry-run', dest='dry_run', action='store_true',
		help="Show what would be classified without calling LLM",
	)
	parser.add_argument(
		'-l', '--limit', dest='limit', type=int, default=None,
		help="Process only first N yaml files (for testing)",
	)
	parser.add_argument(
		'-s', '--shuffle', dest='shuffle', action='store_true',
		help="Shuffle yaml order before processing (useful with --limit)",
	)
	parser.add_argument(
		'-v', '--verbose', dest='verbose', action='store_true',
		help="Show extra debug output (reasoning, raw content, retries)",
	)
	parser.add_argument(
		'-r', '--repeat', dest='repeat', type=int, default=1,
		help="Classify each yaml N times and report consistency (default: 1)",
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
def setup_output_dirs(output_dir: str) -> tuple:
	"""Set up output and debug directories.

	Args:
		output_dir: user-specified output dir or None

	Returns:
		tuple of (results_dir, debug_dir)
	"""
	# Default output is ./results-yaml/ in the CWD so invocation from repo root
	# keeps outputs alongside the other classifier artifacts.
	if output_dir is None:
		results_dir = os.path.join(os.getcwd(), "results-yaml")
	else:
		results_dir = output_dir
	classifier_dir = os.path.dirname(os.path.abspath(__file__))
	debug_dir = os.path.join(classifier_dir, "output")

	os.makedirs(results_dir, exist_ok=True)
	os.makedirs(debug_dir, exist_ok=True)

	return results_dir, debug_dir

#============================================
def discover_yaml_files(repo_root: str) -> list:
	"""Discover all classifiable yaml files under problems/.

	Args:
		repo_root: repository root path

	Returns:
		sorted list of yaml paths relative to repo_root
	"""
	mcs_pattern = os.path.join(repo_root, "problems/multiple_choice_statements/*/*.yml")
	match_pattern = os.path.join(repo_root, "problems/matching_sets/*/*.yml")
	mcs_files = sorted(glob.glob(mcs_pattern))
	match_files = sorted(glob.glob(match_pattern))
	all_files = mcs_files + match_files
	rel_paths = [os.path.relpath(p, repo_root) for p in all_files]
	return rel_paths

#============================================
def _strip_html(text: str) -> str:
	"""Remove HTML tags from a string; leave entities intact."""
	if not text:
		return ""
	stripped = _HTML_TAG_RE.sub("", str(text))
	return stripped

#============================================
def _extract_mcs_content(data: dict) -> str:
	"""Render a multiple-choice-statements yaml into LLM-ready text.

	Args:
		data: parsed yaml dict

	Returns:
		rendered text block (topic + true/false statements)
	"""
	lines = []
	topic_line = _strip_html(data.get("topic", "")).strip()
	if topic_line:
		lines.append(f"Topic: {topic_line}")
		lines.append("")

	true_statements = data.get("true_statements") or {}
	if true_statements:
		lines.append("True statements:")
		for _label, sentence in sorted(true_statements.items()):
			lines.append(f"- {_strip_html(sentence).strip()}")
		lines.append("")

	false_statements = data.get("false_statements") or {}
	if false_statements:
		lines.append("False statements:")
		for _label, sentence in sorted(false_statements.items()):
			lines.append(f"- {_strip_html(sentence).strip()}")

	rendered = "\n".join(lines).strip()
	if len(rendered) > MAX_CONTENT_CHARS:
		rendered = rendered[:MAX_CONTENT_CHARS] + "\n... [truncated]"
	return rendered

#============================================
def _extract_matching_content(data: dict) -> str:
	"""Render a matching-sets yaml into LLM-ready text.

	Args:
		data: parsed yaml dict

	Returns:
		rendered text block (key/value descriptions + pairs)
	"""
	lines = []
	# Some yamls use 'key description', others 'keys description'; same for values
	keys_desc = data.get("keys description") or data.get("key description") or ""
	values_desc = data.get("values description") or data.get("value description") or ""
	if keys_desc:
		lines.append(f"Keys: {_strip_html(keys_desc).strip()}")
	if values_desc:
		lines.append(f"Values: {_strip_html(values_desc).strip()}")
	if lines:
		lines.append("")

	pairs = data.get("matching pairs") or {}
	if pairs:
		lines.append("Pairs:")
		for key, values in pairs.items():
			lines.append(f"- {_strip_html(key).strip()}:")
			if isinstance(values, list):
				for value in values:
					lines.append(f"  * {_strip_html(value).strip()}")
			else:
				lines.append(f"  * {_strip_html(values).strip()}")

	rendered = "\n".join(lines).strip()
	# Trim from the middle (keep header + first few pairs) if too long
	if len(rendered) > MAX_CONTENT_CHARS:
		rendered = rendered[:MAX_CONTENT_CHARS] + "\n... [truncated]"
	return rendered

#============================================
def _extract_yaml_content(abs_path: str, rel_path: str) -> tuple:
	"""Parse a yaml file and return its marker + rendered content.

	Args:
		abs_path: absolute path to the yaml file
		rel_path: repo-relative path

	Returns:
		(marker, content_text) where marker is 'YMCS' or 'YMATCH'

	Raises:
		ValueError: if path shape or content schema is unrecognized
	"""
	if "/multiple_choice_statements/" in rel_path:
		marker = "YMCS"
	elif "/matching_sets/" in rel_path:
		marker = "YMATCH"
	else:
		raise ValueError(f"unexpected yaml path (not mcs or matching): {rel_path}")

	with open(abs_path, "r") as f:
		data = yaml.safe_load(f)
	if not isinstance(data, dict):
		raise ValueError(f"yaml root is not a mapping: {rel_path}")

	if marker == "YMCS":
		content = _extract_mcs_content(data)
	else:
		content = _extract_matching_content(data)

	if not content:
		raise ValueError(f"yaml produced empty content: {rel_path}")

	return marker, content

#============================================
def classify_stage1(
	client: llm.LLMClient,
	yaml_path: str,
	content: str,
	all_indexes: dict,
	cross_examples: list,
	verbose: bool = False,
) -> dict:
	"""Run stage 1 (subject) classification on a yaml file.

	Args:
		client: LLM client
		yaml_path: relative path to yaml
		content: rendered yaml text
		all_indexes: subject index data
		cross_examples: cross-subject few-shot examples
		verbose: show retries

	Returns:
		dict with subject, confidence, reasoning, raw_response
	"""
	messages = prompt_builder.build_stage1_yaml_prompt(
		yaml_path, content, all_indexes, cross_examples,
	)
	response = common.generate_with_retry(
		client, messages, max_tokens=500,
		required_tags=["subject", "confidence"],
		verbose=verbose,
	)
	subject = llm.extract_xml_tag_content(response, "subject")
	confidence_raw = llm.extract_xml_tag_content(response, "confidence")
	reasoning = llm.extract_xml_tag_content(response, "reasoning")
	result = {
		"subject": subject.strip() if subject else None,
		"confidence": common.parse_confidence(confidence_raw),
		"reasoning": reasoning.strip() if reasoning else None,
		"raw_response": response,
	}
	return result

#============================================
def classify_stage2(
	client: llm.LLMClient,
	yaml_path: str,
	content: str,
	subject: str,
	topics: list,
	subject_examples: list,
	verbose: bool = False,
) -> dict:
	"""Run stage 2 (topic) classification on a yaml file.

	Args:
		client: LLM client
		yaml_path: relative path to yaml
		content: rendered yaml text
		subject: predicted subject from stage 1
		topics: topic list for this subject
		subject_examples: few-shot examples from this subject
		verbose: show retries

	Returns:
		dict with topic, confidence, reasoning, raw_response
	"""
	messages = prompt_builder.build_stage2_yaml_prompt(
		yaml_path, content, subject, topics, subject_examples,
	)
	response = common.generate_with_retry(
		client, messages, max_tokens=800,
		required_tags=["topic", "confidence"],
		verbose=verbose,
	)
	topic = llm.extract_xml_tag_content(response, "topic")
	confidence_raw = llm.extract_xml_tag_content(response, "confidence")
	reasoning = llm.extract_xml_tag_content(response, "reasoning")
	result = {
		"topic": topic.strip() if topic else None,
		"confidence": common.parse_confidence(confidence_raw),
		"reasoning": reasoning.strip() if reasoning else None,
		"raw_response": response,
	}
	return result

#============================================
def _yaml_input_path(rel_path: str) -> str:
	"""Convert 'problems/<...>/foo.yml' to '{bp_root}/<...>/foo.yml'."""
	if rel_path.startswith("problems/"):
		return "{bp_root}/" + rel_path[len("problems/"):]
	return rel_path

#============================================
def _find_existing(rel_path: str, marker: str, assignments: dict) -> dict:
	"""Look up an existing bbq_control entry for this yaml file.

	Args:
		rel_path: repo-relative yaml path
		marker: 'YMCS' or 'YMATCH'
		assignments: output of csv_handler.read_existing_assignments

	Returns:
		matching entry dict or None
	"""
	bp_root_path = _yaml_input_path(rel_path)
	basename = os.path.basename(rel_path)
	for _key, entry in assignments.items():
		entry_input = entry.get("input", "").strip()
		# Match full bp_root path or bare basename (legacy bbq_tasks.csv style)
		if entry_input == bp_root_path or entry_input == basename:
			return entry
	return None

#============================================
def classify_one_yaml(
	client: llm.LLMClient,
	rel_path: str,
	repo_root: str,
	all_indexes: dict,
	cross_examples: list,
	assignments: dict,
	verbose: bool = False,
) -> dict:
	"""Classify a single yaml file through subject + topic stages.

	Args:
		client: LLM client
		rel_path: repo-relative yaml path
		repo_root: repository root
		all_indexes: subject index data
		cross_examples: cross-subject few-shot examples
		assignments: existing CSV assignments
		verbose: show extra debug

	Returns:
		result dict, or None if content extraction failed
	"""
	abs_path = os.path.join(repo_root, rel_path)
	try:
		marker, content = _extract_yaml_content(abs_path, rel_path)
	except (ValueError, yaml.YAMLError) as exc:
		console.print(f"  SKIP: {exc}", style="yellow")
		return None

	if verbose:
		console.print(f"  marker: [cyan]{marker}[/cyan], content: {len(content)} chars", style="dim")
		console.print("  --- Rendered content ---", style="dim")
		for line in content.strip().split("\n"):
			console.print(f"    {line}", style="dim")
		console.print("  --- End rendered content ---", style="dim")

	console.print("  Classifying subject...", style="dim")
	stage1 = classify_stage1(
		client, rel_path, content, all_indexes, cross_examples, verbose=verbose,
	)
	if stage1["subject"] is None:
		console.print("  FAILED: could not determine subject", style="bold red")
		result = common.make_failed_result(rel_path, "success", stage1)
		result["script"] = marker
		result["input"] = _yaml_input_path(rel_path)
		return result

	subject = stage1["subject"]
	conf = stage1["confidence"]
	conf_color = "green" if conf >= 4 else ("yellow" if conf >= 3 else "red")
	console.print(f"  Subject: [bold cyan]{subject}[/bold cyan] ([{conf_color}]{conf}/5[/{conf_color}])")
	if verbose and stage1.get("reasoning"):
		console.print(f"    reasoning: {stage1['reasoning']}", style="dim")

	subject_data = all_indexes.get(subject, {"topics": []})
	topics = subject_data["topics"]
	subject_examples = csv_handler.get_examples_for_subject(assignments, subject)

	console.print(f"  Classifying topic within [bold cyan]{subject}[/bold cyan]...", style="dim")
	stage2 = classify_stage2(
		client, rel_path, content, subject, topics, subject_examples, verbose=verbose,
	)
	if stage2["topic"] is None:
		console.print("  FAILED: could not determine topic", style="bold red")
		result = common.make_failed_result(rel_path, "success", stage1, stage2)
		result["script"] = marker
		result["input"] = _yaml_input_path(rel_path)
		return result

	topic_name = common.get_topic_name(topics, stage2["topic"])
	conf2 = stage2["confidence"]
	conf2_color = "green" if conf2 >= 4 else ("yellow" if conf2 >= 3 else "red")
	console.print(f"  Topic: [bold cyan]{stage2['topic']}[/bold cyan] {topic_name} "
		f"([{conf2_color}]{conf2}/5[/{conf2_color}])")
	if verbose and stage2.get("reasoning"):
		console.print(f"    reasoning: {stage2['reasoning']}", style="dim")

	confidence_score = common.compute_confidence_score(stage1, stage2, True, all_indexes)
	status = "classified" if confidence_score >= 3 else "review"

	existing_entry = _find_existing(rel_path, marker, assignments)
	existing_assignment = None
	match = None
	if existing_entry is not None:
		existing_subject = existing_entry.get("subject") or existing_entry.get("chapter")
		existing_assignment = f"{existing_subject}/{existing_entry['topic']}"
		match = (existing_subject == subject and existing_entry["topic"] == stage2["topic"])
		if verbose:
			label = "[green]match[/green]" if match else "[red]disagree[/red]"
			console.print(f"    existing: {existing_assignment} ({label})")

	result = {
		"script": marker,
		"subject": subject,
		"topic": stage2["topic"],
		"flags": "",
		"input": _yaml_input_path(rel_path),
		"notes": "",
		"confidence_score": confidence_score,
		"status": status,
		"execution": "success",
		"existing": existing_assignment,
		"match": match,
		"yaml_path": rel_path,
		"stage1_reasoning": stage1["reasoning"],
		"stage1_confidence": stage1["confidence"],
		"stage2_reasoning": stage2.get("reasoning"),
		"stage2_confidence": stage2["confidence"],
		"topic_name": topic_name,
	}
	return result

#============================================
def main():
	"""Main entry point for the yaml classifier."""
	args = parse_args()
	repo_root = get_repo_root()

	results_dir, debug_dir = setup_output_dirs(args.output_dir)

	console.print("Loading subject indexes...", style="dim italic")
	all_indexes = index_parser.load_all_indexes()

	console.print("Loading existing CSV assignments...", style="dim italic")
	bbq_control_dir = os.path.realpath(BBQ_CONTROL_DIR)
	if os.path.isdir(bbq_control_dir):
		assignments = csv_handler.read_existing_assignments(bbq_control_dir)
		console.print(f"  Loaded [bold]{len(assignments)}[/bold] existing assignments")
	else:
		console.print(f"  WARNING: bbq_control dir not found at {bbq_control_dir}", style="yellow")
		assignments = {}

	cross_examples = csv_handler.get_cross_subject_examples(assignments)

	console.print("Discovering YAML files...", style="dim italic")
	yaml_files = discover_yaml_files(repo_root)
	console.print(f"  Found [bold]{len(yaml_files)}[/bold] yaml files")

	if args.shuffle:
		random.shuffle(yaml_files)

	if args.limit is not None:
		yaml_files = yaml_files[:args.limit]
		console.print(f"  Limited to [bold]{args.limit}[/bold] files")

	if args.dry_run:
		console.print("\n--- Dry run: yaml files to classify ---", style="bold")
		for p in yaml_files:
			console.print(f"  [cyan]{p}[/cyan]")
		console.print(f"\nTotal: [bold]{len(yaml_files)}[/bold] files")
		console.print(f"Subjects available: [cyan]{', '.join(sorted(all_indexes.keys()))}[/cyan]")
		console.print(f"Existing assignments: [bold]{len(assignments)}[/bold]")
		return

	use_ollama = args.use_ollama or (args.model is not None)
	if args.model:
		common.validate_ollama_model(args.model)
	if use_ollama:
		ollama_model = args.model if args.model else llm.choose_model(None)
		console.print(f"Using Ollama model: [cyan]{ollama_model}[/cyan]")
	else:
		console.print("Using Apple Intelligence")
	client = common.create_llm_client(args.model, use_ollama=use_ollama)

	num_repeats = max(1, args.repeat)

	results = []
	extraction_failures = []
	llm_error_files = []
	repeat_results = {}
	total_start = time.monotonic()

	for i, rel_path in enumerate(yaml_files):
		if i > 0:
			elapsed_so_far = time.monotonic() - total_start
			avg_per_item = elapsed_so_far / i
			remaining = avg_per_item * (len(yaml_files) - i)
			eta_str = common.format_duration(remaining)
			elapsed_str = common.format_duration(elapsed_so_far)
			timing_info = f" | elapsed {elapsed_str} | ETA {eta_str}"
		else:
			timing_info = ""
		console.print(f"\n[bold][{i+1}/{len(yaml_files)}][/bold] "
			f"Classifying [cyan]{rel_path}[/cyan]{timing_info}")
		item_start = time.monotonic()

		for run_num in range(num_repeats):
			if num_repeats > 1:
				console.print(f"  run {run_num+1}/{num_repeats}", style="dim")
			try:
				result = classify_one_yaml(
					client, rel_path, repo_root,
					all_indexes, cross_examples, assignments,
					verbose=args.verbose,
				)
			except (RuntimeError, llm.LLMError) as exc:
				console.print(f"  ERROR: {exc}", style="bold red")
				if run_num == 0:
					llm_error_files.append(rel_path)
				continue

			if result is None:
				if run_num == 0:
					extraction_failures.append(rel_path)
				break

			results.append(result)
			repeat_results.setdefault(rel_path, []).append(result)
			common.write_debug_log(result, debug_dir, log_name="yaml_classification_log.jsonl")

			topic_label = result.get("topic_name", result["topic"])
			if num_repeats > 1:
				status_tag = "[green]OK[/green]" if result["status"] == "classified" else "[yellow]??[/yellow]"
				console.print(
					f"    {status_tag} {result['subject']}/{result['topic']} "
					f"[cyan]{topic_label}[/cyan] ({result['confidence_score']})")
			else:
				if result["status"] == "classified":
					console.print(
						f"  [bold green][OK][/bold green] {result['subject']}/{result['topic']} "
						f"[cyan]{topic_label}[/cyan] (score: {result['confidence_score']})")
				else:
					console.print(
						f"  [bold yellow][??][/bold yellow] {result['subject']}/{result['topic']} "
						f"[cyan]{topic_label}[/cyan] (score: {result['confidence_score']})")

		item_elapsed = time.monotonic() - item_start
		console.print(f"  completed in {common.format_duration(item_elapsed)}", style="dim")

	total_elapsed = time.monotonic() - total_start
	console.print(f"\nTotal classification time: [bold]{common.format_duration(total_elapsed)}[/bold]")

	# Deduplicate to first run per yaml for CSV writing
	first_run_results = []
	seen = set()
	for r in results:
		key = r.get("yaml_path") or r["input"]
		if key in seen:
			continue
		seen.add(key)
		first_run_results.append(r)

	console.print(f"\nWriting result CSVs to [cyan]{results_dir}[/cyan]...", style="dim italic")
	written = csv_handler.write_result_csvs(first_run_results, results_dir)
	for f in written:
		console.print(f"  Written: [green]{f}[/green]")

	if extraction_failures:
		path = os.path.join(results_dir, "no_yaml_content.csv")
		with open(path, "w") as f:
			f.write("yaml\n")
			for p in sorted(extraction_failures):
				f.write(f"{p}\n")
		console.print(f"  Written: [green]{path}[/green] "
			f"([bold]{len(extraction_failures)}[/bold] files)")

	if llm_error_files:
		path = os.path.join(results_dir, "llm_errors.csv")
		with open(path, "w") as f:
			f.write("yaml\n")
			for p in sorted(llm_error_files):
				f.write(f"{p}\n")
		console.print(f"  Written: [green]{path}[/green] "
			f"([bold]{len(llm_error_files)}[/bold] files)")

	console.print("\n--- Classification Report ---", style="bold")
	common.print_diff_report(first_run_results)

	if num_repeats > 1 and repeat_results:
		common.print_consistency_report(repeat_results, num_repeats)

#============================================
if __name__ == '__main__':
	main()
