#!/usr/bin/env python3
"""
Rewrite broken markdown links in a chosen set of markdown files.

For each broken local link:
  1. If the URL's basename matches exactly one tracked file in the repo,
     rewrite the URL to the correct relative path from source to that file.
     Prefer canonical (non-archive) matches over archive matches.
  2. Otherwise, convert to backticked basename (delink).

Also: normalize path-like link text to URL basename when text != URL.

Scope selection:
  -g/--glob PATTERN [PATTERN ...]
      Select markdown files by glob pattern or by directory. Arguments are
      anchored at the repo root, so the tool behaves the same from any
      subdirectory, and absolute arguments inside the repo also work. Quote
      patterns so Python expands them even when the shell does not.

        docs/specs/          bare directory: RECURSIVE, every *.md under it
        docs/specs/*.md      that directory's top level only
        docs/specs/**/*.md   recursive, spelled out

      A trailing slash is optional: docs/specs and docs/specs/ behave alike.
  (no -g/--glob)
      Use the default pattern docs/archive/**/*.md. That folder is created
      lazily by changelog rotation, so its absence simply matches nothing.

Only *.md matches are processed, and the final file list is de-duplicated, so
a file reachable through two overlapping patterns is processed exactly once.

Replacements for the retired preset flags:
  --include-changelog     ->  --glob 'docs/CHANGELOG*.md'
  --include-active-plans  ->  --glob 'docs/active_plans/**/*.md'
  --include-experiments   ->  --glob 'experiments/**/*.md'
  --include-canonical     ->  --glob 'docs/*.md' 'docs/specs/**/*.md'

Dry-run by default; pass --apply to write.

Single-file mode: pass -i/--input FILE to process one markdown file.
In single-file mode --apply is the default; pass -n/--dry-run to preview.
"""

import os
import re
import glob
import pathlib
import argparse
import subprocess

# Standard Library imports above.

#============================================
LINK_PATTERN = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')

# Scope used when no -g/--glob is given. docs/archive/ is created lazily by
# changelog rotation, so a repo that has never rotated simply matches nothing.
DEFAULT_GLOB = 'docs/archive/**/*.md'


#============================================
def get_repo_root() -> pathlib.Path:
	"""Return the repo root via `git rev-parse --show-toplevel`."""
	result = subprocess.run(
		['git', 'rev-parse', '--show-toplevel'],
		capture_output=True, text=True, check=True,
	)
	root = pathlib.Path(result.stdout.strip())
	return root


#============================================
def anchor_pattern(repo_root: pathlib.Path, pattern: str) -> str:
	"""Anchor one -g/--glob argument at the repo root and reject escapes.

	A repo-relative argument is joined onto the repo root rather than the
	current working directory, so the tool behaves identically no matter which
	subdirectory it is run from. Absolute arguments are accepted as typed. The
	join is normalized lexically (not via resolve()) because a pattern holds
	wildcards and need not name an existing path. normpath also drops a
	trailing slash, so 'docs/specs' and 'docs/specs/' anchor identically.

	Args:
		repo_root: Repository root, as returned by get_repo_root().
		pattern: One glob pattern or directory as typed on the command line.

	Returns:
		str: Absolute, normalized glob pattern inside the repo root.

	Raises:
		ValueError: The pattern points outside the repo root.
	"""
	root = str(repo_root.resolve())
	if os.path.isabs(pattern):
		anchored = os.path.normpath(pattern)
	else:
		anchored = os.path.normpath(os.path.join(root, pattern))
	# Containment: the root itself is allowed, anything else must sit under it.
	# normpath has already collapsed any '..' segments, so a traversal pattern
	# such as '../../etc/*.md' fails this check rather than sneaking through.
	if anchored != root and not anchored.startswith(root + os.sep):
		raise ValueError('glob pattern is outside the repo root: ' + pattern)
	return anchored


