import os
import re
import random

import git_file_utils

REPO_ROOT = git_file_utils.get_repo_root()
REPORT_NAME = "report_markdown_links.txt"
ERROR_SAMPLE_COUNT = 5

# Inline link and image: optional leading !, [text](url), url ends at ) or space.
LINK_RE = re.compile(r"!?\[([^\]]*)\]\(\s*([^)\s]+)[^)]*\)")
# Inline code span, used to mask out example links inside backticks.
INLINE_CODE_RE = re.compile(r"`[^`]*`")
# Windows absolute path: drive letter then slash or backslash.
WINDOWS_PATH_RE = re.compile(r"^[A-Za-z]:[\\/]")

EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "ftp://")
# A URI scheme of 2+ chars (mailto:, tel:, bitcoin:, dash:, ...). Single-letter
# "schemes" are excluded so Windows drive paths (C:/...) are not misread.
SCHEME_RE = re.compile(r"^([a-z][a-z0-9+.\-]+):", re.IGNORECASE)
# Leading-slash links whose first segment is one of these are filesystem
# paths, not repo-root-relative GitHub links.
SYSTEM_ROOTS = {"home", "Users", "root", "private", "tmp", "var"}


#============================================
def strip_code_regions(text: str) -> list[tuple[int, str]]:
	"""
	Mask fenced code blocks and inline code spans.

	Fenced lines are blanked entirely; inline code spans are replaced with
	spaces so link syntax inside backticks is not parsed as a real link.

	Args:
		text: Full markdown file content.

	Returns:
		list[tuple[int, str]]: (line_number, masked_line) pairs, 1-based.
	"""
	masked_lines = []
	in_fence = False
	for index, line in enumerate(text.splitlines(), start=1):
		stripped = line.lstrip()
		# A line starting with ``` or ~~~ toggles the fenced block state.
		if stripped.startswith("```") or stripped.startswith("~~~"):
			in_fence = not in_fence
			masked_lines.append((index, ""))
			continue
		if in_fence:
			masked_lines.append((index, ""))
			continue
		# Replace inline code spans with spaces of equal length.
		masked = INLINE_CODE_RE.sub(blank_match, line)
		masked_lines.append((index, masked))
	return masked_lines


#============================================
def blank_match(match: re.Match) -> str:
	"""
	Replacement function for inline-code-span masking.

	Returns spaces of the same length as the matched span so column positions
	stay aligned for downstream parsing.
	"""
	return " " * len(match.group(0))


#============================================
def parse_links(masked_line: str) -> list[tuple[str, str]]:
	"""
	Extract inline links and images from a code-masked line.

	Args:
		masked_line: A line with code regions already masked.

	Returns:
		list[tuple[str, str]]: (link_text, url) pairs.
	"""
	links = []
	for match in LINK_RE.finditer(masked_line):
		link_text = match.group(1)
		url = match.group(2).strip()
		links.append((link_text, url))
	return links


#============================================
def classify_url(url: str) -> str:
	"""
	Classify a link URL.

	Returns:
		str: "external", "anchor", or "local".
	"""
	lowered = url.lower()
	if lowered.startswith(EXTERNAL_PREFIXES):
		return "external"
	if url.startswith("#"):
		return "anchor"
	# Non-file URI schemes (tel:, bitcoin:, dash:, ...) render as links on
	# GitHub and are not repo-local paths. Exclude file: so it still trips the
	# filesystem-path check as a local link.
	scheme_match = SCHEME_RE.match(url)
	if scheme_match and scheme_match.group(1).lower() != "file":
		return "external"
	return "local"


#============================================
def strip_anchor(url: str) -> str:
	"""
	Strip a #fragment or ?query suffix from a URL.
	"""
	url_no_anchor = url
	for separator in ("#", "?"):
		index = url_no_anchor.find(separator)
		if index != -1:
			url_no_anchor = url_no_anchor[:index]
	return url_no_anchor


#============================================
def looks_like_filesystem_path(url_no_anchor: str) -> bool:
	"""
	Check whether a local URL is a filesystem-absolute path.

	Filesystem-absolute links only work on one machine, never on github.com.
	This covers home paths, file:// URLs, Windows drive paths, and leading-slash
	links whose first segment is a known system root.
	"""
	if url_no_anchor.startswith("~/"):
		return True
	if url_no_anchor.lower().startswith("file:"):
		return True
	if WINDOWS_PATH_RE.match(url_no_anchor):
		return True
	if url_no_anchor.startswith("/"):
		segments = url_no_anchor.lstrip("/").split("/")
		if segments and segments[0] in SYSTEM_ROOTS:
			return True
	return False


