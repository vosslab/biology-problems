#!/usr/bin/env python3

"""Validate complete multi-subject assignments in bbq task CSV files."""

# Standard Library
import os
import csv
import glob
import argparse
import collections

# local repo modules
import topic_classifier.metadata_loader_lib as metadata_loader
import topic_classifier.script_runner_lib as script_runner


CSV_COLUMNS = ["subject", "topic", "script", "flags", "input", "notes"]
SINGLE_FILE_ROUTES = {
	"biostatistics": "biostats_tasks.csv",
	"biotechnology": "biotech_tasks.csv",
	"laboratory": "laboratory_tasks.csv",
	"molecular_biology": "molecular_bio_tasks.csv",
	"other": "other_tasks.csv",
}
BIOCHEM_ROUTES = {
	"biochem_tasks1.csv": {
		"biomolecules", "water_ph", "amino_acids", "protein_structure",
		"protein_purification",
	},
	"biochem_tasks2.csv": {
		"thermodynamics", "enzyme_kinetics", "enzyme_inhibition", "allostery",
	},
	"biochem_tasks3.csv": {
		"carbohydrates", "nucleic_acids", "lipids", "membranes", "senses",
		"digestion", "sugar_metabolism", "oxidative_phosphorylation",
		"lipid_metabolism", "glycogen_pentose_phosphate", "photosynthesis",
		"nitrogen_metabolism",
	},
}
GENETICS_ROUTES = {
	"genetics_tasks1.csv": {
		"genetic_disorders", "dna_structure", "dna_profiling", "mendelian",
		"gene_interactions", "chromosomal_inheritance", "chi_square",
	},
	"genetics_tasks2.csv": {
		"gene_mapping", "chromosomal_disorders", "population_genetics",
		"phylogenetics",
	},
}


#============================================
def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments."""
	parser = argparse.ArgumentParser(
		description="Validate multi-subject bbq task CSV assignments.",
	)
	parser.add_argument(
		"-t", "--task-dir", dest="task_dir", required=True,
		help="Directory containing the ten task CSV files.",
	)
	parser.add_argument(
		"-i", "--inventory-output", dest="inventory_output",
		help="Optional CSV path for the frozen generator and YAML inventory.",
	)
	return parser.parse_args()


#============================================
def normalize_input_path(input_file: str) -> str:
	"""Normalize task-file aliases to a repository-relative path."""
	if input_file.startswith("{bp_mcs}/"):
		return "problems/multiple_choice_statements/" + input_file[len("{bp_mcs}/"):]
	if input_file.startswith("{bp_match}/"):
		return "problems/matching_sets/" + input_file[len("{bp_match}/"):]
	if input_file.startswith("{bp_root}/"):
		return "problems/" + input_file[len("{bp_root}/"):]
	return input_file


#============================================
def source_path(row: dict) -> str | None:
	"""Return the canonical source path represented by a task row."""
	script = row["script"]
	if script in {"YMCS", "YMATCH"}:
		return normalize_input_path(row["input"])
	if script.startswith("{bp_root}/"):
		return "problems/" + script[len("{bp_root}/"):]
	return None


#============================================
def expected_task_file(subject: str, topic: str) -> str | None:
	"""Return the one task CSV routed to a subject and chapter."""
	if subject in SINGLE_FILE_ROUTES:
		return SINGLE_FILE_ROUTES[subject]
	if subject == "biochemistry":
		routes = BIOCHEM_ROUTES
	elif subject == "genetics":
		routes = GENETICS_ROUTES
	else:
		return None
	for filename, topics in routes.items():
		if topic in topics:
			return filename
	return None


#============================================
def load_rows(task_dir: str) -> tuple[list, list]:
	"""Load non-empty CSV rows and report schema errors."""
	rows = []
	errors = []
	for csv_path in sorted(glob.glob(os.path.join(task_dir, "*.csv"))):
		filename = os.path.basename(csv_path)
		with open(csv_path, "r", newline="") as handle:
			reader = csv.DictReader(handle)
			if reader.fieldnames != CSV_COLUMNS:
				errors.append(f"{filename}: invalid header {reader.fieldnames}")
				continue
			for line_number, raw_row in enumerate(reader, 2):
				row = {key: (value or "").strip() for key, value in raw_row.items()}
				if not any(row.values()):
					continue
				row["source_csv"] = filename
				row["line_number"] = line_number
				rows.append(row)
	return rows, errors


#============================================
def discover_universe(repo_root: str) -> tuple[set, set]:
	"""Discover generator and YAML sources using the classifier's rules."""
	scripts = set(script_runner.discover_generator_scripts(repo_root))
	mcs_pattern = os.path.join(repo_root, "problems/multiple_choice_statements/*/*.yml")
	match_pattern = os.path.join(repo_root, "problems/matching_sets/*/*.yml")
	yaml_paths = glob.glob(mcs_pattern) + glob.glob(match_pattern)
	yamls = {os.path.relpath(path, repo_root) for path in yaml_paths}
	return scripts, yamls