#============================================
def expand_pattern(repo_root: pathlib.Path, pattern: str) -> str:
	"""Anchor one -g/--glob argument, expanding a bare directory into a walk.

	Naming a folder generally means everything in it, so a bare directory
	becomes a RECURSIVE markdown walk. Handing the directory to glob.glob
	unchanged would match only the directory itself, which the *.md filter then
	drops, leaving a silently empty scope. An argument that already carries
	wildcards is anchored and otherwise left alone, which keeps 'docs/*.md'
	top-level only and 'docs/**/*.md' recursive.

	Args:
		repo_root: Repository root, as returned by get_repo_root().
		pattern: One glob pattern or directory as typed on the command line.

	Returns:
		str: Absolute glob pattern ready for glob.glob(recursive=True).

	Raises:
		ValueError: The pattern points outside the repo root.
	"""
	anchored = anchor_pattern(repo_root, pattern)
	if os.path.isdir(anchored):
		anchored = os.path.join(anchored, '**', '*.md')
	return anchored


#============================================
def collect_markdown_files(repo_root: pathlib.Path, patterns: list) -> list:
	"""Expand glob patterns into a sorted, de-duplicated list of *.md files.

	recursive=True is required so '**' spans directories; without it '**'
	quietly degrades to a single '*' and silently narrows the scope. Non-md
	matches are dropped because a pattern like 'docs/*' would otherwise hand
	Python files to a markdown link rewriter. De-duplication matters because
	the rewriting pass is not safe to run twice over the same text, so a file
	reachable through two overlapping patterns must appear exactly once.

	Raises:
		ValueError: A pattern points outside the repo root.
	"""
	source_files = []
	seen = set()
	for pattern in patterns:
		anchored = expand_pattern(repo_root, pattern)
		for match in glob.glob(anchored, recursive=True):
			candidate = pathlib.Path(match)
			if candidate.suffix.lower() != '.md' or not candidate.is_file():
				continue
			resolved = candidate.resolve()
			if resolved not in seen:
				seen.add(resolved)
				source_files.append(resolved)
	source_files.sort()
	return source_files


#============================================
def collect_markdown_files_or_exit(repo_root: pathlib.Path,
		patterns: list) -> list:
	"""CLI wrapper: report a bad --glob pattern without a traceback."""
	try:
		source_files = collect_markdown_files(repo_root, patterns)
	except ValueError as error:
		raise SystemExit('ERROR: ' + str(error))
	return source_files


#============================================
def build_tracked_set(repo_root: pathlib.Path) -> set:
	"""Set of relative paths of every file tracked by git."""
	result = subprocess.run(
		['git', '-C', str(repo_root), 'ls-files'],
		capture_output=True, text=True, check=True,
	)
	tracked = set()
	for line in result.stdout.splitlines():
		line = line.strip()
		if line:
			tracked.add(line)
	return tracked


#============================================
def build_basename_index(tracked: set, archive_prefix: str) -> tuple:
	"""Return (canonical_index, archive_index): basename -> [relpath, ...].

	Canonical = tracked files NOT under archive_prefix.
	Archive = tracked files under archive_prefix.
	"""
	canonical = {}
	archive = {}
	for rel in tracked:
		basename = pathlib.PurePosixPath(rel).name
		if rel.startswith(archive_prefix):
			archive.setdefault(basename, []).append(rel)
		else:
			canonical.setdefault(basename, []).append(rel)
	return canonical, archive


#============================================
def split_anchor(url: str) -> tuple:
	"""Split url into (path, anchor_suffix) where anchor includes '#'."""
	if '#' in url:
		path, anchor = url.split('#', 1)
		return path, '#' + anchor
	return url, ''


#============================================
def is_local_file_link(url: str) -> bool:
	"""True if URL looks like a local file link, not external/anchor-only."""
	if not url:
		return False
	no_anchor = url.split('#', 1)[0]
	if not no_anchor:
		return False
	if no_anchor.startswith(('http://', 'https://', 'mailto:', 'data:',
			'ftp://', 'javascript:', 'tel:')):
		return False
	return True


#============================================
def link_target_tracked(source_file: pathlib.Path, link_url: str,
		tracked: set, repo_root: pathlib.Path) -> bool:
	"""True if link URL resolves to a git-tracked file."""
	url_path, _ = split_anchor(link_url)
	target = (source_file.parent / url_path).resolve()
	try:
		rel = target.relative_to(repo_root)
	except ValueError:
		return False
	return str(rel) in tracked


