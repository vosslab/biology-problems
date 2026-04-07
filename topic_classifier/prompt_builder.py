"""Build LLM classification prompts for both stages.

Prompt text is stored in topic_classifier/prompts/*.yaml for easy editing.
Rendering logic, variable substitution, and validation stay in Python.
"""

# Standard Library
import os

# PIP3 modules
import yaml

# local repo modules
import topic_classifier.index_parser as index_parser

#============================================
# Load prompt YAML files at module init
_PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "prompts")

def _load_prompt(filename: str) -> dict:
	"""Load a YAML prompt file from the prompts directory.

	Args:
		filename: name of the YAML file (e.g., 'summary.yaml')

	Returns:
		parsed dict from YAML
	"""
	filepath = os.path.join(_PROMPTS_DIR, filename)
	with open(filepath, "r") as f:
		data = yaml.safe_load(f)
	return data

# Cache loaded prompts
_SUMMARY_PROMPT = _load_prompt("summary.yaml")
_STAGE1_PROMPT = _load_prompt("stage1_subject.yaml")
_STAGE2_PROMPT = _load_prompt("stage2_topic.yaml")

#============================================
def build_summary_prompt(script_path: str, bbq_output: str) -> list:
	"""Build chat messages for summarizing question output.

	The summarizer describes biological content only, not script mechanics.

	Args:
		script_path: relative path to the script
		bbq_output: human-readable question text

	Returns:
		list of message dicts for LLMClient.generate(messages=...)
	"""
	user_parts = []
	user_parts.append(f"## Script: {script_path}\n\n")
	user_parts.append(f"### Generated questions\n```\n{bbq_output}\n```\n\n")
	user_parts.append(_SUMMARY_PROMPT["instructions"])
	user_content = "".join(user_parts)

	messages = [
		{"role": "system", "content": _SUMMARY_PROMPT["system"].strip()},
		{"role": "user", "content": user_content},
	]
	return messages

#============================================
def build_stage1_prompt(
	script_path: str,
	source_code: str,
	question_summary: str,
	all_indexes: dict,
	cross_examples: list,
) -> list:
	"""Build chat messages for stage 1 (subject classification).

	Args:
		script_path: relative path to the script
		source_code: full or summarized source code
		question_summary: LLM-generated summary of the questions, or None
		all_indexes: output of index_parser.load_all_indexes()
		cross_examples: output of csv_handler.get_cross_subject_examples()

	Returns:
		list of message dicts for LLMClient.generate(messages=...)
	"""
	# Build the subject list
	subject_list = index_parser.format_subject_list(all_indexes)

	# Build few-shot examples section
	examples_text = _format_cross_examples(cross_examples)

	# Build the user prompt -- question summary is primary, source is fallback
	user_parts = []
	user_parts.append("## Available subjects\n")
	user_parts.append(subject_list)
	user_parts.append("\n\n## Examples of assigned scripts\n")
	user_parts.append(examples_text)
	user_parts.append(f"\n\n## Script to classify: {script_path}\n")

	# Extract subject hint from script path folder name (redundant for copying)
	path_parts = script_path.split("/")
	for part in path_parts:
		if part.endswith("-problems"):
			folder_hint = part.replace("-problems", "").replace("-", "_")
			user_parts.append(f"Script folder: {part}\n")
			user_parts.append(f"Folder subject: {folder_hint}\n")
			break

	if question_summary:
		user_parts.append(f"### Question summary\n{question_summary}\n")
	else:
		# Fallback: use source code only when no summary available
		user_parts.append("### Source code (no question output available)\n```python\n")
		user_parts.append(source_code)
		user_parts.append("\n```\n")

	user_parts.append("\n")
	user_parts.append(_STAGE1_PROMPT["instructions"])

	# Add disambiguation micro-examples if available
	micro_examples = _STAGE1_PROMPT.get("micro_examples", "")
	if micro_examples:
		user_parts.append("\n")
		user_parts.append(micro_examples)

	user_content = "".join(user_parts)

	messages = [
		{"role": "system", "content": _STAGE1_PROMPT["system"].strip()},
		{"role": "user", "content": user_content},
	]
	return messages

