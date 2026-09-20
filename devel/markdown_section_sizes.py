#!/usr/bin/env python3
# This file is vendored. Local changes can and will be overwritten by propagation.

"""List Markdown headings with their line numbers, sorted by bullet count.

Counts the '- ' bullet lines that sit directly under each heading (up to the
next heading of any level) so long sections that want splitting rise to the top.
"""

# Standard Library
import re
import signal
import argparse

HEADING_PATTERN = re.compile(r"^(#{1,6}) (.*)$")
BULLET_PATTERN = re.compile(r"^- ")


#============================================
def parse_args() -> argparse.Namespace:
	"""
	Parse command-line arguments.
	"""
	parser = argparse.ArgumentParser(
		description="List Markdown headings sorted by the number of top-level bullets under each"
	)
	parser.add_argument('-i', '--input', dest='input_file', required=True, help="Markdown file")
	parser.add_argument(
		'-n', '--top', dest='top', type=int, default=0,
		help="Show only the N largest sections (default: all)",
	)
	parser.add_argument(
		'-m', '--min', dest='minimum', type=int, default=0,
		help="Show only sections with at least this many bullets (default: 0)",
	)
	args = parser.parse_args()
	return args


#============================================
def collect_sections(lines: list) -> list:
	"""
	Return one record per heading: (bullet_count, line_number, level, title).

	Bullets are counted until the next heading of any level, so a parent heading
	counts only the bullets that precede its first subheading.
	"""
	sections = []
	current = None
	for line_number, line in enumerate(lines, start=1):
		heading = HEADING_PATTERN.match(line)
		if heading:
			if current is not None:
				sections.append(current)
			level = len(heading.group(1))
			current = [0, line_number, level, heading.group(2).strip()]
			continue
		if current is not None and BULLET_PATTERN.match(line):
			current[0] += 1
	if current is not None:
		sections.append(current)
	return sections


#============================================
def main() -> None:
	# Let a closed pipe (for example `| head`) end the process quietly, as a shell tool should.
	signal.signal(signal.SIGPIPE, signal.SIG_DFL)
	args = parse_args()
	with open(args.input_file) as fh:
		lines = fh.read().splitlines()
	sections = collect_sections(lines)
	# largest first; ties keep document order
	sections.sort(key=lambda record: (-record[0], record[1]))
	shown = [record for record in sections if record[0] >= args.minimum]
	if args.top > 0:
		shown = shown[:args.top]
	for bullet_count, line_number, level, title in shown:
		marker = "#" * level
		print(f"{bullet_count:4d}  {line_number:5d}: {marker} {title}")
	total_bullets = sum(record[0] for record in sections)
	print(f"{len(sections)} headings, {total_bullets} bullets, {len(shown)} shown")


if __name__ == '__main__':
	main()
