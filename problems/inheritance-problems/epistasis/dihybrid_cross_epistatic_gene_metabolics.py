#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
# Provides functions to generate random numbers and selections
import copy
import os
import random
import sys

# Import external modules (pip-installed)
# No external modules are used here currently

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
inheritance_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
for path in (repo_root, inheritance_root):
	if path not in sys.path:
		sys.path.insert(0, path)

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities
import bptools
import hybridcrosslib

red_x = '<span style="color: red;"><b>&#10005;</b></span>'

#===================
#===================
def digenic_inheritance(color_set):
	# Four colors
	#0: '9:3:3:1',
	AB_color_raw = color_set[0]
	Ab_color_raw = color_set[1]
	aB_color_raw = color_set[2]
	ab_color_raw = color_set[3]
	AB_color = hybridcrosslib.color_translate.get(AB_color_raw, AB_color_raw)
	Ab_color = hybridcrosslib.color_translate.get(Ab_color_raw, Ab_color_raw)
	aB_color = hybridcrosslib.color_translate.get(aB_color_raw, aB_color_raw)
	ab_color = hybridcrosslib.color_translate.get(ab_color_raw, ab_color_raw)

	table = '<table border="0" style="border: 0px solid white; border-collapse: collapse; ">'
	table += '<tr>'
	table += ' <td style="border: 1px solid black; vertical-align: bottom;" align="center">'

	table += '<table border="0" style="border: 0px solid white; border-collapse: collapse; ">'
	for i in range(3):
		table += '<colgroup width="60"></colgroup> '
	table += '<tr><td></td><td align="center">Gene 1</td></tr>'
	table += '<tr>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(ab_color_raw, ab_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(Ab_color_raw, Ab_color)
	table += '</tr>'
	table += '</table>'
	table += '<b>Only Gene 1 Dominant</b>'

	table += '</td><td style="border: 1px solid black; vertical-align: bottom;" align="center">'

	table += '<table border="0" style="border: 0px solid white; border-collapse: collapse; ">'
	for i in range(3):
		table += '<colgroup width="60"></colgroup> '
	table += '<tr><td></td><td align="center">Gene 2</td></tr>'
	table += '<tr>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(ab_color_raw, ab_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(aB_color_raw, aB_color)
	table += '</tr>'
	table += '</table>'
	table += '<b>Only Gene 2 Dominant</b>'

	table += '</td><td style="border: 1px solid black; vertical-align: bottom;" align="center">'

	table += '<table border="0" style="border: 0px solid white; border-collapse: collapse; ">'
	for i in range(3):
		table += '<colgroup width="60"></colgroup> '
	table += '<tr><td></td><td align="center">Genes 1&plus;2</td></tr>'
	table += '<tr>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(ab_color_raw, ab_color)
	table += ' <td align="center">&xrarr;&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(AB_color_raw, AB_color)
	table += '</tr>'
	table += '</table>'
	table += '<b>Both Genes Dominant</b>'

	table += '</td></tr>'
	table += '</table>'

	#assigned_colors = hybridcrosslib.dihybridAssignColors(0, color_set)
	#print(hybridcrosslib.createDiHybridTable('A', 'B', assigned_colors, 'digenic inheritance'))

	description = table+'<br/>'
	description += 'A two step metabolic pathway determines the pigment color. '
	description += 'Gene 1 when dominant expresses an enzyme that creates the {0} pigment from the {1} precursor pigment. '.format(Ab_color, ab_color)
	description += 'Gene 2 when dominant expresses an enzyme that creates the {0} pigment from the {1} precursor pigment. '.format(aB_color, ab_color)
	description += 'When both genes are dominant, the two enzymes pathways combine to form the new {0} pigment. '.format(AB_color)
	description += 'If neither of the genes are dominant, then there is no pigment change and the {0} precursor pigment remains. '.format(ab_color)
	return description


