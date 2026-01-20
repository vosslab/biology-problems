#!/usr/bin/env python3

import argparse
import ast
import importlib.metadata
import os
import sys
import warnings

# Suppress SyntaxWarnings for old regex patterns
warnings.filterwarnings("ignore", category=SyntaxWarning)

#============================================
def parse_args():
	"""
	Parse command-line arguments.
	"""
	parser = argparse.ArgumentParser(
		description="Find third-party imports and write a pip_requirements.txt file."
	)
	parser.add_argument(
		'-d', '--directory', dest='directory',
		default='.',
		help="Directory to scan for Python files."
	)
	parser.add_argument(
		'-o', '--output', dest='output_file',
		default='pip_requirements.txt',
		help="Output requirements filename."
	)
	args = parser.parse_args()
	return args

#============================================
def extract_imports_from_file(filepath):
	"""
	Extracts top-level import names from a Python file.
	"""
	with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
		source = file.read()
	try:
		tree = ast.parse(source, filename=filepath)
	except SyntaxError:
		return set()

	imports = set()
	for node in ast.walk(tree):
		if isinstance(node, ast.Import):
			for alias in node.names:
				# Only keep the top-level package name.
				imports.add(alias.name.split(".")[0])
		elif isinstance(node, ast.ImportFrom):
			if node.module:
				# Only keep the top-level package name.
				imports.add(node.module.split(".")[0])

	return imports

#============================================
def get_local_modules(directory="."):
	"""
	Finds all local Python modules/packages in the project directory.
	Returns a set of module names to exclude from the final requirements.
	"""
	local_modules = set()
	for root, dirs, files in os.walk(directory):
		# Add folders containing __init__.py (Python packages)
		for d in dirs:
			if os.path.isfile(os.path.join(root, d, "__init__.py")):
				local_modules.add(d)
		# Add standalone Python files
		for file in files:
			if file.endswith(".py"):
				module_name = os.path.splitext(file)[0]  # Remove .py extension
				local_modules.add(module_name)

	return local_modules

#============================================
def map_import_to_pypi(import_name):
	"""
	Attempts to find the official PyPI package name for a given import.
	1. Checks installed packages using `importlib.metadata`.
	2. Falls back to a manual mapping for known exceptions.
	3. Returns the original name if no mapping is found.
	"""
	# Known special cases
	FALLBACK_PYPI_MAPPING = {
		"bs4": "beautifulsoup4",
		"yaml": "pyyaml",
		"PIL": "pillow",
		"Bio": "biopython",
	}

	# Check if import is a standard PyPI package
	try:
		dist = importlib.metadata.distribution(import_name)
		return dist.metadata["Name"]  # Use the official PyPI package name
	except importlib.metadata.PackageNotFoundError:
		# If not found, check fallback dictionary
		return FALLBACK_PYPI_MAPPING.get(import_name, import_name)  # Default to import name

#============================================
def find_all_imports(directory=".", output_file="pip_requirements.txt"):
	"""
	Finds all third-party packages used in Python scripts within the given directory.
	Excludes built-in modules and local project files.
	Generates a pip requirements file.
	"""
	import_statements = set()
	for root, _, files in os.walk(directory):
		for file in files:
			if file.endswith(".py"):
				filepath = os.path.join(root, file)
				import_statements.update(extract_imports_from_file(filepath))

	# Get built-in Python standard modules
	stdlib_modules = set(sys.stdlib_module_names)

	# Get local project modules (both standalone `.py` and package folders)
	local_modules = get_local_modules(directory)

	# Filter imports: Remove built-in modules & local modules
	third_party_imports = sorted(import_statements - stdlib_modules - local_modules)

	# Convert import names to PyPI package names
	pypi_packages = sorted(set(map_import_to_pypi(pkg) for pkg in third_party_imports))

	# Write the final list to the output file.
	with open(output_file, "w", encoding="utf-8") as file:
		for package in pypi_packages:
			file.write(f"{package}\n")

	print(f"Generated {output_file} successfully! (Filtered built-ins & local modules)")

#============================================
def main():
	"""
	Run the import scan and write the requirements file.
	"""
	args = parse_args()
	find_all_imports(directory=args.directory, output_file=args.output_file)

if __name__ == "__main__":
	main()
