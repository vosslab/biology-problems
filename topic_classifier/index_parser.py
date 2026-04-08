"""Parse subject-indexes/*.md files into structured topic lists."""

# Standard Library
import os
import re
import subprocess

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
def parse_subject_description(filepath: str) -> str:
	"""Extract the subject description from the intro section of an index file.

	The description is the text between the title (# heading) and the
	first ## heading. This contains contrastive scope/focus/not lines.

	Args:
		filepath: path to the index markdown file

	Returns:
		description string (may be empty)
	"""
	with open(filepath, "r") as f:
		content = f.read()
	# Extract text between first # heading and first ## heading
	lines = content.split("\n")
	intro_lines = []
	past_title = False
	for line in lines:
		if line.startswith("# ") and not past_title:
			past_title = True
			continue
		if line.startswith("## "):
			break
		if past_title and line.strip():
			intro_lines.append(line.strip())
	description = "\n".join(intro_lines)
	return description

#============================================
def parse_index_file(filepath: str) -> list:
	"""Parse a single subject index markdown file into topic entries.

	Args:
		filepath: path to the index markdown file

	Returns:
		list of dicts with keys: topic_id, name, description
	"""
	with open(filepath, "r") as f:
		content = f.read()

	topics = []
	# Match lines like: 1. [Life Molecules](topic01/index.md) ...
	#     - Description text here.
	# Pattern captures: number, topic name, topic folder, and description on next line
	topic_pattern = re.compile(
		r'^\d+\.\s+\[([^\]]+)\]\((topic\d+)/index\.md\)',
		re.MULTILINE,
	)
	# Description follows on the next line starting with whitespace and dash
	desc_pattern = re.compile(
		r'^\s+-\s+(.+)$',
		re.MULTILINE,
	)

	lines = content.split('\n')
	for i, line in enumerate(lines):
		topic_match = topic_pattern.match(line)
		if topic_match is None:
			continue
		topic_name = topic_match.group(1)
		topic_id = topic_match.group(2)

		# Look for description on the next line
		description = ""
		if i + 1 < len(lines):
			desc_match = desc_pattern.match(lines[i + 1])
			if desc_match is not None:
				description = desc_match.group(1).strip()

		entry = {
			"topic_id": topic_id,
			"name": topic_name,
			"description": description,
		}
		topics.append(entry)

	return topics

#============================================
def derive_subject_from_filename(filename: str) -> str:
	"""Derive subject name from an index filename.

	Args:
		filename: e.g. 'biochemistry-index.md' or 'genetics-index.md'

	Returns:
		subject name, e.g. 'biochemistry' or 'genetics'
	"""
	# Strip '-index.md' suffix to get subject name directly
	subject = filename.replace("-index.md", "")
	return subject

#============================================
def load_all_indexes(index_dir: str = None) -> dict:
	"""Load all subject index files into a structured dict.

	Args:
		index_dir: path to subject-indexes/ directory.
			If None, uses <repo_root>/subject-indexes/

	Returns:
		dict mapping subject name to list of topic dicts
		e.g. {"biochemistry": [{"topic_id": "topic01", "name": "Life Molecules", ...}, ...]}
	"""
	if index_dir is None:
		repo_root = get_repo_root()
		index_dir = os.path.join(repo_root, "subject-indexes")

	all_indexes = {}
	for filename in sorted(os.listdir(index_dir)):
		if not filename.endswith("-index.md"):
			continue
		filepath = os.path.join(index_dir, filename)
		# Resolve symlinks
		filepath = os.path.realpath(filepath)
		if not os.path.isfile(filepath):
			continue

		subject = derive_subject_from_filename(filename)
		topics = parse_index_file(filepath)
		description = parse_subject_description(filepath)
		all_indexes[subject] = {
			"topics": topics,
			"description": description,
		}

	return all_indexes

#============================================
def format_subject_list(all_indexes: dict) -> str:
	"""Format all subjects with contrastive definitions for LLM prompt.

	Each subject gets its intro description (scope/focus/not lines)
	plus all topic names. Descriptions are read from the index files
	so adding a new subject only requires editing one file.

	Args:
		all_indexes: output of load_all_indexes()

	Returns:
		formatted string listing all subjects
	"""
	lines = []
	for subject, data in sorted(all_indexes.items()):
		topics = data["topics"]
		description = data["description"]
		topic_names = [t["name"] for t in topics]
		topic_list = ", ".join(topic_names)
		lines.append(f"### {subject}")
		if description:
			# Indent each line of the description
			for desc_line in description.split("\n"):
				lines.append(f"  {desc_line}")
		lines.append(f"  Topics: {topic_list}")
		lines.append("")
	result = "\n".join(lines)
	return result

#============================================
def format_topic_list(topics: list) -> str:
	"""Format topics for a single subject for LLM prompt.

	Args:
		topics: list of topic dicts from load_all_indexes()[subject]

	Returns:
		formatted string listing all topics with descriptions
	"""
	lines = []
	for topic in topics:
		line = f"- {topic['topic_id']}: {topic['name']} -- {topic['description']}"
		lines.append(line)
	result = "\n".join(lines)
	return result

#============================================
if __name__ == '__main__':
	# Quick test: load and print all indexes
	all_indexes = load_all_indexes()
	for subject, data in sorted(all_indexes.items()):
		topics = data["topics"]
		print(f"\n{subject} ({len(topics)} topics):")
		for t in topics:
			print(f"  {t['topic_id']}: {t['name']}")
	print("\n--- Subject list for LLM ---")
	print(format_subject_list(all_indexes))