#============================================
def resolve_target(repo_root: str, file_dir: str, url_no_anchor: str) -> str:
	"""
	Resolve a local URL to an absolute filesystem path.

	A leading slash resolves repo-root-relative (GitHub behavior); otherwise
	the URL resolves relative to the markdown file's own directory. Uses
	abspath and normpath only, so the target does not need to exist.
	"""
	if url_no_anchor.startswith("/"):
		target = os.path.join(repo_root, url_no_anchor.lstrip("/"))
	else:
		target = os.path.join(file_dir, url_no_anchor)
	return os.path.abspath(os.path.normpath(target))


#============================================
def to_posix(path: str) -> str:
	"""
	Convert a path to POSIX separators for markdown link suggestions.
	"""
	return path.replace(os.sep, "/")


#============================================
def target_path_tails(target_rel_to_root: str) -> list[str]:
	"""
	Build the set of accepted path-like text forms for a target.

	A path-like link text is accepted when it names the same file the URL
	resolves to. That includes the target's full repo-root-relative path and
	every tail suffix of its path components, so for target
	`skills/x/y.md` the accepted forms are `skills/x/y.md`, `x/y.md`, and
	`y.md`. The k=1 tail is the basename, so the older basename rule is
	covered automatically.
	"""
	segments = to_posix(target_rel_to_root).rstrip("/").split("/")
	tails = []
	for k in range(1, len(segments) + 1):
		tails.append("/".join(segments[-k:]))
	return tails


#============================================
def check_path_like_text(
	link_text: str,
	url_no_anchor: str,
	target_rel_to_root: str,
) -> str:
	"""
	Check that path-like link text matches the link target.

	Descriptive text (no `.md` and no `/`) is always allowed. Path-like text
	must equal the URL exactly OR any tail suffix of the target's repo-root-
	relative path components. Catches text/URL mismatches that resolve to
	different files; tolerates `[skills/foo/bar.md](../skills/foo/bar.md)`
	style where the source is in a sibling subtree and the text uses the
	repo-root form.

	Returns:
		str: Issue description, or "" when the link is fine.
	"""
	text = link_text.strip()
	# Allow one optional layer of backticks around the visible text.
	if len(text) > 1 and text.startswith("`") and text.endswith("`"):
		text = text[1:-1]
	if ".md" not in text and "/" not in text:
		return ""
	# Normalize trailing slashes so [tests/] vs target `tests` compares equal.
	text_norm = text.rstrip("/")
	url_norm = url_no_anchor.rstrip("/")
	tails = target_path_tails(target_rel_to_root)
	if text_norm == url_norm or text_norm in tails:
		return ""
	return (
		f"path-like link text [{link_text}] does not match target "
		f"({to_posix(target_rel_to_root)}); use the URL ({url_no_anchor}), "
		f"its basename ({tails[0]}), or a tail of the target path"
	)


#============================================
def check_local_link(
	repo_root: str,
	file_dir: str,
	tracked_set: set,
	tracked_dirs: set,
	link_text: str,
	url: str,
) -> str:
	"""
	Run all hard-error checks on a single local link.

	Returns:
		str: Issue description, or "" when the link is fine.
	"""
	url_no_anchor = strip_anchor(url)
	# A pure anchor or empty URL has no file part to check.
	if not url_no_anchor:
		return ""

	# Filesystem-absolute links never work on github.com.
	if looks_like_filesystem_path(url_no_anchor):
		return (
			f"local link [{link_text}]({url}) points outside repository "
			f"and will not work on GitHub"
		)

	target = resolve_target(repo_root, file_dir, url_no_anchor)
	rel_from_root = os.path.relpath(target, repo_root)

	# Repo containment: the target must live inside REPO_ROOT.
	if rel_from_root == ".." or rel_from_root.startswith(".." + os.sep):
		return (
			f"local link [{link_text}]({url}) escapes repository "
			f"and will not work on GitHub"
		)

	# Existence: the target must be a tracked file or a tracked directory
	# (GitHub renders dir links as a directory listing). Untracked files 404.
	rel_posix = to_posix(rel_from_root)
	if rel_posix not in tracked_set and rel_posix not in tracked_dirs:
		return f"local link [{link_text}]({url}) target not found: {rel_posix}"

	# Redundant traversal: the URL uses ".." but a ..-free path exists.
	if ".." in url_no_anchor.split("/"):
		rel_from_dir = os.path.relpath(target, file_dir)
		if ".." not in rel_from_dir.split(os.sep):
			return (
				f"local link [{link_text}]({url}) uses redundant '..' "
				f"traversal; use {to_posix(rel_from_dir)}"
			)

	# Path-like text must name the same file the URL resolves to.
	return check_path_like_text(link_text, url_no_anchor, rel_posix)