#===================
#===================
def recessive_epistasis(color_set):
	# Three colors
	#1: '9:3:4',
	AB_color_raw = color_set[0]
	Ab_color_raw = color_set[1]
	#aB_color_raw = color_set[2]
	ab_color_raw = color_set[3]
	AB_color = hybridcrosslib.color_translate.get(AB_color_raw, AB_color_raw)
	Ab_color = hybridcrosslib.color_translate.get(Ab_color_raw, Ab_color_raw)
	#aB_color = hybridcrosslib.color_translate.get(aB_color_raw, aB_color_raw)
	ab_color = hybridcrosslib.color_translate.get(ab_color_raw, ab_color_raw)

	table = '<table border="0" style="border: 0px solid white; border-collapse: collapse; ">'
	for i in range(5):
		table += '<colgroup width="60"></colgroup> '
	table += '<tr>'
	table += ' <td></td>'
	table += ' <td align="center">Gene 1</td>'
	table += ' <td></td>'
	table += ' <td align="center">Gene 2</td>'
	table += '</tr>'
	table += '<tr>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(ab_color_raw, ab_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(Ab_color_raw, Ab_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(AB_color_raw, AB_color)
	table += '</tr>'
	table += '</table>'

	#assigned_colors = hybridcrosslib.dihybridAssignColors(1, color_set)
	#print(hybridcrosslib.createDiHybridTable('A', 'B', assigned_colors, 'recessive epistasis'))

	description = table+'<br/>'
	description += 'A two step metabolic pathway determines the pigment color. '
	description += 'When gene 1 is dominant, the gene expresses an enzyme that converts the {0} precursor pigment into the {1} pigment. '.format(ab_color, Ab_color)
	description += 'When gene 1 is homozygous recessive, there is no pigment change and the {0} precursor pigment remains. '.format(ab_color)
	description += 'Gene 2 only has an effect on the pigment when gene 1 is dominant. '
	description += 'When gene 2 is dominant, the gene expresses an enzyme that converts the {0} pigment into the {1} pigment. '.format(Ab_color, AB_color)
	return description

#===================
#===================
def dominant_epistasis(color_set):
	# Three colors
	#2: '12:3:1',
	AB_color_raw = color_set[0]
	Ab_color_raw = color_set[1]
	#aB_color_raw = color_set[2]
	ab_color_raw = color_set[3]
	AB_color = hybridcrosslib.color_translate.get(AB_color_raw, AB_color_raw)
	Ab_color = hybridcrosslib.color_translate.get(Ab_color_raw, Ab_color_raw)
	#aB_color = hybridcrosslib.color_translate.get(aB_color_raw, aB_color_raw)
	ab_color = hybridcrosslib.color_translate.get(ab_color_raw, ab_color_raw)

	table = '<table border="0" style="border: 0px solid white; border-collapse: collapse; ">'
	for i in range(5):
		table += '<colgroup width="60"></colgroup> '
	table += '<tr><td rowspan="2"></td><td align="center">Gene 1</td><td rowspan="2"></td></tr>'
	table += '<tr>'
	table += ' <td align="center">{0}&darr;{0}</td> '.format(red_x)
	table += ' <td align="center">Gene 2</td>'
	table += '</tr>'
	table += '<tr>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(AB_color_raw, AB_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(ab_color_raw, ab_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(Ab_color_raw, Ab_color)
	table += '</tr>'
	table += '</table>'

	#assigned_colors = hybridcrosslib.dihybridAssignColors(2, color_set)
	#print(hybridcrosslib.createDiHybridTable('A', 'B', assigned_colors, 'dominant epistasis'))

	description = table + '<br/>\n'
	description += (
		'A two step metabolic pathway determines the pigment color.<li> '
	)
	description += (
		f'<ul>When gene 1 is dominant, the gene expresses an enzyme that '
		f'inhibits another enzyme that converts the {AB_color} precursor '
		f'pigment into the {ab_color} pigment.</ul> '
	)
	description += (
		f'<ul>When gene 2 is dominant, the gene expresses an enzyme that '
		f'converts the {ab_color} pigment into the {Ab_color} pigment.</ul> '
	)
	description += (
		f'<ul>When both genes are dominant, the dominant allele of gene 1 '
		f'inhibits the production of the {ab_color} color, so it will remain '
		f'the {AB_color} precursor color.</ul> '
	)
	description += (
		f'<ul>When both of the genes are homozygous recessive, then the first '
		f'enzyme is active (not inhibited) and the {AB_color} precursor '
		f'pigment is converted to the {ab_color} pigment and it will remain '
		'the final pigment, as the second enzyme is inactive.</ul></li> '
	)
	return description

