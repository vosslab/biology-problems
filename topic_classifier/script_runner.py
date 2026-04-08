"""Discover generator scripts, run them, detect bbq output files, cache results."""

# Standard Library
import os
import glob
import shutil
import subprocess

# qti-package-maker modules (on PYTHONPATH via source_me.sh)
import qti_package_maker.package_interface as package_interface

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
def discover_generator_scripts(repo_root: str = None) -> list:
	"""Find all generator scripts under problems/*-problems/.

	Filters for Python files that:
	- Are under problems/*-problems/
	- Contain 'if __name__' main block
	- Import bptools or have question-generation patterns
	- Are not __init__.py or test files

	Args:
		repo_root: repository root path. If None, auto-detected.

	Returns:
		sorted list of script paths relative to repo root
	"""
	if repo_root is None:
		repo_root = get_repo_root()

	# Glob for all .py files under problems/*-problems/
	pattern = os.path.join(repo_root, "problems", "*-problems", "**", "*.py")
	all_py_files = glob.glob(pattern, recursive=True)

	generators = []
	for filepath in sorted(all_py_files):
		basename = os.path.basename(filepath)
		# Skip __init__.py and test files
		if basename == "__init__.py":
			continue
		if basename.startswith("test_"):
			continue

		# Read file and check for generator signals
		with open(filepath, "r") as f:
			content = f.read()

		# Must have a main block
		if "if __name__" not in content:
			continue

		# Must produce bbq output via bptools
		# Scripts that use collect_and_write_questions or make_outfile produce bbq files
		# Scripts without these (e.g., .pg generators) are skipped
		has_collect = "collect_and_write_questions" in content
		has_outfile = "make_outfile" in content
		if not (has_collect or has_outfile):
			continue

		# Store path relative to repo root
		rel_path = os.path.relpath(filepath, repo_root)
		generators.append(rel_path)

	return generators

#============================================
def get_script_basename(script_path: str) -> str:
	"""Extract the basename without extension from a script path.

	This mirrors how bptools.make_outfile() derives the script name
	from __main__.__file__ or sys.argv[0].

	Args:
		script_path: path to script (relative or absolute)

	Returns:
		basename without .py extension
	"""
	basename = os.path.basename(script_path)
	name = os.path.splitext(basename)[0]
	return name

#============================================
def find_bbq_files(script_path: str, search_dir: str) -> list:
	"""Find bbq output files matching a script name.

	Args:
		script_path: path to the generator script
		search_dir: directory to search for bbq files

	Returns:
		list of matching bbq file paths sorted by modification time (newest first)
	"""
	script_name = get_script_basename(script_path)
	pattern = os.path.join(search_dir, f"bbq-{script_name}*-questions.txt")
	matches = glob.glob(pattern)
	# Sort by modification time, newest first
	matches.sort(key=lambda p: os.path.getmtime(p), reverse=True)
	return matches

#============================================
def run_script(
	script_path: str,
	repo_root: str,
	extra_args: list = None,
	timeout: int = 30,
) -> dict:
	"""Run a generator script and capture its bbq output file.

	Records matching bbq files before execution, runs the script,
	then detects newly created or newest-modified matches.

	Args:
		script_path: path to script relative to repo root
		repo_root: repository root directory
		extra_args: additional CLI args (e.g. ['-y', 'input.yml'])
		timeout: max seconds to wait for script

	Returns:
		dict with keys: success, bbq_file, stdout, stderr, exit_code
	"""
	# Record existing bbq files before execution
	pre_existing = find_bbq_files(script_path, repo_root)
	pre_mtimes = {}
	for f in pre_existing:
		pre_mtimes[f] = os.path.getmtime(f)

	# Build command and environment, matching run_bbq_tasks.py approach
	abs_script = os.path.join(repo_root, script_path)
	cmd = ["python3", abs_script]
	# Disable anti-cheat that injects random words into question text
	cmd.extend(["--no-hidden-terms", "--allow-click"])
	if extra_args:
		cmd.extend(extra_args)

	# Build PYTHONPATH like run_bbq_tasks.py does
	env = os.environ.copy()
	env["PYTHONPATH"] = _build_pythonpath(repo_root)

	result = {
		"success": False,
		"bbq_file": None,
		"stdout": "",
		"stderr": "",
		"exit_code": -1,
	}

	proc = subprocess.run(
		cmd,
		capture_output=True, text=True,
		timeout=timeout,
		cwd=repo_root,
		env=env,
	)
	result["stdout"] = proc.stdout
	result["stderr"] = proc.stderr
	result["exit_code"] = proc.returncode

	if proc.returncode != 0:
		result["success"] = False
		return result

	# Find new or updated bbq files
	post_existing = find_bbq_files(script_path, repo_root)
	new_file = _find_new_bbq_file(post_existing, pre_mtimes)

	if new_file is None:
		result["success"] = False
		return result

	result["success"] = True
	result["bbq_file"] = new_file
	return result

