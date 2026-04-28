#!/usr/bin/env python3
"""
Normalize SVG files: crop whitespace and shift coordinates so viewBox starts at 0,0.

Walks all drawn elements to compute the bounding box, shifts every coordinate
attribute by the required offset, and rewrites the viewBox to 0 0 W H with
configurable padding.

Handles: rect, circle, ellipse, line, path (absolute M/L/Q/C commands), text.
Also processes elements inside defs/clipPath.
"""

import os
import re
import sys
import argparse

import lxml.etree

# SVG namespace
SVG_NS = "http://www.w3.org/2000/svg"
NS = {"svg": SVG_NS}


#============================================
def parse_args():
	"""Parse command-line arguments."""
	parser = argparse.ArgumentParser(
		description="Normalize SVG viewBox to 0,0 origin by shifting all coordinates"
	)
	parser.add_argument(
		'files', nargs='*',
		help="SVG files to normalize"
	)
	parser.add_argument(
		'-d', '--directory', dest='directory',
		help="Process all .svg files in this directory"
	)
	parser.add_argument(
		'-p', '--padding', dest='padding', type=float, default=2.0,
		help="Padding around content in px (default: 2)"
	)
	parser.add_argument(
		'-n', '--dry-run', dest='dry_run', action='store_true',
		help="Show changes without writing files"
	)
	args = parser.parse_args()
	return args


#============================================
def get_float_attr(elem, attr: str, default: float = 0.0) -> float:
	"""Get a float attribute from an element, returning default if missing."""
	val = elem.get(attr)
	if val is None:
		return default
	return float(val)


#============================================
def parse_path_tokens(d_str: str) -> list:
	"""
	Tokenize an SVG path d attribute into a list of commands and numbers.

	Returns a list of (command_letter, [numbers]) tuples.
	"""
	# split into command groups: each starts with a letter
	tokens = []
	# find all commands with their coordinate data
	parts = re.findall(r'([A-Za-z])\s*([^A-Za-z]*)', d_str)
	for cmd, nums_str in parts:
		# extract all numbers (including negatives and decimals)
		nums = [float(x) for x in re.findall(r'-?[0-9]*\.?[0-9]+', nums_str)]
		tokens.append((cmd, nums))
	return tokens


#============================================
def shift_path_d(d_str: str, dx: float, dy: float) -> str:
	"""
	Shift all absolute coordinates in a path d attribute by (dx, dy).

	Handles M, L, Q, C, Z commands (uppercase/absolute only).
	Lowercase (relative) commands are left unchanged.
	"""
	tokens = parse_path_tokens(d_str)
	parts = []
	for cmd, nums in tokens:
		if cmd in ('M', 'L'):
			# pairs of (x, y)
			shifted = []
			for i in range(0, len(nums), 2):
				if i + 1 < len(nums):
					shifted.append(f"{nums[i] + dx:g}")
					shifted.append(f"{nums[i+1] + dy:g}")
			parts.append(cmd + " " + " ".join(shifted))
		elif cmd == 'Q':
			# quadratic bezier: cx cy x y (groups of 4)
			shifted = []
			for i in range(0, len(nums), 4):
				if i + 3 < len(nums):
					shifted.append(f"{nums[i] + dx:g}")
					shifted.append(f"{nums[i+1] + dy:g}")
					shifted.append(f"{nums[i+2] + dx:g}")
					shifted.append(f"{nums[i+3] + dy:g}")
			parts.append(cmd + " " + " ".join(shifted))
		elif cmd == 'C':
			# cubic bezier: x1 y1 x2 y2 x y (groups of 6)
			shifted = []
			for i in range(0, len(nums), 6):
				if i + 5 < len(nums):
					shifted.append(f"{nums[i] + dx:g}")
					shifted.append(f"{nums[i+1] + dy:g}")
					shifted.append(f"{nums[i+2] + dx:g}")
					shifted.append(f"{nums[i+3] + dy:g}")
					shifted.append(f"{nums[i+4] + dx:g}")
					shifted.append(f"{nums[i+5] + dy:g}")
			parts.append(cmd + " " + " ".join(shifted))
		elif cmd == 'Z':
			parts.append('Z')
		else:
			# relative commands (m, l, q, c, z) or unknown: leave as-is
			if nums:
				parts.append(cmd + " " + " ".join(f"{n:g}" for n in nums))
			else:
				parts.append(cmd)
	return " ".join(parts)


#============================================
def path_bbox(d_str: str) -> tuple:
	"""
	Compute bounding box of a path from its d attribute.

	Returns (min_x, min_y, max_x, max_y) based on all coordinate values.
	This is approximate -- it uses control points, not the actual curve,
	which gives a slightly larger box. Good enough for our SVGs.
	"""
	tokens = parse_path_tokens(d_str)
	xs = []
	ys = []
	for cmd, nums in tokens:
		if cmd in ('M', 'L', 'Q', 'C'):
			# all nums are alternating x, y values
			for i in range(0, len(nums), 2):
				if i + 1 < len(nums):
					xs.append(nums[i])
					ys.append(nums[i + 1])
	if not xs:
		return None
	return (min(xs), min(ys), max(xs), max(ys))


