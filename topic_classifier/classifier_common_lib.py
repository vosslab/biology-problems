#!/usr/bin/env python3

"""Shared helpers for classify_scripts.py and classify_yaml.py.

Lifted from classify_scripts.py without behavior changes so both the script
and YAML classifier pipelines can share the LLM plumbing, confidence scoring,
result reporting, and terminal output routines.
"""

# Standard Library
import os
import sys
import json
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

MAX_RESPONSE_LENGTH = 2000

#============================================
def check_response(response: str, required_tags: list = None) -> list:
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
def generate_with_retry(
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
		problems = check_response(response, required_tags)
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
	return best_response

#============================================
def parse_confidence(raw: str) -> int:
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
def compute_confidence_score(
	stage1: dict,
	stage2: dict,
	has_content: bool,
	all_indexes: dict,
) -> int:
	"""Compute a heuristic confidence score (0-4).

	Args:
		stage1: stage 1 classification result
		stage2: stage 2 classification result
		has_content: whether rendered content (bbq or yaml) was available
		all_indexes: subject index data for validation

	Returns:
		integer score 0-4
	"""
	score = 0

	# +1 for content available
	if has_content:
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
def get_topic_name(topics: list, topic_id: str) -> str:
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
def make_failed_result(
	item_path: str,
	execution_status: str,
	stage1: dict,
	stage2: dict = None,
) -> dict:
	"""Create a result dict for a failed classification.

	Args:
		item_path: relative path to script or yaml file
		execution_status: success/failed/cached/skipped
		stage1: stage 1 result dict
		stage2: stage 2 result dict or None

	Returns:
		result dict with status='review'
	"""
	result = {
		"script": item_path,
		"subject": stage1.get("subject", "unknown"),
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
def write_debug_log(result: dict, debug_dir: str, log_name: str = "classification_log.jsonl") -> None:
	"""Append a result to the JSONL debug log for crash recovery.

	Args:
		result: classification result dict
		debug_dir: directory for debug files
		log_name: filename for the JSONL log
	"""
	log_path = os.path.join(debug_dir, log_name)
	with open(log_path, "a") as f:
		f.write(json.dumps(result) + "\n")

#============================================
def _result_subject(r: dict) -> str:
	"""Read subject from a result dict with chapter fallback."""
	value = r.get("subject") or r.get("chapter") or ""
	return value

#============================================
def print_diff_report(results: list) -> None:
	"""Print a diff report comparing results against existing assignments.

	Args:
		results: list of classification result dicts
	"""
	matches = 0
	disagreements = 0
	new_items = 0
	reviews = 0

	for r in results:
		item_name = os.path.basename(r["script"])
		topic_name = r.get("topic_name", "")
		subject = _result_subject(r)
		if topic_name:
			predicted = f"{subject}/{r['topic']} ({topic_name})"
		else:
			predicted = f"{subject}/{r['topic']}"

		if r["status"] == "review":
			console.print(f"[yellow]REVIEW[/yellow]   {item_name} -> {predicted} "
				f"(score: {r['confidence_score']}, exec: {r['execution']})")
			reviews += 1
		elif r["existing"] is None:
			console.print(f"[cyan]NEW[/cyan]      {item_name} -> {predicted}")
			new_items += 1
		elif r["match"]:
			console.print(f"[green]MATCH[/green]    {item_name} -> {predicted}")
			matches += 1
		else:
			console.print(f"[red]DISAGREE[/red] {item_name} -> {predicted} "
				f"(existing: {r['existing']})")
			disagreements += 1

	console.print(f"\nSummary: [green]{matches} matches[/green], "
		f"[cyan]{new_items} new[/cyan], "
		f"[red]{disagreements} disagreements[/red], "
		f"[yellow]{reviews} review[/yellow]")

#============================================
def print_consistency_report(repeat_results: dict, num_repeats: int) -> None:
	"""Print a condensed per-item rollup for repeated classification runs.

	Args:
		repeat_results: dict mapping item_path to list of result dicts
		num_repeats: number of repeats per item
	"""
	console.print(f"\n--- Consistency Report ({num_repeats} runs per item) ---", style="bold")
	stable_count = 0
	flagged_count = 0
	total_items = len(repeat_results)

	for item_path, run_results in sorted(repeat_results.items()):
		item_name = os.path.basename(item_path)

		subject_votes = {}
		topic_votes = {}
		confidences = []
		topic_names = {}
		existing = None
		for r in run_results:
			subj = _result_subject(r)
			subject_votes[subj] = subject_votes.get(subj, 0) + 1
			top = r["topic"]
			topic_votes[top] = topic_votes.get(top, 0) + 1
			confidences.append(r["confidence_score"])
			if r.get("topic_name"):
				topic_names[top] = r["topic_name"]
			if r.get("existing") and existing is None:
				existing = r["existing"]

		top_subject = max(subject_votes, key=subject_votes.get)
		top_subject_count = subject_votes[top_subject]
		top_topic = max(topic_votes, key=topic_votes.get)
		top_topic_count = topic_votes[top_topic]
		top_topic_name = topic_names.get(top_topic, "")

		threshold = (2 * num_repeats + 2) // 3
		subject_stable = top_subject_count >= threshold
		topic_stable = top_topic_count >= threshold
		is_stable = subject_stable and topic_stable

		conf_min = min(confidences)
		conf_max = max(confidences)
		conf_str = f"{conf_min}" if conf_min == conf_max else f"{conf_min}-{conf_max}"

		final_label = f"{top_subject}/{top_topic}"
		if top_topic_name:
			final_label += f" ({top_topic_name})"

		if is_stable:
			stable_count += 1
			tag = "[green]STABLE[/green]  "
		else:
			flagged_count += 1
			tag = "[red]UNSTABLE[/red]"

		console.print(f"  {tag} {item_name}")
		subj_parts = [f"{s}: {c}/{num_repeats}" for s, c in sorted(subject_votes.items(), key=lambda x: -x[1])]
		console.print(f"    subject: {', '.join(subj_parts)}", style="dim")
		topic_parts = []
		for t, c in sorted(topic_votes.items(), key=lambda x: -x[1]):
			tname = topic_names.get(t, "")
			tlabel = f"{t} {tname}" if tname else t
			topic_parts.append(f"{tlabel}: {c}/{num_repeats}")
		console.print(f"    topic:   {', '.join(topic_parts)}", style="dim")
		console.print(f"    final:   [cyan]{final_label}[/cyan]  conf: {conf_str}")
		if existing:
			match_str = "[green]match[/green]" if existing == f"{top_subject}/{top_topic}" else "[red]disagree[/red]"
			console.print(f"    existing: {existing} ({match_str})")

	console.print(
		f"\n  [green]{stable_count}[/green]/{total_items} stable, "
		f"[red]{flagged_count}[/red] flagged")

#============================================
def format_duration(seconds: float) -> str:
	"""Format a duration in seconds to a human-readable string.

	Args:
		seconds: duration in seconds

	Returns:
		formatted string like '12.3s' or '2m 15s'
	"""
	if seconds < 60:
		return f"{seconds:.1f}s"
	minutes = int(seconds) // 60
	secs = int(seconds) % 60
	return f"{minutes}m {secs:02d}s"

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
		response = urllib.request.urlopen(request, timeout=15)  # nosec B310
	except (urllib.error.URLError, TimeoutError):
		raise RuntimeError(
			f"Cannot connect to Ollama at {base_url}\n"
			"Start Ollama first: ollama serve")
	data = json.loads(response.read().decode("utf-8"))
	local_models = [m["name"] for m in data.get("models", [])]
	if model not in local_models:
		installed_str = ", ".join(local_models) if local_models else "none"
		msg = (f"Requested Ollama model not available locally: {model}\n"
			f"Installed models: {installed_str}\n"
			f"Install with: ollama pull {model}\n"
			"Or run with --ollama to use the default RAM-selected model.")
		raise RuntimeError(msg)

#============================================
def create_llm_client(model: str = None, use_ollama: bool = False) -> llm.LLMClient:
	"""Create an LLM client with strict transport selection.

	Args:
		model: exact Ollama model name (requires use_ollama=True)
		use_ollama: if True, use Ollama only; if False, use Apple only

	Returns:
		configured LLMClient
	"""
	if use_ollama:
		ollama_model = model if model else llm.choose_model(None)
		transport = llm.OllamaTransport(model=ollama_model)
	else:
		transport = llm.AppleTransport()
	client = llm.LLMClient(transports=[transport], quiet=True)
	return client