#===================
#===================
def duplicate_recessive_epistasis(color_set):
	# Two colors
	#3: '9:7',
	AB_color_raw = color_set[0]
	#Ab_color_raw = color_set[1]
	#aB_color_raw = color_set[2]
	ab_color_raw = color_set[3]
	AB_color = hybridcrosslib.color_translate.get(AB_color_raw, AB_color_raw)
	#Ab_color = hybridcrosslib.color_translate.get(Ab_color_raw, Ab_color_raw)
	#aB_color = hybridcrosslib.color_translate.get(aB_color_raw, aB_color_raw)
	ab_color = hybridcrosslib.color_translate.get(ab_color_raw, ab_color_raw)

	table = '<table border="0" style="border: 0px solid white; border-collapse: collapse; ">'
	for i in range(5):
		table += '<colgroup width="60"></colgroup> '
	table += '<tr>'
	table += ' <td></td>'
	table += ' <td align="center">Gene 1</td>'
	table += ' <td></td>'
	table += ' <td align="center">Gene 2</td>'
	table += '</tr>'
	table += '<tr>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(ab_color_raw, ab_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(ab_color_raw, ab_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(AB_color_raw, AB_color)
	table += '</tr>'
	table += '</table>'

	#assigned_colors = hybridcrosslib.dihybridAssignColors(3, color_set)
	#print(hybridcrosslib.createDiHybridTable('A', 'B', assigned_colors, 'duplicate recessive epistasis'))

	description = table+'<br/>'
	description += 'A two step metabolic pathway determines the pigment color. '
	description += 'When gene 1 is dominant, the gene expresses an enzyme that converts the {0} precursor pigment into a a second molecule with the same {0} pigment. '.format(ab_color)
	description += 'When gene 2 is dominant, the gene expresses an enzyme that converts the second {0} pigment molecule from gene 1 into the {1} pigment. '.format(ab_color, AB_color)
	description += 'The {0} pigment forms only when both genes are dominant, if either gene is homozygous recessive, the {1} pigment will remain. '.format(AB_color, ab_color)
	return description