#============================================
def find_basename_match(basename: str, canonical: dict, archive: dict) -> str:
	"""Lookup basename, prefer canonical. Return rel path or None.

	None if 0 matches or ambiguous.
	"""
	can_hits = canonical.get(basename, [])
	if len(can_hits) == 1:
		return can_hits[0]
	if len(can_hits) > 1:
		return None
	arch_hits = archive.get(basename, [])
	if len(arch_hits) == 1:
		return arch_hits[0]
	return None


#============================================
def process_file(source_file: pathlib.Path, apply_changes: bool,
		tracked: set, canonical: dict, archive: dict,
		repo_root: pathlib.Path) -> dict:
	"""Walk one md file. Rewrite broken or path-mismatched links.

	Returns counts and per-file changes.
	"""
	counts = {'scanned': 0, 'broken': 0, 'rewritten': 0,
		'text_normalized': 0, 'delinked': 0, 'unresolved': 0,
		'changes': []}
	original_text = source_file.read_text(encoding='utf-8')
	new_text = original_text

	for match in LINK_PATTERN.finditer(original_text):
		link_text = match.group(1)
		link_url = match.group(2)
		if not is_local_file_link(link_url):
			continue
		counts['scanned'] += 1
		url_path, anchor = split_anchor(link_url)
		url_basename = pathlib.PurePosixPath(url_path).name
		if link_target_tracked(source_file, link_url, tracked, repo_root):
			# Target valid. Normalize path-like link text != URL.
			if '/' in link_text and link_text != link_url:
				old_link = '[' + link_text + '](' + link_url + ')'
				new_link = '[' + url_basename + '](' + link_url + ')'
				new_text = new_text.replace(old_link, new_link, 1)
				counts['text_normalized'] += 1
				counts['changes'].append((old_link, new_link))
			continue
		counts['broken'] += 1
		if not url_basename:
			counts['unresolved'] += 1
			continue
		target_rel = find_basename_match(url_basename, canonical, archive)
		if target_rel is None:
			# no match or ambiguous: delink to backticked basename
			old_link = '[' + link_text + '](' + link_url + ')'
			new_text = new_text.replace(old_link, '`' + url_basename + '`', 1)
			counts['delinked'] += 1
			counts['changes'].append((old_link, '`' + url_basename + '`'))
			continue
		# rewrite URL to relative path from source dir to target
		target_abs = repo_root / target_rel
		new_url = os.path.relpath(target_abs, start=source_file.parent) + anchor
		old_link = '[' + link_text + '](' + link_url + ')'
		# also normalize link text if it is a path different from new URL
		new_text_part = link_text
		if '/' in link_text and link_text != new_url:
			new_text_part = pathlib.PurePosixPath(new_url.split('#')[0]).name
		new_link = '[' + new_text_part + '](' + new_url + ')'
		new_text = new_text.replace(old_link, new_link, 1)
		counts['rewritten'] += 1
		counts['changes'].append((old_link, new_link))

	if apply_changes and new_text != original_text:
		source_file.write_text(new_text, encoding='utf-8')

	return counts


