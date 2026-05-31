"""Load subject and topic metadata from topics_metadata.yml.

Provides load_all_indexes(), format_subject_list(), and format_topic_list()
for use by classifier scripts and prompt builders."""

# Standard Library
import os
import subprocess

# PIP3 modules
import yaml

#============================================
def get_repo_root() -> str:
	"""Return the repository root directory via git rev-parse.

	Returns:
		Absolute path string of the repo root.
	"""
	result = subprocess.run(
		["git", "rev-parse", "--show-toplevel"],
		capture_output=True, text=True, check=True,
	)
	repo_root = result.stdout.strip()
	return repo_root

#============================================
def get_metadata_path() -> str:
	"""Compute the canonical path to topics_metadata.yml in the sibling website repo.

	Returns:
		Absolute path to topics_metadata.yml.

	Raises:
		FileNotFoundError: if the computed path does not exist.
	"""
	repo_root = get_repo_root()
	# topics_metadata.yml lives in the sibling biology-problems-website repo
	parent_dir = os.path.dirname(repo_root)
	metadata_path = os.path.join(parent_dir, "biology-problems-website", "topics_metadata.yml")
	if not os.path.isfile(metadata_path):
		raise FileNotFoundError(
			f"topics_metadata.yml not found at expected path: {metadata_path}\n"
			f"Clone the biology-problems-website repo as a sibling of {repo_root}"
		)
	return metadata_path

#============================================
def load_all_indexes(metadata_path: str = None) -> dict:
	"""Load all subjects and topics from topics_metadata.yml.

	Returns a structure used by classifier scripts and prompt builders.
	The topic_id field is the alias when present, else the topicNN key, so that
	downstream comparison and output use human-readable aliases automatically.

	Args:
		metadata_path: path to topics_metadata.yml. If None, uses get_metadata_path().

	Returns:
		dict mapping subject_key to subject data:
		{
		  subject_key: {
		    "title": <subject title str>,
		    "description": <subject description str>,
		    "topics": [
		      {
		        "topic_id": <alias if present else topicNN>,
		        "name": <topic title>,
		        "description": <topic description>,
		        "alias": <alias str or None>,
		        "topicNN": <topicNN key str>,
		      },
		      ...
		    ],
		  },
		  ...
		}

	Raises:
		FileNotFoundError: if the metadata file is not found.
	"""
	if metadata_path is None:
		metadata_path = get_metadata_path()

	with open(metadata_path, "r") as f:
		raw = yaml.safe_load(f)

	all_indexes = {}
	# Preserve insertion order from the YAML file (Python dict preserves order)
	for subject_key, subject_data in raw.items():
		subject_title = subject_data["title"]
		# Strip trailing whitespace/newlines from block scalar descriptions
		subject_description = subject_data["description"].strip()
		topics_raw = subject_data["topics"]

		topics = []
		for topicNN, topic_data in topics_raw.items():
			# alias is optional per topic
			alias = topic_data.get("alias", None)
			# topic_id is alias when present, else the topicNN key
			topic_id = alias if alias is not None else topicNN
			topic_entry = {
				"topic_id": topic_id,
				"name": topic_data["title"],
				"description": topic_data["description"],
				"alias": alias,
				"topicNN": topicNN,
			}
			topics.append(topic_entry)

		all_indexes[subject_key] = {
			"title": subject_title,
			"description": subject_description,
			"topics": topics,
		}

	return all_indexes

#============================================
def format_subject_list(all_indexes: dict) -> str:
	"""Format all subjects with descriptions and topic names for LLM prompt.

	Lists each subject as ### heading, indented description lines, and
	a comma-joined topic-names line.

	Args:
		all_indexes: output of load_all_indexes()

	Returns:
		Formatted string listing all subjects.
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

	Because topic_id is the alias when present, the model sees aliases.

	Args:
		topics: list of topic dicts from load_all_indexes()[subject]["topics"]

	Returns:
		Formatted string listing all topics with descriptions.
	"""
	lines = []
	for topic in topics:
		line = f"- {topic['topic_id']}: {topic['name']} -- {topic['description']}"
		lines.append(line)
	result = "\n".join(lines)
	return result
