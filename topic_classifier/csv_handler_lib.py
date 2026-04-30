"""Read existing bbq_control CSVs and write bbq_control-format result CSVs."""

# Standard Library
import os
import csv
import glob

#============================================
def read_existing_assignments(csv_dir: str) -> dict:
	"""Read all bbq_control CSV files into a unified assignments dict.

	Args:
		csv_dir: path to bbq_control/ directory containing task CSVs

	Returns:
		dict mapping script path (with {bp_root} prefix) to dict with keys:
		chapter, topic, flags, input, notes
	"""
	assignments = {}
	csv_pattern = os.path.join(csv_dir, "*.csv")
	for csv_path in sorted(glob.glob(csv_pattern)):
		file_assignments = _read_single_csv(csv_path)
		assignments.update(file_assignments)
	return assignments

#============================================
def _read_single_csv(csv_path: str) -> dict:
	"""Read a single bbq_control CSV file.

	Args:
		csv_path: path to a single CSV file

	Returns:
		dict mapping script path to assignment dict
	"""
	assignments = {}
	with open(csv_path, "r") as f:
		reader = csv.reader(f)
		header = next(reader)
		# Strip whitespace from header
		header = [col.strip() for col in header]
		# Accept both the new 'subject' header and the legacy 'chapter' header
		expected_subject = ["subject", "topic", "script", "flags", "input", "notes"]
		expected_chapter = ["chapter", "topic", "script", "flags", "input", "notes"]
		if header != expected_subject and header != expected_chapter:
			print(f"WARNING: unexpected header in {csv_path}: {header}")
			return assignments

		for row in reader:
			# Skip empty rows
			if not row or all(cell.strip() == "" for cell in row):
				continue
			# Pad short rows
			while len(row) < 6:
				row.append("")
			subject = row[0].strip()
			topic = row[1].strip()
			script = row[2].strip()
			flags = row[3].strip()
			input_file = row[4].strip()
			notes = row[5].strip()

			# Skip special entries like YMATCH
			if not script.startswith("{bp_root}"):
				continue

			# Store under both keys so legacy callers reading 'chapter' keep
			# working alongside new callers reading 'subject'.
			entry = {
				"subject": subject,
				"chapter": subject,
				"topic": topic,
				"flags": flags,
				"input": input_file,
				"notes": notes,
			}
			# Use script+flags as key to handle same script with different flags
			key = f"{script}|{flags}"
			assignments[key] = entry
	return assignments

#============================================
def get_script_path_from_key(key: str) -> str:
	"""Extract script path from an assignment key.

	Args:
		key: assignment key in format 'script_path|flags'

	Returns:
		script path portion
	"""
	script_path = key.split("|")[0]
	return script_path

#============================================
def get_variants_for_script(assignments: dict, script_path: str) -> list:
	"""Enumerate (flags, input) variants assigned to a script in the CSVs.

	Args:
		assignments: output of read_existing_assignments()
		script_path: relative path under problems/ (e.g.
			'problems/biochemistry-problems/carbs/classify_Haworth.py')

	Returns:
		list of dicts with 'flags' and 'input' keys. If the script has no
		matching CSV rows, returns a single empty variant so callers always
		have at least one work unit.
	"""
	# Convert the relative path into the {bp_root}/... form used as the
	# script portion of assignment keys
	bp_root_path = "{bp_root}/" + script_path.replace("problems/", "", 1)
	variants = []
	for key, entry in assignments.items():
		entry_script = get_script_path_from_key(key)
		if entry_script != bp_root_path:
			continue
		variant = {
			"flags": entry["flags"],
			"input": entry["input"],
		}
		variants.append(variant)
	if not variants:
		variants = [{"flags": "", "input": ""}]
	return variants