#============================================
def is_invisible(elem) -> bool:
	"""Check if an element is invisible (hidden anchor rects, etc.)."""
	if elem.get("display") == "none":
		return True
	# elements with fill=none AND stroke=none are invisible
	if elem.get("fill") == "none" and elem.get("stroke") == "none":
		return True
	return False


#============================================
def element_bbox(elem) -> tuple:
	"""
	Compute bounding box for a single SVG element.

	Returns (min_x, min_y, max_x, max_y) or None if not a drawn element.
	"""
	# strip namespace for tag comparison
	tag = elem.tag
	if not isinstance(tag, str):
		return None
	if "}" in tag:
		tag = tag.split("}")[1]

	if tag == "rect":
		x = get_float_attr(elem, "x")
		y = get_float_attr(elem, "y")
		w = get_float_attr(elem, "width")
		h = get_float_attr(elem, "height")
		return (x, y, x + w, y + h)

	elif tag == "circle":
		cx = get_float_attr(elem, "cx")
		cy = get_float_attr(elem, "cy")
		r = get_float_attr(elem, "r")
		return (cx - r, cy - r, cx + r, cy + r)

	elif tag == "ellipse":
		cx = get_float_attr(elem, "cx")
		cy = get_float_attr(elem, "cy")
		rx = get_float_attr(elem, "rx")
		ry = get_float_attr(elem, "ry")
		return (cx - rx, cy - ry, cx + rx, cy + ry)

	elif tag == "line":
		x1 = get_float_attr(elem, "x1")
		y1 = get_float_attr(elem, "y1")
		x2 = get_float_attr(elem, "x2")
		y2 = get_float_attr(elem, "y2")
		return (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))

	elif tag == "path":
		d = elem.get("d")
		if d:
			return path_bbox(d)

	elif tag == "text":
		x = get_float_attr(elem, "x")
		y = get_float_attr(elem, "y")
		# estimate text height from font-size attribute
		font_size = get_float_attr(elem, "font-size", 10)
		# text baseline is at y, so the top is roughly y - font_size
		# width is hard to estimate; use a rough guess of font_size * len(text)
		text_content = elem.text or ""
		# approximate width: 0.6 * font_size per character
		est_width = len(text_content) * font_size * 0.6
		return (x, y - font_size, x + est_width, y)

	return None


#============================================
def compute_svg_bbox(root) -> tuple:
	"""
	Walk all elements in an SVG tree and compute the overall bounding box.

	Skips invisible elements (display=none, fill=none+stroke=none).
	Returns (min_x, min_y, max_x, max_y).
	"""
	min_x = float('inf')
	min_y = float('inf')
	max_x = float('-inf')
	max_y = float('-inf')

	for elem in root.iter():
		if is_invisible(elem):
			continue
		bbox = element_bbox(elem)
		if bbox is not None:
			min_x = min(min_x, bbox[0])
			min_y = min(min_y, bbox[1])
			max_x = max(max_x, bbox[2])
			max_y = max(max_y, bbox[3])

	if min_x == float('inf'):
		return None
	return (min_x, min_y, max_x, max_y)


#============================================
def shift_element(elem, dx: float, dy: float):
	"""Shift coordinate attributes of a single element by (dx, dy)."""
	tag = elem.tag
	if not isinstance(tag, str):
		return
	if "}" in tag:
		tag = tag.split("}")[1]

	if tag == "rect":
		if elem.get("x") is not None:
			elem.set("x", f"{get_float_attr(elem, 'x') + dx:g}")
		if elem.get("y") is not None:
			elem.set("y", f"{get_float_attr(elem, 'y') + dy:g}")

	elif tag == "circle":
		if elem.get("cx") is not None:
			elem.set("cx", f"{get_float_attr(elem, 'cx') + dx:g}")
		if elem.get("cy") is not None:
			elem.set("cy", f"{get_float_attr(elem, 'cy') + dy:g}")

	elif tag == "ellipse":
		if elem.get("cx") is not None:
			elem.set("cx", f"{get_float_attr(elem, 'cx') + dx:g}")
		if elem.get("cy") is not None:
			elem.set("cy", f"{get_float_attr(elem, 'cy') + dy:g}")

	elif tag == "line":
		if elem.get("x1") is not None:
			elem.set("x1", f"{get_float_attr(elem, 'x1') + dx:g}")
		if elem.get("y1") is not None:
			elem.set("y1", f"{get_float_attr(elem, 'y1') + dy:g}")
		if elem.get("x2") is not None:
			elem.set("x2", f"{get_float_attr(elem, 'x2') + dx:g}")
		if elem.get("y2") is not None:
			elem.set("y2", f"{get_float_attr(elem, 'y2') + dy:g}")

	elif tag == "path":
		d = elem.get("d")
		if d:
			elem.set("d", shift_path_d(d, dx, dy))

	elif tag == "text":
		if elem.get("x") is not None:
			elem.set("x", f"{get_float_attr(elem, 'x') + dx:g}")
		if elem.get("y") is not None:
			elem.set("y", f"{get_float_attr(elem, 'y') + dy:g}")


