#!/usr/bin/env python3

import random

import bptools
import translocationlib

debug = False

def questionText(chromosome1, chromosome2):
	question = ''
	question += '<p>An individual has a Robertsonian translocation involving chromosomes '
	question += f'{chromosome1} and {chromosome2}.</p>'
	question += '<h5>Which one of the following gametes was formed by '
	question += '<span style="color: darkred;">alternate</span> segregation in this individual?</h5>'
	return question

def blackboardFormat(N: int, chromosome1: int, chromosome2: int) -> object:
	question_string = questionText(chromosome1, chromosome2)
	table1 = ''
	#A. rob(14; 21)
	#B. rob(14; 21), +14
	#C. rob(14; 21), +21
	#D. -14
	#E. -21

	if random.random() < 0.5:
		color1 = 'deepskyblue'
		color2 = 'coral'
	else:
		color1 = 'coral'
		color2 = 'deepskyblue'

	table1  = translocationlib.draw_robertsonian_single_chromosome(chromosome1, color1)
	table2  = translocationlib.draw_robertsonian_single_chromosome(chromosome2, color2)
	table12 = translocationlib.draw_robertsonian_chromosome(chromosome1, chromosome2, color1, color2)
	#print(table1+table2+table12)
	table_merge = translocationlib.merge_tables([table1, table2, table12])
	question_string += table_merge
	question_string += '<p>all of three of the chromosomes in a somatic cell are shown above.</p><p></p>'

	choices = []

	answer = translocationlib.format_gamete_choice(
		f'rob({chromosome1}; {chromosome2})', [table12])
	choices.append(answer)

	wrong = translocationlib.format_gamete_choice(
		f'rob({chromosome1}; {chromosome2}), +{chromosome1}', [table12, table1])
	choices.append(wrong)

	wrong = translocationlib.format_gamete_choice(
		f'rob({chromosome1}; {chromosome2}), +{chromosome2}', [table12, table2])
	choices.append(wrong)

	wrong = translocationlib.format_gamete_choice(f'&ndash;{chromosome1}', [table2])
	choices.append(wrong)

	wrong = translocationlib.format_gamete_choice(f'&ndash;{chromosome2}', [table1])
	choices.append(wrong)

	random.shuffle(choices)
	blackboard = bptools.formatBB_MC_Question(N, question_string, choices, answer)

	return blackboard

def write_question(N: int, args) -> str:
	acrocentric_chromosomes = translocationlib.ACROCENTRIC_CHROMOSOMES
	pairs = []
	for i, chromosome1 in enumerate(acrocentric_chromosomes):
		for chromosome2 in acrocentric_chromosomes[i+1:]:
			pairs.append((chromosome1, chromosome2))
	chromosome1, chromosome2 = random.choice(pairs)
	return blackboardFormat(N, chromosome1, chromosome2)

def parse_arguments():
	parser = bptools.make_arg_parser(
		description="Generate Robertsonian translocation questions.",
	)
	args = parser.parse_args()
	return args

def main():
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)

if __name__ == "__main__":
	main()