#============================================
def build_tracked_dirs(tracked_set: set) -> set:
	"""
	Compute the set of directories implied by tracked files.

	Every parent of every tracked path (in POSIX form) is included so that
	directory-target links such as `[skills/](../skills/)` resolve to a known
	location even though no file path matches the bare directory name.
	"""
	dirs = set()
	for path in tracked_set:
		parts = to_posix(path).split("/")
		# Build each parent prefix: parts[0], parts[0]/parts[1], ...
		for end in range(1, len(parts)):
			dirs.add("/".join(parts[:end]))
	return dirs


#============================================
def scan_file(
	repo_root: str,
	tracked_set: set,
	tracked_dirs: set,
	md_path: str,
) -> list[str]:
	"""
	Scan one markdown file for link issues.

	Args:
		repo_root: Absolute path to the repository root.
		tracked_set: Set of tracked repo-relative paths.
		tracked_dirs: Set of tracked-directory repo-relative paths.
		md_path: Repo-relative path to the markdown file.

	Returns:
		list[str]: "path:line: message" issue strings.
	"""
	abs_path = os.path.join(repo_root, md_path)
	file_dir = os.path.dirname(abs_path)
	with open(abs_path, encoding="utf-8") as handle:
		text = handle.read()

	issues = []
	for line_number, masked_line in strip_code_regions(text):
		for link_text, url in parse_links(masked_line):
			if classify_url(url) != "local":
				continue
			message = check_local_link(
				repo_root,
				file_dir,
				tracked_set,
				tracked_dirs,
				link_text,
				url,
			)
			if message:
				issues.append(f"{md_path}:{line_number}: {message}")
	return issues


#============================================
def gather_all(repo_root: str) -> list[str]:
	"""
	List all tracked markdown files.
	"""
	return git_file_utils.list_tracked_files(repo_root, ["*.md"])


#============================================
def gather_changed(repo_root: str) -> list[str]:
	"""
	List changed markdown files.
	"""
	changed = git_file_utils.list_changed_files(repo_root)
	return [path for path in changed if path.endswith(".md")]


#============================================
def report_issues(all_issues: list[str]) -> None:
	"""
	Write the report file and print samples, then fail.
	"""
	report_path = os.path.join(REPO_ROOT, REPORT_NAME)
	with open(report_path, "w", encoding="utf-8") as handle:
		for line in all_issues:
			handle.write(f"{line}\n")

	print("")
	print(f"First {ERROR_SAMPLE_COUNT} errors")
	for line in all_issues[:ERROR_SAMPLE_COUNT]:
		print(line)
	print("-------------------------")

	print(f"Random {ERROR_SAMPLE_COUNT} errors")
	sample = all_issues
	if len(all_issues) > ERROR_SAMPLE_COUNT:
		sample = random.sample(all_issues, ERROR_SAMPLE_COUNT)
	for line in sample:
		print(line)
	print("-------------------------")

	print(f"Last {ERROR_SAMPLE_COUNT} errors")
	for line in all_issues[-ERROR_SAMPLE_COUNT:]:
		print(line)
	print("-------------------------")

	# Count issues per file for a quick overview.
	file_counts = {}
	for line in all_issues:
		file_path = line.split(":", 1)[0]
		file_counts[file_path] = file_counts.get(file_path, 0) + 1
	print("Issues per file")
	for file_path in sorted(file_counts):
		print(f"{file_path}: {file_counts[file_path]}")
	print("")

	print(
		f"Found {len(all_issues)} markdown link errors written to "
		f"REPO_ROOT/{REPORT_NAME}"
	)
	raise AssertionError("Markdown link errors detected.")


#============================================
def test_markdown_links() -> None:
	"""
	Check every local markdown link is GitHub-browsable and well formed.
	"""
	files = git_file_utils.collect_files(REPO_ROOT, gather_all, gather_changed)

	# Delete any stale report before running.
	report_path = os.path.join(REPO_ROOT, REPORT_NAME)
	if os.path.exists(report_path):
		os.remove(report_path)

	if not files:
		print("No files matched the requested scope.")
		print("No errors found!!!")
		return

	tracked_set = set(git_file_utils.list_tracked_files(REPO_ROOT))
	tracked_dirs = build_tracked_dirs(tracked_set)

	all_issues = []
	for md_path in sorted(files):
		all_issues.extend(scan_file(REPO_ROOT, tracked_set, tracked_dirs, md_path))

	if not all_issues:
		print("No errors found!!!")
		return

	report_issues(all_issues)