#============================================
def normalize_svg(filepath: str, padding: float, dry_run: bool) -> bool:
	"""
	Normalize a single SVG file: compute bbox, shift coords, update viewBox.

	Returns True if the file was modified (or would be in dry-run mode).
	"""
	# parse preserving comments and whitespace
	parser = lxml.etree.XMLParser(remove_blank_text=False, remove_comments=False)
	tree = lxml.etree.parse(filepath, parser)
	root = tree.getroot()

	# check for unsupported SVG features that would produce incorrect results
	basename = os.path.basename(filepath)
	for elem in root.iter():
		tag = elem.tag
		if not isinstance(tag, str):
			continue
		if "}" in tag:
			tag = tag.split("}")[1]
		# transforms would invalidate our coordinate shifting
		if elem.get("transform") is not None:
			print(f"  {basename}: SKIPPED -- has transform attribute (unsupported)")
			return False
		# use/symbol elements reference other geometry we cannot reliably shift
		if tag in ("use", "symbol"):
			print(f"  {basename}: SKIPPED -- has <{tag}> element (unsupported)")
			return False
		# gradients with coordinate attributes would need shifting too
		if tag in ("linearGradient", "radialGradient"):
			print(f"  {basename}: SKIPPED -- has <{tag}> element (unsupported)")
			return False
		# relative path commands would not be shifted correctly
		if tag == "path":
			d = elem.get("d", "")
			rel_cmds = re.findall(r'[mlhvcsqtaz]', d)
			if rel_cmds:
				print(f"  {basename}: SKIPPED -- has relative path commands {rel_cmds} (unsupported)")
				return False

	# compute bounding box of visible content
	bbox = compute_svg_bbox(root)
	if bbox is None:
		print(f"  {os.path.basename(filepath)}: no drawable elements found, skipping")
		return False

	content_min_x, content_min_y, content_max_x, content_max_y = bbox
	content_width = content_max_x - content_min_x
	content_height = content_max_y - content_min_y

	# target viewBox: 0 0 (content_width + 2*padding) (content_height + 2*padding)
	new_vb_w = content_width + 2 * padding
	new_vb_h = content_height + 2 * padding

	# shift needed: move content so that content_min lands at (padding, padding)
	dx = padding - content_min_x
	dy = padding - content_min_y

	# check if shift is significant (more than 0.1px)
	old_vb = root.get("viewBox", "")
	new_vb = f"0 0 {new_vb_w:g} {new_vb_h:g}"

	if abs(dx) < 0.1 and abs(dy) < 0.1 and old_vb == new_vb:
		print(f"  {os.path.basename(filepath)}: already normalized")
		return False

	print(f"  {os.path.basename(filepath)}:")
	print(f"    viewBox: {old_vb} -> {new_vb}")
	print(f"    shift: dx={dx:+.1f}, dy={dy:+.1f}")
	print(f"    content bounds: ({content_min_x:.1f}, {content_min_y:.1f}) to ({content_max_x:.1f}, {content_max_y:.1f})")

	if dry_run:
		return True

	# shift all elements (including inside defs/clipPath)
	for elem in root.iter():
		shift_element(elem, dx, dy)

	# update viewBox
	root.set("viewBox", new_vb)

	# remove width/height if present (let viewBox control sizing)
	if root.get("width") is not None:
		del root.attrib["width"]
	if root.get("height") is not None:
		del root.attrib["height"]

	# write back
	# write as UTF-8, no XML declaration
	result = lxml.etree.tostring(root, encoding="unicode", xml_declaration=False)
	with open(filepath, 'w') as f:
		f.write(result)

	# ensure file ends with newline
	with open(filepath, 'r') as f:
		content = f.read()
	if not content.endswith('\n'):
		with open(filepath, 'a') as f:
			f.write('\n')

	print(f"    written: {filepath}")

	return True


#============================================
def main():
	"""Main entry point."""
	args = parse_args()

	# collect file list
	files = list(args.files) if args.files else []
	if args.directory:
		for name in sorted(os.listdir(args.directory)):
			if name.endswith('.svg'):
				files.append(os.path.join(args.directory, name))

	if not files:
		print("No SVG files specified. Use positional args or -d directory.")
		sys.exit(1)

	mode_label = " (dry run)" if args.dry_run else ""
	print(f"Normalizing {len(files)} SVG files with {args.padding}px padding{mode_label}:")

	modified = 0
	for filepath in files:
		if not os.path.isfile(filepath):
			print(f"  {filepath}: file not found, skipping")
			continue
		if normalize_svg(filepath, args.padding, args.dry_run):
			modified += 1

	print(f"\n{modified} file(s) {'would be ' if args.dry_run else ''}modified.")


if __name__ == '__main__':
	main()
