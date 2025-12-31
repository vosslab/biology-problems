#!/usr/bin/env python3

# Standard Library
import argparse
import os

# Local repo modules
import pedigree_html_lib
import pedigree_svg_lib
import pedigree_validate_lib


#===============================
def parse_args():
	"""
	Parse command-line arguments.
	"""
	parser = argparse.ArgumentParser(description='Render a pedigree code string to HTML or PNG.')
	parser.add_argument(
		'--code', dest='code', type=str, default=None,
		help='Pedigree code string to render'
	)
	parser.add_argument(
		'--code-file', dest='code_file', type=str, default=None,
		help='Path to a file containing a pedigree code string'
	)
	parser.add_argument(
		'--png', dest='write_png', action='store_true',
		help='Write a PNG render'
	)
	parser.add_argument(
		'--html', dest='write_html', action='store_true',
		help='Write an HTML render'
	)
	parser.add_argument(
		'--svg', dest='write_svg', action='store_true',
		help='Write an SVG render'
	)
	parser.add_argument(
		'-o', '--out', dest='out', type=str, default='code_render',
		help='Output base name or file path'
	)
	parser.add_argument(
		'-s', '--scale', dest='scale', type=float, default=1.3,
		help='PNG scale factor'
	)
	args = parser.parse_args()
	return args


#===============================
def _load_code(args) -> str:
	if args.code:
		return args.code
	if args.code_file:
		with open(args.code_file, 'r') as handle:
			return handle.read().strip()
	raise ValueError('Provide --code or --code-file.')


#===============================
def _output_path(base: str, suffix: str) -> str:
	if base.lower().endswith(suffix):
		return base
	return f"{base}{suffix}"


#===============================
def main():
	"""
	Render a pedigree code string to HTML and/or PNG.
	"""
	args = parse_args()
	code_string = _load_code(args)

	if not args.write_png and not args.write_html and not args.write_svg:
		raise ValueError('Select at least one output with --png, --html, or --svg.')
	errors = pedigree_validate_lib.validate_row_parity_semantics(code_string)
	if errors:
		raise ValueError("Invalid pedigree code string:\n" + "\n".join(errors))

	if args.write_html:
		html_path = _output_path(args.out, '.html')
		html_text = pedigree_html_lib.make_pedigree_html(code_string)
		with open(html_path, 'w') as handle:
			handle.write(html_text)
		print(f"Wrote HTML to {html_path}")

	if args.write_png:
		png_path = _output_path(args.out, '.png')
		pedigree_svg_lib.save_pedigree_png(code_string, png_path, scale=args.scale)
		print(f"Wrote PNG to {png_path}")

	if args.write_svg:
		svg_path = _output_path(args.out, '.svg')
		pedigree_svg_lib.save_pedigree_svg(code_string, svg_path, scale=args.scale)
		print(f"Wrote SVG to {svg_path}")


#===============================
if __name__ == '__main__':
	main()

## THE END
