"""Blank working tables for independent-assortment questions."""

import html
import random

import bptools


def choose_student_names(count):
	"""Sample distinct names from the repository list, escaped for HTML text."""
	with open(bptools.get_repo_data_path('student_names.txt'), encoding='utf-8') as names_file:
		names = list(dict.fromkeys(line.strip() for line in names_file if line.strip()))
	# ASVS V1.2.1: encode file content for the HTML text context.
	return [html.escape(name).encode('ascii', 'xmlcharrefreplace').decode('ascii')
		for name in random.sample(names, count)]


def make_work_table(gene_list1, names, gene_list2=None, last_step='gametes'):
	"""Show parental alleles and blank counts through the assessed step."""
	cell_style = 'border: 1px solid #aaa; padding: 7px 9px; text-align: center;'
	label_style = cell_style + ' text-align: left; font-weight: normal;'
	blank = f'<td style="{cell_style}">&nbsp;</td>'
	blocked = f'<td style="{cell_style} background-color: #222;">&nbsp;</td>'
	total_blank = f'<td style="{cell_style} background-color: #fce6cf;">&nbsp;</td>'
	gene_count = len(gene_list1)
	table = '<table style="border-collapse: collapse; font-family: Arial, sans-serif; '
	table += 'font-size: 15px; color: #111; background-color: #fff;">'
	table += f'<thead><tr><th scope="col" style="{label_style}">Genes &rarr;</th>'
	for gene_pair in gene_list1:
		table += f'<th scope="col" style="{cell_style} background-color: #c9dcf5;">'
		table += f'{gene_pair[0].upper()}</th>'
	table += f'<th scope="col" style="{cell_style} background-color: #c9dcf5;">'
	table += 'TOTAL</th></tr></thead><tbody>'
	parents = [(f'{names[0]} genotype', gene_list1)]
	if gene_list2 is not None:
		parents += [(f'{names[1]} genotype', gene_list2)]
	for label, gene_list in parents:
		table += f'<tr><th scope="row" style="{label_style}">{label}</th>'
		for gene_pair in gene_list:
			table += f'<td style="{cell_style} background-color: #e8f0fb; '
			table += f'font-family: monospace;">{"".join(gene_pair)}</td>'
		table += blocked + '</tr>'
	labels = [f'{names[0]} gametes']
	if gene_list2 is not None:
		labels = [f'(a) {names[0]} gametes', f'(b) {names[1]} gametes']
		labels += ['(c) Punnett square size']
		if last_step in ('genotypes', 'phenotypes'):
			labels += ['(d) Number of cross genotypes']
		if last_step == 'phenotypes':
			labels += ['(e) Number of cross phenotypes']
	for label in labels:
		table += f'<tr><th scope="row" style="{label_style}">{label}</th>'
		if label.startswith('(c)'):
			table += f'<td colspan="{gene_count}" style="{cell_style} '
			table += 'background-color: #222; color: #fff; text-align: right;">&rarr;</td>'
		else:
			table += blank * gene_count
		table += total_blank + '</tr>'
	table += '</tbody></table>'
	return table


def work_table_instructions(is_cross=False):
	"""Explain how students can use the blank table as scratch work."""
	text = '<p>Use the blank table to organize your work. For each gene, enter the '
	text += 'number of possibilities, then multiply across the row to find the total.</p>'
	if is_cross:
		text += '<p>Work in order: (a) and (b) count the different gametes each person '
		text += 'can produce; (c) give the Punnett square dimensions '
		text += '(rows &times; columns) and total number of cells; then count the '
		text += 'different offspring outcomes in the remaining row(s). '
		text += 'You do not need to draw the full Punnett square.</p>'
	text += '<p>Fill in the white cells and shaded TOTAL cells. '
	text += 'Use your final total to select the answer below.</p>'
	return text
