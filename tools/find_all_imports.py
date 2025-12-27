import os
import ast
import sys
import pkgutil
import warnings
import importlib_metadata

# Suppress SyntaxWarnings for old regex patterns
warnings.filterwarnings("ignore", category=SyntaxWarning)

def extract_imports_from_file(filepath):
	"""
	Extracts top-level import names from a Python file.
	"""
	with open(filepath, "r", encoding="utf-8") as file:
		try:
			tree = ast.parse(file.read(), filename=filepath)
		except (SyntaxError, UnicodeDecodeError):
			return set()

	imports = set()
	for node in ast.walk(tree):
		if isinstance(node, ast.Import):
			for alias in node.names:
				imports.add(alias.name.split(".")[0])  # Only top-level package
		elif isinstance(node, ast.ImportFrom):
			if node.module:
				imports.add(node.module.split(".")[0])  # Only top-level package

	return imports

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

def map_import_to_pypi(import_name):
	"""
	Attempts to find the official PyPI package name for a given import.
	1. Checks installed packages using `importlib_metadata`.
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
		dist = importlib_metadata.distribution(import_name)
		return dist.metadata["Name"]  # Use the official PyPI package name
	except importlib_metadata.PackageNotFoundError:
		# If not found, check fallback dictionary
		return FALLBACK_PYPI_MAPPING.get(import_name, import_name)  # Default to import name

def find_all_imports(directory="."):
	"""
	Finds all third-party packages used in Python scripts within the given directory.
	Excludes built-in modules and local project files.
	Generates a `requirements.txt` file.
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

	# Write the final list to `requirements.txt`
	with open("requirements.txt", "w") as f:
		for package in pypi_packages:
			f.write(f"{package}\n")

	print("✅ Generated `requirements.txt` successfully! (Filtered built-ins & local modules)")

if __name__ == "__main__":
	find_all_imports()