#===================
#===================
def duplicate_interaction_epistasis(color_set):
	# Three colors
	#4: '9:6:1',
	AB_color_raw = color_set[0]
	Ab_color_raw = color_set[1]
	#aB_color_raw = color_set[2]
	ab_color_raw = color_set[3]
	AB_color = hybridcrosslib.color_translate.get(AB_color_raw, AB_color_raw)
	Ab_color = hybridcrosslib.color_translate.get(Ab_color_raw, Ab_color_raw)
	#aB_color = hybridcrosslib.color_translate.get(aB_color_raw, aB_color_raw)
	ab_color = hybridcrosslib.color_translate.get(ab_color_raw, ab_color_raw)

	table = '<table border="0" style="border: 0px solid white; border-collapse: collapse; ">'
	table += '<tr>'
	table += ' <td style="border: 1px solid black; vertical-align: bottom;" align="center">'

	table += '<table border="0" style="border: 0px solid white; border-collapse: collapse; ">'
	for i in range(3):
		table += '<colgroup width="60"></colgroup> '
	table += '<tr><td></td><td align="center">Gene 1</td></tr>'
	table += '<tr>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(ab_color_raw, ab_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(Ab_color_raw, Ab_color)
	table += '</tr>'
	table += '</table>'
	table += '<b>Only Gene 1 Dominant</b>'

	table += '</td><td style="border: 1px solid black; vertical-align: bottom;" align="center">'

	table += '<table border="0" style="border: 0px solid white; border-collapse: collapse; ">'
	for i in range(3):
		table += '<colgroup width="60"></colgroup> '
	table += '<tr><td></td><td align="center">Gene 2</td></tr>'
	table += '<tr>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(ab_color_raw, ab_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(Ab_color_raw, Ab_color)
	table += '</tr>'
	table += '</table>'
	table += '<b>Only Gene 2 Dominant</b>'

	table += '</td><td style="border: 1px solid black; vertical-align: bottom;" align="center">'

	table += '<table border="0" style="border: 0px solid white; border-collapse: collapse; ">'
	for i in range(3):
		table += '<colgroup width="60"></colgroup> '
	table += '<tr><td></td><td align="center">Genes 1&plus;2</td></tr>'
	table += '<tr>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(ab_color_raw, ab_color)
	table += ' <td align="center">&xrarr;&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(AB_color_raw, AB_color)
	table += '</tr>'
	table += '</table>'
	table += '<b>Both Genes Dominant</b>'

	table += '</td></tr>'
	table += '</table>'

	#assigned_colors = hybridcrosslib.dihybridAssignColors(4, color_set)
	#print(hybridcrosslib.createDiHybridTable('A', 'B', assigned_colors, 'duplicate interaction epistasis'))

	#Complete dominance at both gene pairs; however, when either gene is dominant, it hides the effects of the other gene
	#Certain phenotypic traits depend on the dominant alleles of two gene loci. When dominant is present it will show its phenotype. The ratio will be 9: 6: 1.

	description = table+'<br/>'
	description += 'Both Gene 1 and Gene 2 when dominant express an enzyme that convert the {0} precursor pigment into the {1} pigment. '.format(ab_color, Ab_color)
	description += 'When both genes are dominant, the two enzymes combine to form the new {0} pigment. '.format(AB_color)
	description += 'If neither of the genes are dominant, then there is no pigment change and only the {0} precursor pigment remains. '.format(ab_color)
	return description



#===================
#===================
def duplicate_dominant_epistasis(color_set):
	# Two colors
	#5: '15:1',
	AB_color_raw = color_set[0]
	#Ab_color_raw = color_set[1]
	#aB_color_raw = color_set[2]
	ab_color_raw = color_set[3]
	AB_color = hybridcrosslib.color_translate.get(AB_color_raw, AB_color_raw)
	#Ab_color = hybridcrosslib.color_translate.get(Ab_color_raw, Ab_color_raw)
	#aB_color = hybridcrosslib.color_translate.get(aB_color_raw, aB_color_raw)
	ab_color = hybridcrosslib.color_translate.get(ab_color_raw, ab_color_raw)

	table = '<table border="0" style="border: 0px solid white; border-collapse: collapse; ">'
	for i in range(3):
		table += '<colgroup width="60"></colgroup> '
	table += '<tr><td></td><td align="center">Gene 1</td><td></td></tr>'
	#table += '<tr><td></td><td align="center">&darr;</td></tr>'
	table += '<tr>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(ab_color_raw,ab_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(AB_color_raw,AB_color)
	table += '</tr>'
	#table += '<tr><td></td><td align="center">&uarr;</td><<td rowspan="2"></td></tr>'
	table += '<tr><td></td><td align="center">Gene 2</td></tr>'
	table += '</table>'

	#assigned_colors = hybridcrosslib.dihybridAssignColors(5, color_set)
	#print(hybridcrosslib.createDiHybridTable('A', 'B', assigned_colors, 'duplicate dominant epistasis'))

	description = table+'<br/>'
	description += 'When either gene 1 or gene 2 is dominant, they express an enzyme that converts the {0} precursor pigment into the {1} pigment. '.format(ab_color, AB_color)
	description += 'If both gene 1 and gene 2 are homozygous recessive, then only the {0} precursor pigment is present'.format(ab_color)
	return description

