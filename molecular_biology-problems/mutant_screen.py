#!/usr/bin/env python3

import copy
import random

import bptools

def html_print(ordered, metabolites, classes):
	htmltext = ""

	tdopen = '<td align="center" valign="middle">'
	width = 60 * (len(ordered) + 1)
	htmltext += ('<table width="{0:d}px" cellpadding="2" cellspacing="2" style="text-align:center; border: 1px solid black; font-size: 14px;">'.format(width))
	htmltext += ('<tr><td></td>')
	for molecule in ordered:
		htmltext += ('{0}{1}</td>'.format(tdopen, molecule))
	htmltext += ('</tr>')
	for i in range(len(classes)):
		htmltext += ('<tr>')
		alive = False
		htmltext += ('{0}Class {1:d}</td>'.format(tdopen, i+1))
		happylist = {}
		happymeta = classes[i]
		for m in metabolites:
			if m == happymeta:
				alive = True
			happylist[m] = alive
		for m in ordered:
			if happylist[m] is True:
				htmltext += ('{0}+</td>'.format(tdopen))
			else:
				htmltext += ('{0}&ndash;</td>'.format(tdopen))
		htmltext += ('</tr>')
	htmltext += ('</table>')
	return htmltext

def build_scenario(num_metabolites: int) -> tuple[list[str], list[str], list[str], dict]:
	charlist = "ABCDEGHJKMPQRSTWXYZ"
	ordered = list(charlist[-num_metabolites:])
	metabolites = copy.copy(ordered)
	random.shuffle(metabolites)
	classes = copy.copy(ordered)
	random.shuffle(classes)
	class_count = {}
	for i in range(len(classes)):
		alive = False
		happylist = {}
		happymeta = classes[i]
		for m in metabolites:
			if m == happymeta:
				alive = True
			happylist[m] = alive
		for m in ordered:
			if happylist[m] is True:
				class_count[i+1] = class_count.get(i+1, 0) + 1
	return ordered, metabolites, classes, class_count

#===========================================================
def build_question_text(ordered, metabolites, classes):
	metabolic_text = "&nbsp;({0}-{1})".format(ordered[0], ordered[-1])
	question_text = "<p>A mutant screen was carried out to produce the diagram below. "
	question_text += ("The diagram shows different classes&nbsp;(1-{0}) of mutants for metabolic "
		"precursors{1} of a metabolic pathway to produce a product were characterized to either "
		"grow&nbsp;(+) or not grow&nbsp;(&ndash;) in minimal media.").format(len(ordered), metabolic_text)
	question_text += '</p>'
	question_text += html_print(ordered, metabolites, classes)
	return question_text, metabolic_text

#===========================================================
def write_question(N: int, args) -> str:
	ordered, metabolites, classes, class_count = build_scenario(args.num_metabolites)
	question_text, metabolic_text = build_question_text(ordered, metabolites, classes)
	answer = "".join(metabolites)

	if args.question_format == 'fib':
		example_text = answer
		while example_text == answer:
			example = copy.copy(ordered)
			random.shuffle(example)
			example_text = "".join(example)
		question_text += ("<h6>Write the metabolic precursors{0} in their correct order for the "
			"pathway without spaces or dashes. For example, {1}.</h6>").format(metabolic_text, example_text)
		return bptools.formatBB_FIB_Question(N, question_text, [answer])

	question_text += "<h6>Which one of the following classes is the <i>wild-type</i> organism?</h6>"
	choices_list = []
	answer_text = None
	for i in range(len(classes)):
		choice_text = "Class {0:d}".format(i + 1)
		choices_list.append(choice_text)
		if class_count.get(i + 1, 0) == len(classes):
			answer_text = choice_text
	if answer_text is None:
		return None
	return bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)

#===========================================================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate mutant screen pathway questions.")
	parser.add_argument(
		'-n', '--num-metabolites', dest='num_metabolites', type=int,
		default=4, help='Number of metabolites in the pathway.'
	)
	parser = bptools.add_question_format_args(
		parser,
		types_list=['fib', 'mc'],
		required=False,
		default='fib'
	)
	args = parser.parse_args()
	return args

#===========================================================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile(None, f"{args.question_format}", f"{args.num_metabolites}_metabolites")
	bptools.collect_and_write_questions(write_question, args, outfile)

#===========================================================
if __name__ == '__main__':
	main()