#============================================
def build_stage2_prompt(
	script_path: str,
	source_code: str,
	summary_result: dict,
	subject: str,
	topics: list,
	subject_examples: list,
) -> list:
	"""Build chat messages for stage 2 (topic classification within subject).

	Args:
		script_path: relative path to the script
		source_code: full or summarized source code
		summary_result: full summary dict from summarizer stage, or None
		subject: predicted subject from stage 1
		topics: topic list for this subject from index_parser
		subject_examples: few-shot examples from this subject

	Returns:
		list of message dicts for LLMClient.generate(messages=...)
	"""
	# Build the topic list
	topic_list = index_parser.format_topic_list(topics)

	# Build few-shot examples
	examples_text = _format_subject_examples(subject_examples)

	# Build the user prompt
	user_parts = []
	user_parts.append(f"## Available topics for {subject}\n")
	user_parts.append(topic_list)
	user_parts.append("\n\n## Examples of scripts assigned to this subject\n")
	user_parts.append(examples_text)
	user_parts.append(f"\n\n## Script to classify: {script_path}\n")

	if summary_result and summary_result.get("primary_concept"):
		# Present summary fields in ranked order (most discriminating first)
		user_parts.append("### Question analysis\n")
		user_parts.append(f"**Primary concept:** {summary_result['primary_concept']}\n")
		if summary_result.get("key_terms"):
			user_parts.append(f"**Key terms:** {summary_result['key_terms']}\n")
		if summary_result.get("summary"):
			user_parts.append(f"**Summary:** {summary_result['summary']}\n")
	else:
		# Fallback: use source code only
		user_parts.append("### Source code (no question analysis available)\n```python\n")
		user_parts.append(source_code)
		user_parts.append("\n```\n")

	# Add instructions, decision rules, subject-specific rules, and response format
	user_parts.append("\n## Instructions\n")
	user_parts.append(f"This script belongs to the subject '{subject}'. ")
	user_parts.append("Classify it into exactly one topic from the list above.\n\n")
	user_parts.append("## Decision rules\n")
	user_parts.append(_STAGE2_PROMPT["decision_rules"])

	# Add positive examples if available
	examples = _STAGE2_PROMPT.get("examples", "")
	if examples:
		user_parts.append("\n")
		user_parts.append(examples)

	user_parts.append("\n## Response format\n")
	user_parts.append(_STAGE2_PROMPT["response_format"])

	user_content = "".join(user_parts)

	messages = [
		{"role": "system", "content": _STAGE2_PROMPT["system"].strip()},
		{"role": "user", "content": user_content},
	]
	return messages

#============================================
def _format_cross_examples(examples: list) -> str:
	"""Format cross-subject few-shot examples for stage 1.

	Args:
		examples: output of csv_handler.get_cross_subject_examples()

	Returns:
		formatted string
	"""
	lines = []
	for ex in examples:
		line = f"- {ex['script']} -> {ex['chapter']}/{ex['topic']}"
		lines.append(line)
	result = "\n".join(lines)
	return result

#============================================
def _format_subject_examples(examples: list) -> str:
	"""Format subject-specific few-shot examples for stage 2.

	Args:
		examples: output of csv_handler.get_examples_for_subject()

	Returns:
		formatted string
	"""
	lines = []
	for ex in examples:
		line = f"- {ex['script']} -> {ex['topic']}"
		if ex.get("flags"):
			line += f" (flags: {ex['flags']})"
		lines.append(line)
	result = "\n".join(lines)
	return result

#============================================
def summarize_source(source_code: str, max_lines: int = 120) -> str:
	"""Summarize source code if it exceeds max_lines or max_chars.

	For short scripts, returns the full source. For longer scripts,
	extracts key signals: docstring, imports, argparse, key functions.
	The bbq output is the primary classification signal, so source
	is trimmed aggressively to stay within context limits.

	Args:
		source_code: full source code string
		max_lines: threshold for summarization

	Returns:
		source code or summary string
	"""
	lines = source_code.split("\n")
	if len(lines) <= max_lines and len(source_code) <= 4000:
		return source_code

	# Extract key sections for long scripts
	sections = []
	sections.append("# [Source code summarized - original is {} lines]".format(len(lines)))

	# Extract docstring (first triple-quoted block)
	in_docstring = False
	docstring_lines = []
	for line in lines[:30]:
		if '"""' in line or "'''" in line:
			docstring_lines.append(line)
			if in_docstring:
				break
			in_docstring = True
			continue
		if in_docstring:
			docstring_lines.append(line)
	if docstring_lines:
		sections.append("\n".join(docstring_lines))

	# Extract imports
	import_lines = [l for l in lines if l.startswith("import ") or l.startswith("from ")]
	if import_lines:
		sections.append("\n# Imports")
		sections.append("\n".join(import_lines))

	# Extract function signatures and their first docstring line
	for i, line in enumerate(lines):
		stripped = line.strip()
		if stripped.startswith("def "):
			sections.append("\n" + line)
			# Get docstring if present
			if i + 1 < len(lines) and '"""' in lines[i + 1]:
				sections.append(lines[i + 1])

	summary = "\n".join(sections)
	return summary
