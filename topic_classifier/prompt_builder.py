"""Build LLM classification prompts for both stages."""

# local repo modules
import topic_classifier.index_parser as index_parser

#============================================
STAGE1_SYSTEM = (
	"You are a biology textbook topic classifier. "
	"Given a Python question generator script and its output, "
	"assign it to exactly one subject from the provided list. "
	"Respond using XML tags as shown in the instructions."
)

STAGE2_SYSTEM = (
	"You are a biology textbook topic classifier. "
	"Given a Python question generator script and its output, "
	"assign it to exactly one topic from the provided list. "
	"Respond using XML tags as shown in the instructions."
)

#============================================
def build_stage1_prompt(
	script_path: str,
	source_code: str,
	bbq_output: str,
	all_indexes: dict,
	cross_examples: list,
) -> list:
	"""Build chat messages for stage 1 (subject classification).

	Args:
		script_path: relative path to the script
		source_code: full or summarized source code
		bbq_output: sample output from running the script, or None
		all_indexes: output of index_parser.load_all_indexes()
		cross_examples: output of csv_handler.get_cross_subject_examples()

	Returns:
		list of message dicts for LLMClient.generate(messages=...)
	"""
	# Build the subject list
	subject_list = index_parser.format_subject_list(all_indexes)

	# Build few-shot examples section
	examples_text = _format_cross_examples(cross_examples)

	# Build the user prompt
	user_parts = []
	user_parts.append("## Available subjects\n")
	user_parts.append(subject_list)
	user_parts.append("\n\n## Examples of assigned scripts\n")
	user_parts.append(examples_text)
	user_parts.append(f"\n\n## Script to classify: {script_path}\n")
	user_parts.append("### Source code\n```python\n")
	user_parts.append(source_code)
	user_parts.append("\n```\n")

	if bbq_output is not None:
		user_parts.append("### Sample output\n```\n")
		user_parts.append(bbq_output)
		user_parts.append("\n```\n")

	user_parts.append(_stage1_instructions())

	user_content = "".join(user_parts)

	messages = [
		{"role": "system", "content": STAGE1_SYSTEM},
		{"role": "user", "content": user_content},
	]
	return messages

#============================================
def build_stage2_prompt(
	script_path: str,
	source_code: str,
	bbq_output: str,
	subject: str,
	topics: list,
	subject_examples: list,
) -> list:
	"""Build chat messages for stage 2 (topic classification within subject).

	Args:
		script_path: relative path to the script
		source_code: full or summarized source code
		bbq_output: sample output or None
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
	user_parts.append("### Source code\n```python\n")
	user_parts.append(source_code)
	user_parts.append("\n```\n")

	if bbq_output is not None:
		user_parts.append("### Sample output\n```\n")
		user_parts.append(bbq_output)
		user_parts.append("\n```\n")

	user_parts.append(_stage2_instructions(subject))

	user_content = "".join(user_parts)

	messages = [
		{"role": "system", "content": STAGE2_SYSTEM},
		{"role": "user", "content": user_content},
	]
	return messages

#============================================
def _stage1_instructions() -> str:
	"""Return the XML response instructions for stage 1."""
	text = (
		"\n## Instructions\n"
		"Classify this script into exactly one subject. "
		"Respond with these XML tags:\n"
		"<subject>subject_name</subject>\n"
		"<confidence>high</confidence>\n"
		"<reasoning>Brief explanation of why this subject fits.</reasoning>\n\n"
		"For confidence, use exactly one of: high, medium, or low.\n"
	)
	return text

#============================================
def _stage2_instructions(subject: str) -> str:
	"""Return the XML response instructions for stage 2."""
	text = (
		"\n## Instructions\n"
		f"This script belongs to the subject '{subject}'. "
		"Now classify it into exactly one topic from the list above. "
		"Respond with these XML tags:\n"
		"<topic>topicNN</topic>\n"
		"<confidence>high</confidence>\n"
		"<reasoning>Brief explanation of why this topic fits.</reasoning>\n\n"
		"For confidence, use exactly one of: high, medium, or low.\n"
	)
	return text

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
def summarize_source(source_code: str, max_lines: int = 200) -> str:
	"""Summarize source code if it exceeds max_lines.

	For short scripts, returns the full source. For longer scripts,
	extracts key signals: docstring, imports, argparse, key functions.

	Args:
		source_code: full source code string
		max_lines: threshold for summarization

	Returns:
		source code or summary string
	"""
	lines = source_code.split("\n")
	if len(lines) <= max_lines:
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