#============================================
def write_inventory(output_path: str, scripts: set, yamls: set) -> None:
	"""Write the stable source inventory used by coverage validation."""
	with open(output_path, "w", newline="") as handle:
		writer = csv.writer(handle)
		writer.writerow(["source_type", "source"])
		for source in sorted(scripts):
			writer.writerow(["generator", source])
		for source in sorted(yamls):
			writer.writerow(["yaml", source])


#============================================
def validate_rows(rows: list, repo_root: str, all_indexes: dict) -> list:
	"""Validate metadata, routing, identity uniqueness, and source paths."""
	errors = []
	valid_topics = {
		subject: {topic["topic_id"] for topic in data["topics"]}
		for subject, data in all_indexes.items()
	}
	per_subject = collections.defaultdict(list)

	for row in rows:
		location = f"{row['source_csv']}:{row['line_number']}"
		subject = row["subject"]
		topic = row["topic"]
		if subject not in valid_topics:
			errors.append(f"{location}: invalid subject {subject!r}")
			continue
		if topic not in valid_topics[subject]:
			errors.append(f"{location}: invalid chapter {subject}/{topic}")
		expected_file = expected_task_file(subject, topic)
		if expected_file != row["source_csv"]:
			errors.append(
				f"{location}: {subject}/{topic} routes to {expected_file}, "
				f"not {row['source_csv']}"
			)

		canonical_source = source_path(row)
		if canonical_source is None:
			errors.append(f"{location}: unsupported script marker {row['script']!r}")
			continue
		abs_source = os.path.join(repo_root, canonical_source)
		if not os.path.isfile(abs_source):
			errors.append(f"{location}: source does not exist: {canonical_source}")

		variant = (row["script"], row["flags"], row["input"])
		per_subject[variant + (subject,)].append((topic, location))

	for key, assignments in per_subject.items():
		topics = {topic for topic, _location in assignments}
		if len(topics) > 1:
			labels = ", ".join(f"{topic} at {location}" for topic, location in assignments)
			errors.append(
				f"source variant has conflicting chapters in subject {key[-1]}: {labels}"
			)
	return errors


#============================================
def validate_coverage(rows: list, repo_root: str) -> tuple[list, set, set]:
	"""Require every discovered generator and YAML source to be assigned."""
	scripts, yamls = discover_universe(repo_root)
	assigned_scripts = set()
	assigned_yamls = set()
	for row in rows:
		canonical_source = source_path(row)
		if canonical_source in scripts:
			assigned_scripts.add(canonical_source)
		if canonical_source in yamls:
			assigned_yamls.add(canonical_source)
	errors = []
	for path in sorted(scripts - assigned_scripts):
		errors.append(f"unassigned generator: {path}")
	for path in sorted(yamls - assigned_yamls):
		errors.append(f"unassigned YAML: {path}")
	return errors, scripts, yamls


#============================================
def main() -> None:
	"""Validate the requested task directory and print a concise result."""
	args = parse_args()
	repo_root = script_runner.get_repo_root()
	rows, errors = load_rows(args.task_dir)
	all_indexes = metadata_loader.load_all_indexes()
	errors.extend(validate_rows(rows, repo_root, all_indexes))
	coverage_errors, scripts, yamls = validate_coverage(rows, repo_root)
	errors.extend(coverage_errors)
	if args.inventory_output:
		write_inventory(args.inventory_output, scripts, yamls)

	print(f"Rows: {len(rows)}")
	print(f"Generator universe: {len(scripts)}")
	print(f"YAML universe: {len(yamls)}")
	if errors:
		print(f"Validation errors: {len(errors)}")
		for error in errors:
			print(f"ERROR: {error}")
		raise SystemExit(1)
	print("Validation errors: 0")


if __name__ == "__main__":
	main()