#===================
#===================
def dominant_and_recessive_epistasis(color_set):
	# Two colors
	#6: '13:3',
	AB_color_raw = color_set[0]
	#Ab_color_raw = color_set[1]
	#aB_color_raw = color_set[2]
	ab_color_raw = color_set[3]
	AB_color = hybridcrosslib.color_translate.get(AB_color_raw, AB_color_raw)
	#Ab_color = hybridcrosslib.color_translate.get(Ab_color_raw, Ab_color_raw)
	#aB_color = hybridcrosslib.color_translate.get(aB_color_raw, aB_color_raw)
	ab_color = hybridcrosslib.color_translate.get(ab_color_raw, ab_color_raw)

	table = '<table border="0" style="border: 0px solid white; border-collapse: collapse; ">'
	for i in range(3):
		table += '<colgroup width="60"></colgroup> '
	table += '<tr><td rowspan="3"></td><td align="center">Gene 1</td></tr>'
	table += '<tr><td align="center">{0}&darr;{0}</td></tr>'.format(red_x)
	table += '<tr><td align="center">Gene 2</td></tr>'
	table += '<tr>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(AB_color_raw,AB_color)
	table += ' <td align="center">&xrarr;</td>'
	table += ' <td align="center" style="background-color: {0}">{1}</td>'.format(ab_color_raw,ab_color)
	table += '</tr>'
	table += '</table>'

	#assigned_colors = hybridcrosslib.dihybridAssignColors(6, color_set)
	#print(hybridcrosslib.createDiHybridTable('A', 'B', assigned_colors, 'dominant and recessive epistasis'))

	description = table+'<br/>'
	description += 'When gene 2 is dominant and gene 1 is homozygous recessive, '
	description += 'gene 2 expresses an active enzyme that converts the {0} precursor pigment into the {1} pigment. '.format(AB_color, ab_color)
	description += 'Whenever gene 1 is dominant, then gene 1 expresses a protein that completely suppresses the activity of gene 2. '
	description += 'When both genes are dominant, the inhibited gene 2 is unable to produce the {0} pigment, so the {1} precursor pigment remains. '.format(ab_color, AB_color)
	description += 'If neither of the genes are dominant, then there is no active enzyme and again only the {0} precursor pigment remains. '.format(AB_color)

	return description

#===================
#===================
#===================
#===================
def questionContent(gene_id):
	question = '<br/>'
	question += '<p>The diagram and description above explain the interaction of two genes. '
	question += ' <b>Determine the dihybird cross phenotypic ratio.</b></p>'
	#print(question)
	return question

#===================
#===================
def makeQuestion(gene_id, color_set):

	method = method_list[gene_id]
	header = method(color_set)

	# write the question content
	question_content = questionContent(gene_id)

	question_text = header
	question_text += " <br/> "
	question_text += question_content

	return question_text

#============================================
def gene_id_to_choice_html(gene_id: int, color_set: list, two_letters: list) -> str:
	"""
	Build a formatted HTML choice block for a gene interaction.

	Returns:
		str: HTML block containing the label text and the dihybrid table.
	"""
	name = hybridcrosslib.gene_interaction_names_plus[gene_id]
	ratio = hybridcrosslib.gene_type_ratios[gene_id]

	assigned_colors = hybridcrosslib.dihybridAssignColorsModified(gene_id, color_set)

	data_table = hybridcrosslib.createDiHybridTable(
		two_letters[0], two_letters[1], assigned_colors, name
	)

	choice_html = (
		f"<p>These two genes would show {name} and a "
		f"<b>{ratio} ratio</b>.</p> {data_table}"
	)
	return choice_html