#============================================
def _build_pythonpath(repo_root: str) -> str:
	"""Build PYTHONPATH for running generator scripts.

	Mirrors the approach in run_bbq_tasks.py: include the repo root
	and the qti-package-maker sibling repo.

	Args:
		repo_root: repository root directory

	Returns:
		colon-separated PYTHONPATH string
	"""
	parts = [repo_root]
	# Add qti-package-maker as sibling repo
	parent_dir = os.path.dirname(repo_root)
	qti_dir = os.path.join(parent_dir, "qti-package-maker")
	if os.path.isdir(qti_dir):
		parts.append(qti_dir)
	# Preserve existing PYTHONPATH entries
	existing = os.environ.get("PYTHONPATH", "")
	if existing:
		for p in existing.split(os.pathsep):
			if p and p not in parts:
				parts.append(p)
	result = os.pathsep.join(parts)
	return result

#============================================
def _find_new_bbq_file(post_files: list, pre_mtimes: dict) -> str:
	"""Identify the newly created or updated bbq file.

	Args:
		post_files: bbq files found after execution (newest first)
		pre_mtimes: dict of file -> mtime from before execution

	Returns:
		path to the new/updated file, or None
	"""
	# Check for entirely new files first
	for f in post_files:
		if f not in pre_mtimes:
			return f

	# Check for files with updated mtime
	for f in post_files:
		if f in pre_mtimes and os.path.getmtime(f) > pre_mtimes[f]:
			return f

	return None

#============================================
def cache_bbq_file(bbq_file: str, cache_dir: str) -> str:
	"""Copy a bbq output file to the cache directory.

	Args:
		bbq_file: path to the bbq output file
		cache_dir: directory to cache into

	Returns:
		path to the cached copy
	"""
	os.makedirs(cache_dir, exist_ok=True)
	basename = os.path.basename(bbq_file)
	cached_path = os.path.join(cache_dir, basename)
	shutil.copy2(bbq_file, cached_path)
	return cached_path

#============================================
def read_bbq_output(bbq_file: str) -> str:
	"""Read a bbq file and extract the first question statement.

	Uses the package interface to parse the bbq format, save as
	human_readable to a temp file, then extract just the question
	statement (no choices or answers) for classification.

	Args:
		bbq_file: path to the bbq output file

	Returns:
		question statement text (no HTML, no choices)
	"""
	import tempfile

	# Read bbq file through qti-package-maker
	packer = package_interface.QTIPackageInterface(
		package_name="classifier_temp",
		verbose=False,
		allow_mixed=True,
	)
	packer.read_package(bbq_file, "bbq_text")

	# Only need the first question for classification
	packer.trim_item_bank(1)

	# Save as human_readable to a temp file, then read it back
	with tempfile.TemporaryDirectory() as tmpdir:
		outfile = os.path.join(tmpdir, "human_output.txt")
		packer.save_package("human_readable", outfile)
		if not os.path.isfile(outfile):
			return ""
		with open(outfile, "r") as f:
			content = f.read()

	# Strip HTML wrapper if present (human_readable includes HTML header for browser display)
	if "<pre>" in content:
		content = content.split("<pre>", 1)[1]
	if "</pre>" in content:
		content = content.rsplit("</pre>", 1)[0]
	content = content.strip()

	# Extract just the question statement, strip choices and answers
	# Choices start with letter-dot (A. B. C.) or dash-space for answers
	statement_lines = []
	for line in content.split("\n"):
		stripped = line.strip()
		# Stop at first choice or answer line
		if stripped and stripped[0].isalpha() and len(stripped) > 2 and stripped[1] == '.':
			# Could be "A. choice" or "1. question" -- only stop for A-Z single letter
			if len(stripped[0]) == 1 and stripped[0].upper() in "ABCDEFGH":
				break
		if stripped.startswith("- ") or stripped.startswith("Answer:"):
			break
		statement_lines.append(line)
	content = "\n".join(statement_lines).strip()
	return content

#============================================
def read_source_code(script_path: str, repo_root: str) -> str:
	"""Read the full source code of a generator script.

	Args:
		script_path: path relative to repo root
		repo_root: repository root directory

	Returns:
		full source code as string
	"""
	abs_path = os.path.join(repo_root, script_path)
	with open(abs_path, "r") as f:
		content = f.read()
	return content

#============================================
def get_cached_bbq(script_path: str, cache_dir: str) -> str:
	"""Check if a cached bbq output file exists for a script.

	Args:
		script_path: path to the generator script
		cache_dir: cache directory to check

	Returns:
		path to cached file if found, None otherwise
	"""
	matches = find_bbq_files(script_path, cache_dir)
	if matches:
		cached_path = matches[0]
		return cached_path
	return None

#============================================
if __name__ == '__main__':
	repo_root = get_repo_root()
	scripts = discover_generator_scripts(repo_root)
	print(f"Found {len(scripts)} generator scripts:")
	for s in scripts[:10]:
		print(f"  {s}")
	if len(scripts) > 10:
		print(f"  ... and {len(scripts) - 10} more")
