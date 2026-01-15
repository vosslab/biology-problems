#!/opt/homebrew/opt/python@3.12/bin/python3.12
import os
import random
import re
import subprocess
import sys


EXTENSIONS = {
	".md",
	".txt",
	".py",
	".js",
	".jsx",
	".ts",
	".tsx",
	".html",
	".htm",
	".css",
	".json",
	".yml",
	".yaml",
	".toml",
	".ini",
	".cfg",
	".conf",
	".sh",
	".bash",
	".zsh",
	".fish",
	".csv",
	".tsv",
	".xml",
	".svg",
	".sql",
	".rb",
	".php",
	".java",
	".c",
	".h",
	".cpp",
	".hpp",
	".go",
	".rs",
	".swift",
}
SKIP_DIRS = {".git", ".venv", "old_shell_folder"}
PYTHON_BIN = "/opt/homebrew/opt/python@3.12/bin/python3.12"
ERROR_RE = re.compile(r":[0-9]+:[0-9]+:")
CODEPOINT_RE = re.compile(r"non-ISO-8859-1 character U\+([0-9A-Fa-f]{4,6})")
ERROR_SAMPLE_COUNT = 5


#============================================
def is_emoji_codepoint(codepoint: int) -> bool:
	"""
	Check whether a codepoint is likely an emoji.

	Args:
		codepoint: Integer Unicode codepoint.

	Returns:
		bool: True if the codepoint falls in a common emoji range.
	"""
	if 0x1F000 <= codepoint <= 0x1FAFF:
		return True
	if 0x2600 <= codepoint <= 0x27BF:
		return True
	return False


#============================================
def find_repo_root() -> str:
	"""
	Locate the repository root using git.

	Returns:
		str: Absolute repo root path, or empty string on failure.
	"""
	result = subprocess.run(
		["git", "rev-parse", "--show-toplevel"],
		capture_output=True,
		text=True,
	)
	if result.returncode != 0:
		message = result.stderr.strip()
		if not message:
			message = "Failed to determine repo root."
		print(message, file=sys.stderr)
		return ""
	return result.stdout.strip()


#============================================
def get_progress_colors() -> dict[str, str]:
	"""
	Get ANSI color codes for progress output.

	Returns:
		dict[str, str]: Color code mapping.
	"""
	if sys.stderr.isatty():
		return {
			"reset": "\033[0m",
			"green": "\033[32m",
			"yellow": "\033[33m",
			"red": "\033[31m",
		}
	return {"reset": "", "green": "", "yellow": "", "red": ""}


#============================================
def gather_files(
	repo_root: str,
	ascii_out: str,
	pyflakes_out: str,
) -> list[str]:
	"""
	Collect files to scan, honoring extension and skip rules.

	Args:
		repo_root: Root path for the repo.
		ascii_out: Output path to skip.
		pyflakes_out: Output path to skip.

	Returns:
		list[str]: Sorted file list.
	"""
	matches = []
	skip_files = {ascii_out, pyflakes_out}
	for root, dirs, files in os.walk(repo_root):
		dirs[:] = [name for name in dirs if name not in SKIP_DIRS]
		for name in files:
			ext = os.path.splitext(name)[1].lower()
			if ext not in EXTENSIONS:
				continue
			path = os.path.join(root, name)
			if path in skip_files:
				continue
			matches.append(path)
	matches.sort()
	return matches


#============================================
def shorten_error_path(line: str) -> str:
	"""
	Shorten a full error path to just the basename.

	Args:
		line: Full error line.

	Returns:
		str: Error line with shortened path.
	"""
	separator = line.find(":")
	if separator == -1:
		return line
	path = line[:separator]
	remainder = line[separator:]
	return f"{os.path.basename(path)}{remainder}"


#============================================
def sample_errors(lines: list[str], count: int) -> list[str]:
	"""
	Sample up to N error lines.

	Args:
		lines: Full list of error lines.
		count: Desired sample size.

	Returns:
		list[str]: Sampled error lines.
	"""
	if len(lines) <= count:
		return list(lines)
	return random.sample(lines, count)


#============================================
def list_error_files(lines: list[str]) -> list[str]:
	"""
	Collect unique file paths from error lines.

	Args:
		lines: Error lines with path prefixes.

	Returns:
		list[str]: Sorted unique paths.
	"""
	paths = set()
	for line in lines:
		separator = line.find(":")
		if separator == -1:
			continue
		paths.add(line[:separator])
	return sorted(paths)


