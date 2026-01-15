#!/usr/bin/env python3

import io
import time
import argparse
import contextlib

from treelib import tools
from treelib import lookup
from treelib import permute
from treelib import treecodeclass
from treelib import output


#===========================================
def group_tree_codes_by_common_name(tree_code_str_list: list[str]) -> dict[str, list[str]]:
	groups: dict[str, list[str]] = {}
	for tree_code_str in tree_code_str_list:
		common_name = lookup.get_common_name_from_tree_code(tree_code_str)
		if common_name is None:
			common_name = tools.reset_sort_taxa_in_code(tree_code_str)
		groups[common_name] = groups.get(common_name, []) + [tree_code_str]
	return groups


#===========================================
def render_ascii_tree(tree_code_str: str, renderer: output.GeneTreeOutput) -> str:
	buffer = io.StringIO()
	with contextlib.redirect_stdout(buffer):
		renderer.print_ascii_tree(tree_code_str)
	return buffer.getvalue()


#===========================================
def write_ascii_gallery(outfile: str, groups: dict[str, list[str]], max_per_group: int):
	renderer = output.GeneTreeOutput()
	renderer.replace_names = False
	group_names = list(groups.keys())
	group_names.sort()
	with open(outfile, "w", encoding="utf-8") as f:
		f.write("All gene trees\n\n")
		for i, group_name in enumerate(group_names):
			tree_codes = groups[group_name]
			tree_codes.sort()
			f.write(f"{i+1}. {group_name} -- {len(tree_codes)} trees\n")
			count = 0
			for tree_code_str in tree_codes:
				f.write(f"tree_code: {tree_code_str}\n")
				f.write(render_ascii_tree(tree_code_str, renderer))
				f.write("\n")
				count += 1
				if count >= max_per_group:
					break
			f.write("\n")


#===========================================
def write_html_gallery(outfile: str, groups: dict[str, list[str]], max_per_group: int):
	html = "<html><head><meta charset='utf-8'/>"
	html += "<title>All gene trees</title>"
	html += "<style>"
	html += "body{font-family:Arial, sans-serif;}"
	html += "code{background:#eee; padding:2px 4px;}"
	html += "table{margin:10px 0;}"
	html += "</style>"
	html += "</head><body>"
	html += "<h1>All gene trees</h1>"

	group_names = list(groups.keys())
	group_names.sort()
	for i, group_name in enumerate(group_names):
		tree_codes = groups[group_name]
		tree_codes.sort()
		html += f"<h2>{i+1}. {group_name} &mdash; {len(tree_codes)} trees</h2>"
		count = 0
		for tree_code_str in tree_codes:
			treecode_cls = treecodeclass.TreeCode(tree_code_str)
			html += treecode_cls.get_html_table(caption=False)
			html += f"<p><code>{tree_code_str}</code></p>"
			count += 1
			if count >= max_per_group:
				break
	html += "</body></html>"
	with open(outfile, "w", encoding="utf-8") as f:
		f.write(html)

#===========================================
#===========================================
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Generate and inspect all gene trees.")
	parser.add_argument('-l', '--leaves', '--num-leaves', type=int, dest='num_leaves',
		help='number of leaves in gene trees', default=5)
	parser.add_argument('-d', '--duplicate-runs', type=int, dest='duplicate_runs',
		help='legacy flag (unused); kept for compatibility', default=1)
	parser.add_argument('-c', '--choices', type=int, dest='num_choices',
		help='number of example trees to render per group (when --html is used)', default=5)
	parser.add_argument('--html', dest='write_html', action='store_true',
		help='write an HTML gallery of trees')
	parser.add_argument('--no-html', dest='write_html', action='store_false',
		help='disable HTML gallery output')
	parser.add_argument('--ascii', dest='write_ascii', action='store_true',
		help='write an ASCII gallery of trees')
	parser.add_argument('--no-ascii', dest='write_ascii', action='store_false',
		help='disable ASCII gallery output')
	parser.set_defaults(write_html=True, write_ascii=True)
	parser.add_argument('-H', '--html-outfile', dest='html_outfile', type=str,
		help='output HTML file name', default=None)
	parser.add_argument('-A', '--ascii-outfile', dest='ascii_outfile', type=str,
		help='output ASCII file name', default=None)
	parser.add_argument('-o', '--outfile', dest='outfile', type=str,
		help='legacy HTML outfile name (deprecated; use --html-outfile)', default=None)
	args = parser.parse_args()

	if args.num_leaves > 7:
		raise ValueError("Too many leaves requested (>7). This can be extremely slow and memory-heavy.")

	t0 = time.time()
	base_treecode_cls_list = lookup.get_all_base_tree_codes_for_leaf_count(args.num_leaves)
	base_tree_code_str_list = [t.tree_code_str for t in base_treecode_cls_list]
	tree_code_str_list = permute.get_all_permuted_tree_codes_from_tree_code_list(base_tree_code_str_list)
	tree_code_str_list = list(set(tree_code_str_list))
	tree_code_str_list.sort()

	groups = group_tree_codes_by_common_name(tree_code_str_list)
	print(f"Generated {len(tree_code_str_list):,d} gene trees for {args.num_leaves} leaves in {time.time()-t0:.3f}s")
	print(f"Grouped into {len(groups):,d} common-name groups")

	if args.write_html:
		if args.html_outfile is None:
			if args.outfile is None:
				args.html_outfile = f"all_gene_trees-{args.num_leaves}-leaves.html"
			else:
				args.html_outfile = args.outfile
		write_html_gallery(args.html_outfile, groups, args.num_choices)
		print(f"Wrote HTML gallery to: {args.html_outfile}")

	if args.write_ascii:
		if args.ascii_outfile is None:
			args.ascii_outfile = f"all_gene_trees-{args.num_leaves}-leaves.txt"
		write_ascii_gallery(args.ascii_outfile, groups, args.num_choices)
		print(f"Wrote ASCII gallery to: {args.ascii_outfile}")
