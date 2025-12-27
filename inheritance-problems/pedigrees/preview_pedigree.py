#!/usr/bin/env python3

# Standard Library
import argparse
import os
import random

# Local repo modules
import pedigree_graph_lib
import pedigree_html_lib
import pedigree_png_lib
import pedigree_template_gen_lib
import pedigree_validate_lib


#===============================
def parse_args():
	"""
	Parse command-line arguments.
	"""
	parser = argparse.ArgumentParser(description="Preview pedigree HTML and PNG outputs.")
	parser.add_argument(
		'-m', '--mode', dest='mode', type=str, default='autosomal recessive',
		help='Inheritance mode for generated pedigrees'
	)
	parser.add_argument(
		'-t', '--generator', dest='generator', type=str,
		choices=('template', 'graph'), default='graph',
		help='Generator source: template or graph'
	)
	parser.add_argument(
		'-g', '--generations', dest='generations', type=int, default=4,
		help='Number of generations to request'
	)
	parser.add_argument(
		'-c', '--starting-couples', dest='starting_couples', type=int, default=1,
		help='Number of founder couples to start (1 to 3)'
	)
	parser.add_argument(
		'-n', '--count', dest='count', type=int, default=12,
		help='Number of pedigrees to generate'
	)
	parser.add_argument(
		'-o', '--outdir', dest='outdir', type=str, default='previews',
		help='Output directory for HTML, PNG, and code strings'
	)
	parser.add_argument(
		'-s', '--scale', dest='scale', type=float, default=1.3,
		help='Scale factor for PNG rendering'
	)
	parser.add_argument(
		'--seed', dest='seed', type=int, default=None,
		help='Random seed for reproducible previews'
	)
	parser.add_argument(
		'--show-carriers', dest='show_carriers', action='store_true',
		help='Render carrier symbols for recessive modes'
	)
	args = parser.parse_args()
	return args


#===============================
def make_index_entry(index_lines, label, png_file, html_text, code_text):
	index_lines.append(f"<h3>{label}</h3>")
	index_lines.append(f"<p><img src='{png_file}' alt='{label}'></p>")
	index_lines.append("<div style='margin-bottom: 24px;'>")
	index_lines.append(html_text)
	index_lines.append("<pre>")
	index_lines.append(code_text)
	index_lines.append("</pre>")
	index_lines.append("</div>")


#===============================
def main():
	"""
	Generate HTML and PNG previews for pedigrees.
	"""
	args = parse_args()
	os.makedirs(args.outdir, exist_ok=True)

	if args.seed is None:
		rng = random.Random()
	else:
		rng = random.Random(args.seed)

	index_lines = []
	index_lines.append("<html><head><meta charset='UTF-8'></head><body>")
	index_lines.append(f"<h1>Pedigree previews: {args.mode}</h1>")

	attempts = 0
	generated = 0
	max_attempts = args.count * 20
	max_width_cells = 60
	max_height_cells = 20

	while generated < args.count and attempts < max_attempts:
		attempts += 1
		if args.generator == 'template':
			code_string = pedigree_template_gen_lib.make_pedigree_code(
				args.mode,
				generations=args.generations,
				allow_mirror=True,
				rng=rng,
			)
		else:
			code_string = pedigree_graph_lib.generate_pedigree_code(
				args.mode,
				generations=args.generations,
				starting_couples=args.starting_couples,
				rng=rng,
				show_carriers=args.show_carriers,
			)

		errors = pedigree_validate_lib.validate_code_string_strict(
			code_string,
			max_width_cells=max_width_cells,
			max_height_cells=max_height_cells
		)
		if errors:
			continue

		generated += 1
		idx = generated
		html_text = pedigree_html_lib.make_pedigree_html(code_string)
		png_name = f"preview_{idx:03d}.png"
		txt_name = f"preview_{idx:03d}.txt"
		png_path = os.path.join(args.outdir, png_name)
		txt_path = os.path.join(args.outdir, txt_name)

		pedigree_png_lib.save_pedigree_png(code_string, png_path, scale=args.scale)
		with open(txt_path, 'w') as txt_handle:
			txt_handle.write(code_string)

		label = f"{args.mode} {idx:03d}"
		make_index_entry(index_lines, label, png_name, html_text, code_string)

	index_lines.append("</body></html>")
	index_path = os.path.join(args.outdir, "index.html")
	with open(index_path, 'w') as index_handle:
		index_handle.write("\n".join(index_lines))

	if generated < args.count:
		print(f"WARNING: generated {generated} of {args.count} previews after {attempts} attempts.")
	print(f"Saved previews to {args.outdir}")


#===============================
if __name__ == '__main__':
	main()

## THE END
