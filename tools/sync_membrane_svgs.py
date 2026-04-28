#!/usr/bin/env python3
"""
Sync membrane component SVGs into the three production PGML files.

Source-of-truth SVGs live in
problems/biochemistry-problems/membranes/:

  - phospholipid-unit.svg   -> $PHOSPHO_UNIT_SVG
  - transporter-protein.svg -> $PROTEIN_INNER_SVG

Each SVG wraps its drawn content in a <g id="..."> group. This script
extracts the inner content of that group and rewrites the matching
SYNC block in every membrane PGML, e.g.:

  # ---- BEGIN SYNC: phospholipid-unit.svg ----
  $PHOSPHO_UNIT_SVG = '<path .../>'
      . '<circle .../>';
  # ---- END SYNC: phospholipid-unit.svg ----

Edit the SVGs in Inkscape, then run this script to refresh all three
PGMLs in lockstep. Color, stroke-width, and geometry live in the SVG
files; the PGMLs only position the inlined content.
"""

import os
import re
import sys
import argparse
import subprocess

# Map: SVG basename -> (group id, Perl scalar name)
COMPONENTS = (
	('phospholipid-unit.svg',    'phospholipid-unit',   'PHOSPHO_UNIT_SVG'),
	('transporter-protein.svg',  'transporter-protein', 'PROTEIN_INNER_SVG'),
)

PGML_FILES = (
	'identify_transporter_type.pgml',
	'driving_force_from_gradient.pgml',
	'coupled_transport_perturbation.pgml',
)

MEMBRANES_DIR = 'problems/biochemistry-problems/membranes'


#============================================
def parse_args():
	"""Parse command-line arguments."""
	parser = argparse.ArgumentParser(
		description="Sync membrane SVGs into the three PGML files."
	)
	parser.add_argument(
		'-n', '--dry-run', dest='dry_run', action='store_true',
		help="Show the new SYNC block content without writing files."
	)
	args = parser.parse_args()
	return args


#============================================
def extract_group_inner(svg_path: str, group_id: str) -> str:
	"""Return the inner XML of <g id=group_id>...</g> with whitespace tidied.

	Args:
		svg_path: Absolute path to an SVG file.
		group_id: id attribute on the wrapping <g> element.
	"""
	with open(svg_path, 'r', encoding='utf-8') as fh:
		text = fh.read()
	# Match the opening tag with the requested id then capture up to </g>.
	pattern = re.compile(
		r'<g\s+[^>]*id\s*=\s*"' + re.escape(group_id) + r'"[^>]*>(.*?)</g>',
		re.DOTALL,
	)
	match = pattern.search(text)
	if match is None:
		raise SystemExit(
			f"<g id={group_id!r}> not found in {svg_path}"
		)
	inner = match.group(1).strip()
	# Collapse any internal whitespace runs to single spaces so
	# Perl-string formatting is predictable.
	inner = re.sub(r'\s+', ' ', inner)
	return inner


#============================================
def split_self_closing_tags(inner_xml: str) -> list:
	"""Split the inner XML into a list of tag substrings.

	Each list item is a single self-closing element like '<path .../>'
	or '<circle .../>'. The two SVGs we sync only contain self-closing
	primitives, so we error out if anything else is present.
	"""
	# Find every self-closing tag.
	tags = re.findall(r'<[a-zA-Z][^<>]*?/>', inner_xml)
	# Sanity-check coverage: re-joining the tags should match the
	# whitespace-collapsed input. Anything missing means a non-self-
	# closing element snuck in.
	rebuilt = ''.join(tags)
	stripped_input = re.sub(r'\s+', '', inner_xml)
	if re.sub(r'\s+', '', rebuilt) != stripped_input:
		raise SystemExit(
			"Inner XML has tags this script does not handle. "
			"Only self-closing primitives are supported. Inner XML: "
			+ inner_xml
		)
	return tags