#===================
#===================
def build_question(N: int, answer_gene_id: str, color_set: list, num_choices: int) -> str:
	"""
	Creates a formatted MC question about gene interaction types.
	"""
	# Select and sort two gene letters for use in question table
	letter_pool = copy.copy(hybridcrosslib.gene_letters)
	random.shuffle(letter_pool)
	two_letters = sorted([letter_pool.pop(), letter_pool.pop()])

	# Build the main question text for the Blackboard item, based on the correct gene interaction
	question_text = makeQuestion(answer_gene_id, color_set)

	# Get the number of phenotype colors produced by the correct gene interaction
	num_colors = hybridcrosslib.gene_type_num_colors[answer_gene_id]

	# Mapping of extended gene interaction type IDs (0–10) including hypothetical/fake types for distractors
	# Create a list of *all* possible gene interaction IDs
	all_plus_gene_ids = list(hybridcrosslib.gene_interaction_names_plus.keys())

	all_plus_gene_ids.remove(answer_gene_id)

	# Special case: if the correct answer is ID 1, remove ID 10 because they are equivalent/redundant
	if answer_gene_id == 1:
		all_plus_gene_ids.remove(10)

	# Start an empty list of "wrong" gene IDs (distractors)
	wrong_gene_ids = []

	# Collect plausible distractors
	for sub_gene_id in all_plus_gene_ids:
		if hybridcrosslib.gene_type_num_colors[sub_gene_id] == num_colors:
			wrong_gene_ids.append(sub_gene_id)

	# Trim excess distractors if needed
	wrong_gene_ids = wrong_gene_ids[:num_choices - 1]

	# Fill up with random if too short
	while len(wrong_gene_ids) < (num_choices - 1):
		wrong_gene_ids.append(random.choice(all_plus_gene_ids))
		wrong_gene_ids = list(set(wrong_gene_ids))

	# Build answer and choices
	answer_text = gene_id_to_choice_html(answer_gene_id, color_set, two_letters)
	wrong_gene_ids.append(answer_gene_id)

	choices_list = []
	for sub_gene_id in wrong_gene_ids:
		choice_text = gene_id_to_choice_html(sub_gene_id, color_set, two_letters)
		choices_list.append(choice_text)

	random.shuffle(choices_list)
	complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)

	return complete_question


#===================
method_list = [
	digenic_inheritance,
	recessive_epistasis,
	dominant_epistasis,
	duplicate_recessive_epistasis,
	duplicate_interaction_epistasis,
	duplicate_dominant_epistasis,
	dominant_and_recessive_epistasis,
]

all_gene_ids = list(hybridcrosslib.gene_interaction_names.keys())
all_color_sets = hybridcrosslib.get_four_color_sets()

#===========================================================
#===========================================================
def write_question(N: int, args) -> str:
	"""
	Create a single epistatic gene interaction question.
	"""
	gene_id = all_gene_ids[(N - 1) % len(all_gene_ids)]
	color_set = random.choice(all_color_sets)
	complete_question = build_question(N, gene_id, color_set, args.num_choices)
	return complete_question


#===========================================================
#===========================================================
# This function handles the parsing of command-line arguments.
def parse_arguments():
	"""
	Parses command-line arguments for the script.
	"""
	parser = bptools.make_arg_parser(description="Generate epistatic gene interaction questions.")
	parser = bptools.add_choice_args(parser, default=4)
	args = parser.parse_args()
	return args

#===================
#===================
#===================
#===================
def old_function():
	duplicates = 1
	outfile = bptools.make_outfile()
	print('writing to file: '+outfile)
	file_handle = open(outfile, 'w')
	N = 0
	for i in range(duplicates):
		for color_set in hybridcrosslib.get_four_color_sets():
			for gene_id in hybridcrosslib.gene_interaction_names:
				N += 1
				complete_bb_question = build_question(N, gene_id, color_set, 4)
				file_handle.write(complete_bb_question)
	file_handle.close()

#===========================================================
#===========================================================
# This function serves as the entry point for generating and saving questions.
def main():
	# Parse arguments from the command line
	args = parse_arguments()

	outfile = bptools.make_outfile(f"{args.num_choices}_choices")
	bptools.collect_and_write_questions(write_question, args, outfile)

#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END
