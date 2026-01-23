#!/usr/bin/env python3

"""
Add dbsubject field to YAML files based on their folder location.
"""

# Standard Library
import argparse
import pathlib
import sys

# PIP3 modules
import yaml

#============================================

# Mapping of folder names to dbsubject values
FOLDER_TO_DBSUBJECT = {
	'biochemistry': 'Biochemistry',
	'biostatistics': 'Biostatistics',
	'biotechnology': 'Biotechnology',
	'cell_biology': 'Cell Biology',
	'dna_profiling': 'DNA Profiling',
	'inheritance': 'Genetics',
	'laboratory': 'Laboratory Techniques',
	'molecular_biology': 'Molecular Biology',
}

#============================================

def parse_args():
	"""
	Parse command-line arguments.
	"""
	parser = argparse.ArgumentParser(
		description="Add dbsubject field to YAML files based on folder location."
	)
	parser.add_argument(
		'-d', '--directory', dest='directory', required=True,
		help='Directory to scan for YAML files'
	)
	parser.add_argument(
		'-n', '--dry-run', dest='dry_run', action='store_true',
		help='Show what would be changed without writing files'
	)
	args = parser.parse_args()
	return args

#============================================

def get_dbsubject_from_path(yaml_path: pathlib.Path) -> str:
	"""
	Determine dbsubject based on file path.

	Args:
		yaml_path: Path to the YAML file.

	Returns:
		The dbsubject string, or empty string if not determined.
	"""
	parts = yaml_path.parts
	for part in parts:
		if part in FOLDER_TO_DBSUBJECT:
			return FOLDER_TO_DBSUBJECT[part]
	return ''

#============================================

def update_yaml_file(yaml_path: pathlib.Path, dry_run: bool) -> bool:
	"""
	Update a single YAML file with dbsubject.

	Args:
		yaml_path: Path to the YAML file.
		dry_run: If True, only show what would change.

	Returns:
		True if the file was updated (or would be updated in dry-run).
	"""
	# Determine dbsubject
	dbsubject = get_dbsubject_from_path(yaml_path)
	if not dbsubject:
		print(f"Warning: Could not determine dbsubject for {yaml_path}")
		return False

	# Read YAML file
	try:
		with open(yaml_path, 'r', encoding='utf-8') as f:
			content = f.read()
		yaml_data = yaml.safe_load(content)
	except Exception as e:
		print(f"Error reading {yaml_path}: {e}", file=sys.stderr)
		return False

	if yaml_data is None:
		yaml_data = {}

	# Check if dbsubject already exists
	existing_dbsubject = yaml_data.get('dbsubject') or yaml_data.get('DBsubject')
	if existing_dbsubject:
		if existing_dbsubject == dbsubject:
			print(f"Skip: {yaml_path} (already has correct dbsubject)")
			return False
		else:
			print(f"Update: {yaml_path}")
			print(f"  Old dbsubject: {existing_dbsubject}")
			print(f"  New dbsubject: {dbsubject}")
	else:
		print(f"Add: {yaml_path}")
		print(f"  dbsubject: {dbsubject}")

	if dry_run:
		return True

	# Add dbsubject to the YAML data
	yaml_data['dbsubject'] = dbsubject

	# Write back to file
	try:
		with open(yaml_path, 'w', encoding='utf-8') as f:
			yaml.safe_dump(
				yaml_data,
				f,
				default_flow_style=False,
				allow_unicode=True,
				sort_keys=False,
			)
		return True
	except Exception as e:
		print(f"Error writing {yaml_path}: {e}", file=sys.stderr)
		return False

#============================================

def main():
	"""
	Script entrypoint.
	"""
	args = parse_args()
	directory = pathlib.Path(args.directory)

	if not directory.exists():
		print(f"Error: Directory not found: {directory}", file=sys.stderr)
		sys.exit(1)

	if not directory.is_dir():
		print(f"Error: Not a directory: {directory}", file=sys.stderr)
		sys.exit(1)

	# Find all YAML files
	yaml_files = list(directory.rglob('*.yml'))
	if not yaml_files:
		print(f"No YAML files found in {directory}")
		return

	print(f"Found {len(yaml_files)} YAML files in {directory}")
	if args.dry_run:
		print("DRY RUN MODE - no files will be modified")
	print()

	# Update each file
	updated_count = 0
	for yaml_path in sorted(yaml_files):
		if yaml_path.name == 'TEMPLATE.yml':
			print(f"Skip: {yaml_path} (template file)")
			continue
		if update_yaml_file(yaml_path, args.dry_run):
			updated_count += 1

	print()
	if args.dry_run:
		print(f"Would update {updated_count} files")
	else:
		print(f"Updated {updated_count} files")

#============================================

if __name__ == '__main__':
	main()