#============================================
def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments."""
	parser = argparse.ArgumentParser(
		description='Rewrite broken md links in a chosen set of markdown files.'
	)
	parser.add_argument('-i', '--input', dest='input_files', nargs='+',
		help='Process one or more markdown files (globs expand via the shell). '
			'In this mode --apply is the default; use --dry-run to preview.')
	parser.add_argument('-a', '--apply', dest='apply_changes',
		action='store_true', help='Write changes to disk (default: dry-run).')
	parser.add_argument('-n', '--dry-run', dest='dry_run',
		action='store_true',
		help='Preview only. In single-file mode, overrides the apply default.')
	parser.add_argument('-v', '--verbose', dest='verbose',
		action='store_true', help='Print every rewrite.')
	parser.add_argument('-g', '--glob', dest='glob_patterns', nargs='+',
		default=[], metavar='PATTERN',
		help='Select *.md files by glob pattern or directory, anchored at the '
			'repo root (globs expand in Python, so quote them). A bare '
			'directory walks recursively; a wildcard pattern is used as typed, '
			"so 'docs/*.md' is top level only and 'docs/**/*.md' recurses. "
			"Default: '" + DEFAULT_GLOB + "'. "
			"Example: --glob docs/specs/ 'tests/*.md'.")
	args = parser.parse_args()
	return args


#============================================
def run_files(source_files: list, apply_changes: bool, tracked: set,
		canonical: dict, archive: dict, repo_root: pathlib.Path,
		verbose: bool) -> None:
	"""Process every source file, tally totals, print summary."""
	totals = {'scanned': 0, 'broken': 0, 'rewritten': 0,
		'text_normalized': 0, 'delinked': 0, 'unresolved': 0,
		'files_changed': 0}

	for source_file in sorted(source_files):
		counts = process_file(source_file, apply_changes,
			tracked, canonical, archive, repo_root)
		totals['scanned'] += counts['scanned']
		totals['broken'] += counts['broken']
		totals['rewritten'] += counts['rewritten']
		totals['text_normalized'] += counts['text_normalized']
		totals['delinked'] += counts['delinked']
		totals['unresolved'] += counts['unresolved']
		changed_now = (counts['rewritten'] + counts['delinked'] +
			counts['text_normalized'])
		if changed_now > 0:
			totals['files_changed'] += 1
			if verbose:
				rel = source_file.relative_to(repo_root)
				print(str(rel) + ': ' + str(changed_now) + ' changes')
				for old, new in counts['changes']:
					print('  ' + old + ' -> ' + new)

	mode = 'APPLY' if apply_changes else 'DRY-RUN'
	print('')
	print('=' * 60)
	print('Mode: ' + mode)
	print('Files scanned: ' + str(len(source_files)))
	print('Local links scanned: ' + str(totals['scanned']))
	print('Broken links found: ' + str(totals['broken']))
	print('Rewritten (basename matched, path fixed): ' + str(totals['rewritten']))
	print('Text normalized (text path != URL): ' + str(totals['text_normalized']))
	print('Delinked (no basename match): ' + str(totals['delinked']))
	print('Unresolved (no basename / ambiguous): ' + str(totals['unresolved']))
	print('Files changed: ' + str(totals['files_changed']))


#============================================
def main() -> None:
	"""Entry point: walk source files, rewrite broken md links."""
	args = parse_args()
	repo_root = get_repo_root()

	tracked = build_tracked_set(repo_root)
	canonical, archive = build_basename_index(tracked, 'docs/archive/')

	# Single-file/glob mode: apply by default, --dry-run to preview.
	if args.input_files:
		source_files = []
		for pattern in args.input_files:
			# Expand glob in Python so quoted patterns work even when the
			# shell does not expand them.
			matches = glob.glob(pattern)
			if not matches:
				raise SystemExit('ERROR: no files match input pattern: ' + pattern)
			for match in matches:
				source_files.append(pathlib.Path(match).resolve())
		apply_changes = not args.dry_run
		run_files(source_files, apply_changes, tracked, canonical, archive,
			repo_root, args.verbose)
		return

	# Glob mode: dry-run by default, --apply to write. An explicit -g/--glob
	# replaces the default scope entirely, so `--glob 'tests/*.md'` walks
	# tests/ and nothing else.
	apply_changes = args.apply_changes and not args.dry_run
	patterns = args.glob_patterns
	if not patterns:
		patterns = [DEFAULT_GLOB]

	source_files = collect_markdown_files_or_exit(repo_root, patterns)
	# Zero matches is a note, not an error: the patterns describe a union, and
	# the default pattern legitimately matches nothing in a repo that has never
	# rotated its changelog. (-i/--input keeps its per-pattern hard error,
	# because there the user named specific files to rewrite.)
	if not source_files:
		print('No markdown files matched: ' + ' '.join(patterns))
		print("Pass -g/--glob PATTERN to choose a scope, "
			"for example: --glob 'docs/**/*.md'")

	run_files(source_files, apply_changes, tracked, canonical, archive,
		repo_root, args.verbose)


if __name__ == '__main__':
	main()