#============================================
def format_perl_scalar(varname: str, tags: list) -> str:
	"""Format the tag list as a Perl scalar assignment.

	First tag goes on the assignment line; subsequent tags are appended
	with `	. '...'` so the block reads naturally.
	"""
	if not tags:
		raise SystemExit(f"No tags to assign to ${varname}")
	# Reject single-quote characters; Perl single-quoted strings
	# would need q{...} fallback, but neither real SVG uses them.
	for tag in tags:
		if "'" in tag:
			raise SystemExit(
				f"Tag contains a single quote and cannot be embedded in "
				f"a Perl single-quoted string: {tag}"
			)
	lines = [f"${varname} = '{tags[0]}'"]
	for tag in tags[1:]:
		lines.append(f"\t. '{tag}'")
	# Last line gets the terminating semicolon.
	lines[-1] = lines[-1] + ';'
	return '\n'.join(lines)


#============================================
def build_sync_block(svg_basename: str, varname: str, body: str) -> str:
	"""Return the full BEGIN/END SYNC block including marker lines."""
	begin = f"# ---- BEGIN SYNC: {svg_basename} ----"
	end = f"# ---- END SYNC: {svg_basename} ----"
	header_comment = (
		f"# Source of truth: {svg_basename} in this folder.\n"
		f"# Refresh by running tools/sync_membrane_svgs.py.\n"
		f"# DO NOT EDIT BY HAND inside the SYNC markers.\n"
	)
	block = begin + '\n' + header_comment + body + '\n' + end
	return block


#============================================
def replace_sync_block(pgml_text: str, svg_basename: str, new_block: str) -> str:
	"""Replace the BEGIN/END SYNC block for svg_basename in pgml_text."""
	begin = re.escape(f"# ---- BEGIN SYNC: {svg_basename} ----")
	end = re.escape(f"# ---- END SYNC: {svg_basename} ----")
	pattern = re.compile(begin + r'.*?' + end, re.DOTALL)
	if pattern.search(pgml_text) is None:
		raise SystemExit(
			f"SYNC markers for {svg_basename!r} not found in PGML. "
			f"Add the BEGIN/END marker pair to the PGML before "
			f"running this script."
		)
	# Use a function replacement so backslashes in new_block stay literal.
	return pattern.sub(lambda _m: new_block, pgml_text, count=1)


#============================================
def main():
	"""Sync entry point."""
	args = parse_args()
	# Resolve repo root via git so the script works from any CWD.
	repo_root = subprocess.check_output(
		['git', 'rev-parse', '--show-toplevel'], text=True
	).strip()
	membranes = os.path.join(repo_root, MEMBRANES_DIR)

	# Build (svg_basename, varname, sync_block_text) for each component.
	component_blocks = []
	for svg_basename, group_id, varname in COMPONENTS:
		svg_path = os.path.join(membranes, svg_basename)
		inner = extract_group_inner(svg_path, group_id)
		tags = split_self_closing_tags(inner)
		perl_assignment = format_perl_scalar(varname, tags)
		block = build_sync_block(svg_basename, varname, perl_assignment)
		component_blocks.append((svg_basename, block))
		print(f"Extracted {len(tags)} tag(s) from {svg_basename} -> ${varname}")

	# Apply replacements to every PGML.
	any_change = False
	for pgml_name in PGML_FILES:
		pgml_path = os.path.join(membranes, pgml_name)
		with open(pgml_path, 'r', encoding='utf-8') as fh:
			before = fh.read()
		after = before
		for svg_basename, block in component_blocks:
			after = replace_sync_block(after, svg_basename, block)
		if after == before:
			print(f"  {pgml_name}: no change")
			continue
		any_change = True
		if args.dry_run:
			print(f"  {pgml_name}: would update (dry run)")
			continue
		with open(pgml_path, 'w', encoding='utf-8') as fh:
			fh.write(after)
		print(f"  {pgml_name}: updated")

	if args.dry_run and any_change:
		print("Dry run: no files written.")


#============================================
if __name__ == '__main__':
	main()