#============================================
def count_error_details(lines: list[str]) -> tuple[dict[str, int], dict[str, int]]:
	"""
	Count errors by file and by Unicode codepoint.

	Args:
		lines: Error lines with path prefixes.

	Returns:
		tuple[dict[str, int], dict[str, int]]: File and codepoint counts.
	"""
	file_counts = {}
	codepoint_counts = {}
	for line in lines:
		match = CODEPOINT_RE.search(line)
		if not match:
			continue
		separator = line.find(":")
		if separator == -1:
			continue
		file_path = line[:separator]
		file_counts[file_path] = file_counts.get(file_path, 0) + 1
		codepoint = match.group(1).upper()
		codepoint_counts[codepoint] = codepoint_counts.get(codepoint, 0) + 1
	return file_counts, codepoint_counts


#============================================
def top_items(counts: dict[str, int], limit: int) -> list[tuple[str, int]]:
	"""
	Sort a count dictionary by descending count.

	Args:
		counts: Map of key to count.
		limit: Maximum number of items to return.

	Returns:
		list[tuple[str, int]]: Sorted key/count pairs.
	"""
	items = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
	return items[:limit]


#============================================
def main() -> int:
	"""
	Run the ASCII compliance check runner.

	Returns:
		int: Process exit code.
	"""
	repo_root = find_repo_root()
	if not repo_root:
		return 1

	ascii_out = os.path.join(repo_root, "ascii_compliance.txt")
	pyflakes_out = os.path.join(repo_root, "pyflakes.txt")
	script_path = os.path.join(repo_root, "tests", "check_ascii_compliance.py")

	if not os.path.isfile(script_path):
		print(f"Missing script: {script_path}", file=sys.stderr)
		return 1

	with open(ascii_out, "w", encoding="utf-8"):
		pass

	files = gather_files(repo_root, ascii_out, pyflakes_out)
	colors = get_progress_colors()

	with open(ascii_out, "a", encoding="utf-8") as ascii_handle:
		for file_path in files:
			status = 0
			result = subprocess.run(
				[PYTHON_BIN, script_path, "-i", file_path],
				stderr=ascii_handle,
			)
			status = result.returncode
			if status == 0:
				sys.stderr.write(f"{colors['green']}.{colors['reset']}")
			elif status == 2:
				sys.stderr.write(f"{colors['yellow']}+{colors['reset']}")
			else:
				sys.stderr.write(f"{colors['red']}!{colors['reset']}")
			sys.stderr.flush()

	sys.stderr.write("\n")
	sys.stderr.flush()

	with open(ascii_out, "r", encoding="utf-8") as handle:
		all_lines = [line.rstrip("\n") for line in handle]

	if not all_lines:
		print("No errors found!!!")
		return 0

	error_lines = [line for line in all_lines if ERROR_RE.search(line)]

	print("")
	print(f"First {ERROR_SAMPLE_COUNT} errors")
	for line in error_lines[:ERROR_SAMPLE_COUNT]:
		print(shorten_error_path(line))
	print("-------------------------")
	print("")

	print(f"Random {ERROR_SAMPLE_COUNT} errors")
	for line in sample_errors(error_lines, ERROR_SAMPLE_COUNT):
		print(shorten_error_path(line))
	print("-------------------------")
	print("")

	print(f"Last {ERROR_SAMPLE_COUNT} errors")
	for line in error_lines[-ERROR_SAMPLE_COUNT:]:
		print(shorten_error_path(line))
	print("-------------------------")
	print("")

	error_files = list_error_files(error_lines)
	error_file_count = len(error_files)
	file_counts, codepoint_counts = count_error_details(error_lines)
	emoji_count = 0
	for codepoint in codepoint_counts:
		codepoint_int = int(codepoint, 16)
		if is_emoji_codepoint(codepoint_int):
			emoji_count += codepoint_counts[codepoint]

	if error_file_count <= 5:
		print(f"Files with errors ({error_file_count})")
		for path in error_files:
			count = file_counts.get(path, 0)
			print(f"{os.path.relpath(path, repo_root)}: {count}")
		print("")
	else:
		print(f"Files with errors: {error_file_count}")
		top_files = top_items(file_counts, ERROR_SAMPLE_COUNT)
		if top_files:
			print("")
			print("Top 5 files by error count")
			for path, count in top_files:
				display_path = os.path.relpath(path, repo_root)
				print(f"{display_path}: {count}")
	top_codepoints = top_items(codepoint_counts, ERROR_SAMPLE_COUNT)
	if top_codepoints:
		print("")
		print("Top 5 Unicode characters by frequency")
		for codepoint, count in top_codepoints:
			display_char = chr(int(codepoint, 16))
			if not display_char.isprintable() or display_char.isspace():
				display_char = "?"
			print(f"U+{codepoint} {display_char}: {count}")
	if emoji_count:
		print("")
		print(f"Found {emoji_count} emoji codepoints; handle them case by case.")

	print("Found {} ASCII compliance errors written to REPO_ROOT/ascii_compliance.txt".format(
		len(all_lines),
	))
	return 1


if __name__ == "__main__":
	raise SystemExit(main())