#============================================
def get_examples_for_subject(assignments: dict, subject: str, limit: int = 5) -> list:
	"""Get few-shot examples for a given subject from existing assignments.

	Args:
		assignments: output of read_existing_assignments()
		subject: subject name to filter by (e.g. 'biochemistry')
		limit: max number of examples to return

	Returns:
		list of dicts with script, topic, flags keys
	"""
	examples = []
	for key, entry in assignments.items():
		# 'subject' is the new canonical key; 'chapter' is kept as a fallback
		# for any legacy callers that still write it
		if (entry.get("subject") or entry.get("chapter")) != subject:
			continue
		script_path = get_script_path_from_key(key)
		example = {
			"script": script_path,
			"topic": entry["topic"],
			"flags": entry["flags"],
		}
		examples.append(example)
		if len(examples) >= limit:
			break
	return examples

#============================================
def get_cross_subject_examples(assignments: dict, limit: int = 5) -> list:
	"""Get few-shot examples across all subjects for stage 1 classification.

	Picks one example per subject to avoid bias.

	Args:
		assignments: output of read_existing_assignments()
		limit: max total examples

	Returns:
		list of dicts with script, chapter, topic keys
	"""
	# Collect one example per subject
	seen_subjects = set()
	examples = []
	for key, entry in assignments.items():
		subject = entry.get("subject") or entry.get("chapter")
		if subject in seen_subjects:
			continue
		seen_subjects.add(subject)
		script_path = get_script_path_from_key(key)
		example = {
			"script": script_path,
			"chapter": subject,
			"topic": entry["topic"],
		}
		examples.append(example)
		if len(examples) >= limit:
			break
	return examples

#============================================
def write_result_csvs(results: list, output_dir: str) -> list:
	"""Write classification results as per-subject CSV files.

	All results are collected first, then written in one pass per subject.

	Args:
		results: list of dicts with keys: script, chapter, topic, flags, input, notes, status
		output_dir: directory to write CSV files into

	Returns:
		list of written file paths
	"""
	os.makedirs(output_dir, exist_ok=True)

	# Group results by subject
	by_subject = {}
	for result in results:
		# Only write classified results, not review-flagged
		if result.get("status") != "classified":
			continue
		# Accept either new 'subject' key or legacy 'chapter' key
		subject = result.get("subject") or result.get("chapter")
		if subject not in by_subject:
			by_subject[subject] = []
		by_subject[subject].append(result)

	written_files = []
	for subject, entries in sorted(by_subject.items()):
		# Sort entries by topic for readability
		entries.sort(key=lambda e: e["topic"])
		filename = f"{subject}_tasks.csv"
		filepath = os.path.join(output_dir, filename)
		_write_single_csv(filepath, entries)
		written_files.append(filepath)

	return written_files

#============================================
def _write_single_csv(filepath: str, entries: list) -> None:
	"""Write a single bbq_control-format CSV file.

	Args:
		filepath: output file path
		entries: list of result dicts
	"""
	with open(filepath, "w", newline="") as f:
		writer = csv.writer(f)
		writer.writerow(["subject", "topic", "script", "flags", "input", "notes"])
		for entry in entries:
			subject = entry.get("subject") or entry.get("chapter", "")
			writer.writerow([
				subject,
				entry["topic"],
				entry.get("script", ""),
				entry.get("flags", ""),
				entry.get("input", ""),
				entry.get("notes", ""),
			])

#============================================
if __name__ == '__main__':
	# Quick test: read existing assignments
	csv_dir = "/Users/vosslab/nsh/PROBLEMS/biology-problems-website/bbq_control"
	assignments = read_existing_assignments(csv_dir)
	print(f"Loaded {len(assignments)} assignments from {csv_dir}")

	# Show subject distribution
	subjects = {}
	for key, entry in assignments.items():
		subject = entry.get("subject") or entry.get("chapter")
		subjects[subject] = subjects.get(subject, 0) + 1
	for subject, count in sorted(subjects.items()):
		print(f"  {subject}: {count} scripts")

	# Show cross-subject examples
	print("\nCross-subject examples:")
	examples = get_cross_subject_examples(assignments)
	for ex in examples:
		print(f"  {ex['chapter']}/{ex['topic']}: {ex['script']}")
