"""Build LLM classification prompts for both stages.

Prompt text is stored in topic_classifier/prompts/*.yaml for easy editing.
Rendering logic, variable substitution, and validation stay in Python.
"""

# Standard Library
import os

# PIP3 modules
import yaml

# local repo modules
import topic_classifier.index_parser_lib as index_parser

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
_STAGE1_PROMPT = _load_prompt("stage1_subject.yaml")
_STAGE2_PROMPT = _load_prompt("stage2_topic.yaml")

#============================================
def build_stage1_prompt(
	script_path: str,
	source_code: str,
	all_indexes: dict,
	cross_examples: list,
	bbq_output: str = None,
) -> list:
	"""Build chat messages for stage 1 (subject classification).

	Args:
		script_path: relative path to the script
		source_code: full or summarized source code
		all_indexes: output of index_parser.load_all_indexes()
		cross_examples: output of csv_handler.get_cross_subject_examples()
		bbq_output: cleaned question text from the script, or None

	Returns:
		list of message dicts for LLMClient.generate(messages=...)
	"""
	# Build the subject list
	subject_list = index_parser.format_subject_list(all_indexes)

	# Build few-shot examples section
	examples_text = _format_cross_examples(cross_examples)

	# Build the user prompt -- question text is primary, source is fallback
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

	# Include actual question text when available
	if bbq_output:
		user_parts.append(f"### Generated questions\n```\n{bbq_output}\n```\n")
	else:
		# Fallback: use source code only when no question output available
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
	subject: str,
	topics: list,
	subject_examples: list,
	bbq_output: str = None,
) -> list:
	"""Build chat messages for stage 2 (topic classification within subject).

	Args:
		script_path: relative path to the script
		source_code: full or summarized source code
		subject: predicted subject from stage 1
		topics: topic list for this subject from index_parser
		subject_examples: few-shot examples from this subject
		bbq_output: cleaned question text from the script, or None

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

	# Extract subfolder path hint for stage 2 (e.g., PUBCHEM/AMINO_ACIDS -> amino acids)
	path_parts = script_path.split("/")
	# Find parts after the *-problems folder and before the filename
	problems_idx = None
	for idx, part in enumerate(path_parts):
		if part.endswith("-problems"):
			problems_idx = idx
			break
	if problems_idx is not None and len(path_parts) > problems_idx + 2:
		# There are subdirectories between the subject folder and the script
		subfolders = path_parts[problems_idx + 1:-1]
		if subfolders:
			subfolder_hint = "/".join(subfolders).replace("_", " ").lower()
			user_parts.append(f"Script subfolder: {subfolder_hint}\n")

	# Include actual question text when available
	if bbq_output:
		user_parts.append(f"### Generated questions\n```\n{bbq_output}\n```\n")
	else:
		# Fallback: use source code only
		user_parts.append("### Source code (no question output available)\n```python\n")
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
def build_stage1_yaml_prompt(
	yaml_path: str,
	content: str,
	all_indexes: dict,
	cross_examples: list,
) -> list:
	"""Build chat messages for stage 1 (subject classification) on a YAML file.

	Args:
		yaml_path: relative path to the yaml file
		content: rendered text extracted from the yaml (statements, pairs, ...)
		all_indexes: output of index_parser.load_all_indexes()
		cross_examples: output of csv_handler.get_cross_subject_examples()

	Returns:
		list of message dicts for LLMClient.generate(messages=...)
	"""
	subject_list = index_parser.format_subject_list(all_indexes)
	examples_text = _format_cross_examples(cross_examples)

	user_parts = []
	user_parts.append("## Available subjects\n")
	user_parts.append(subject_list)
	user_parts.append("\n\n## Examples of assigned items\n")
	user_parts.append(examples_text)
	user_parts.append(f"\n\n## YAML file to classify: {yaml_path}\n")

	# Folder hint: multiple_choice_statements/<folder>/file.yml or
	# matching_sets/<folder>/file.yml
	folder_hint = _yaml_folder_hint(yaml_path)
	if folder_hint:
		user_parts.append(f"Current folder: {folder_hint}\n")

	user_parts.append(f"### YAML content\n```\n{content}\n```\n")
	user_parts.append("\n")
	user_parts.append(_STAGE1_PROMPT["instructions"])

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
def build_stage2_yaml_prompt(
	yaml_path: str,
	content: str,
	subject: str,
	topics: list,
	subject_examples: list,
) -> list:
	"""Build chat messages for stage 2 (topic classification) on a YAML file.

	Args:
		yaml_path: relative path to the yaml file
		content: rendered text extracted from the yaml
		subject: predicted subject from stage 1
		topics: topic list for this subject from index_parser
		subject_examples: few-shot examples from this subject

	Returns:
		list of message dicts for LLMClient.generate(messages=...)
	"""
	topic_list = index_parser.format_topic_list(topics)
	examples_text = _format_subject_examples(subject_examples)

	user_parts = []
	user_parts.append(f"## Available topics for {subject}\n")
	user_parts.append(topic_list)
	user_parts.append("\n\n## Examples of items assigned to this subject\n")
	user_parts.append(examples_text)
	user_parts.append(f"\n\n## YAML file to classify: {yaml_path}\n")

	folder_hint = _yaml_folder_hint(yaml_path)
	if folder_hint:
		user_parts.append(f"Current folder: {folder_hint}\n")

	user_parts.append(f"### YAML content\n```\n{content}\n```\n")

	user_parts.append("\n## Instructions\n")
	user_parts.append(f"This content belongs to the subject '{subject}'. ")
	user_parts.append("Classify it into exactly one topic from the list above.\n\n")
	user_parts.append("## Decision rules\n")
	user_parts.append(_STAGE2_PROMPT["decision_rules"])

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
def _yaml_folder_hint(yaml_path: str) -> str:
	"""Extract the subject-hint folder name from a yaml path.

	For paths like 'problems/multiple_choice_statements/biochemistry/x.yml' or
	'problems/matching_sets/inheritance/y.yml' return the middle folder name.

	Args:
		yaml_path: relative path to yaml file

	Returns:
		folder name string, or empty string if path shape is unexpected
	"""
	parts = yaml_path.split("/")
	# Expect: problems / (multiple_choice_statements|matching_sets) / <subject> / file.yml
	for idx, part in enumerate(parts):
		if part in ("multiple_choice_statements", "matching_sets"):
			if idx + 1 < len(parts) - 1:
				return parts[idx + 1]
	return ""

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
