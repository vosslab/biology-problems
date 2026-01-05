#!/usr/bin/env python3

import random

import bptools
import translocationlib

debug = False

types = {
	1: 'adjacent-1',
	2: 'adjacent-2',
	3: 'alternate',
	4: 'alternate',
}

def get_question_statement(segregation_type_index: int, chromosome1: int, chromosome2: int) -> str:
	"""
	Generates a question statement for a genetic counseling scenario involving balanced translocations.
	"""
	segregation_type = types[segregation_type_index]
	question = (
		f'<p>A phenotypically <i>wildtype</i> prospective couple seeks genetic counseling. '
		f'The man has a <strong>balanced translocation</strong>, '
		f'between chromosomes {chromosome1} and {chromosome2}.'
		f'This means that  a segment of chromosome {chromosome1} '
		f'has been exchanged with a segment of chromosome {chromosome2} without any gain or loss of genetic material. '
		f'While balanced translocations typically do not affect the individual\'s phenotype, '
		f'they can result in different types of gametes during reproduction.</p>'
		f'<p><ul>'
		f'<li><strong>Chromosome Pair:</strong> {chromosome1}, {chromosome2}</li>'
		f'<li><strong>Segregation Type:</strong> {segregation_type}</li>'
		f'</ul></p>'
	)
	return question


def get_choices(N, segregation_type_index, chromosome1, chromosome2):

	table1 = ''

	table1  = translocationlib.draw_meiosis_chromosome(chromosome1, 'red')
	table2  = translocationlib.draw_meiosis_chromosome(chromosome2, 'blue')
	table12 = translocationlib.draw_translocated_chromosome(chromosome1, chromosome2, 'red', 'blue')
	table21 = translocationlib.draw_translocated_chromosome(chromosome2, chromosome1, 'blue', 'red')
	table_merge = translocationlib.merge_tables([table1, table2, table12, table21])
	#print(table1+table2+table12+table21)

	segregation_type = types[segregation_type_index]
	question_table = table_merge
	question_table += '<p>all four of the chromosomes present in a somatic cell are shown above</p><p></p>'
	question_table += (
		f'<p>Below are all the possible gametes produced by the man with the translocation.</p> '
		f'<p>Among the six choices below, only two (2) gametes or two (2) sets of chromosomes '
		f'are formed by <strong>{segregation_type}</strong> segregation.</p> '
		f'<p>Your task is to <strong>select the two (2) gametes produced by '
		f'{segregation_type}</strong> segregation.</p>'
	)
	question_table += '<p>CHECK TWO BOXES below!</p>'

	choices = []

	smtab = '<table style="border-collapse: collapse; border: 1px solid silver;">'
	trtd = '<tr><td style="border: 0px solid white;">'

	alternate1 = smtab + trtd + 't({0}; {1}), t({1}; {0})</td></tr>'.format(chromosome1, chromosome2)
	alternate1 += trtd + table12 + '</td></tr>'
	alternate1 += trtd + table21 + '</td></tr>'
	alternate1 += '</table><p></p><hr/><p></p>'
	choices.append(alternate1)

	alternate2 = smtab + trtd + '{0}, {1}</td></tr>'.format(chromosome1, chromosome2)
	alternate2 += trtd + table1 + '</td></tr>'
	alternate2 += trtd + table2 + '</td></tr>'
	alternate2 += '</table><p></p><hr/><p></p>'
	choices.append(alternate2)

	adjacent1a = smtab + trtd + 't({0}; {1}), +{1}</td></tr>'.format(chromosome1, chromosome2)
	adjacent1a += trtd + table12 + '</td></tr>'
	adjacent1a += trtd + table2 + '</td></tr>'
	adjacent1a += '</table><p></p><hr/><p></p>'
	choices.append(adjacent1a)

	adjacent1b = smtab + trtd + 't({1}; {0}), +{0}</td></tr>'.format(chromosome1, chromosome2)
	adjacent1b += trtd + table21 + '</td></tr>'
	adjacent1b += trtd + table1 + '</td></tr>'
	adjacent1b += '</table><p></p><hr/><p></p>'
	choices.append(adjacent1b)

	adjacent2a = smtab + trtd + 't({0}; {1}), +{0}</td></tr>'.format(chromosome1, chromosome2)
	adjacent2a += trtd + table12 + '</td></tr>'
	adjacent2a += trtd + table1 + '</td></tr>'
	adjacent2a += '</table><p></p><hr/><p></p>'
	choices.append(adjacent2a)

	adjacent2b = smtab + trtd + 't({1}; {0}), +{1}</td></tr>'.format(chromosome1, chromosome2)
	adjacent2b += trtd + table21 + '</td></tr>'
	adjacent2b += trtd + table2 + '</td></tr>'
	adjacent2b += '</table><p></p><hr/><p></p>'
	choices.append(adjacent2b)

	answers = []
	if segregation_type_index == 1:
		answers.append(adjacent1a)
		answers.append(adjacent1b)
	elif segregation_type_index == 2:
		answers.append(adjacent2a)
		answers.append(adjacent2b)
	elif segregation_type_index == 3 or segregation_type_index == 4:
		#happens twice as often
		answers.append(alternate1)
		answers.append(alternate2)
	else:
		raise ValueError

	random.shuffle(choices)

	return question_table, choices, answers

#======================================
#======================================
def write_question(N, args):
	segregation_type = random.randint(1,4)
	chromosome1 = random.randint(1, 22-1)
	chromosome2 = random.randint(chromosome1+1, 22)
	while chromosome1 >= chromosome2:
		chromosome1 = random.randint(1, 22-1)
		chromosome2 = random.randint(chromosome1+1, 22)
	print(f"selected chromosome pair: {chromosome1} and {chromosome2}")
	N += 1
	question_statement = get_question_statement(segregation_type, chromosome1, chromosome2)
	question_table, choices_list, answers_list = get_choices(N, segregation_type, chromosome1, chromosome2)
	question_statement = question_statement + question_table
	complete_question = bptools.formatBB_MA_Question(N, question_statement, choices_list, answers_list)

	return complete_question

#=====================
def parse_arguments():
	"""
	Parses command-line arguments for the script.

	Defines and handles all arguments for the script, including:
	- `duplicates`: The number of questions to generate.
	- `num_choices`: The number of answer choices for each question.
	- `question_type`: Type of question (numeric or multiple choice).

	Returns:
		argparse.Namespace: Parsed arguments with attributes `duplicates`,
		`num_choices`, and `question_type`.
	"""
	parser = bptools.make_arg_parser(description="Generate questions.")

	args = parser.parse_args()
	return args




#======================================
#======================================
def main():
	"""
	Main function that orchestrates question generation and file output.
	"""

	# Parse arguments from the command line
	args = parse_arguments()

	outfile = bptools.make_outfile(None)
	bptools.collect_and_write_questions(write_question, args, outfile)

#======================================
#======================================
if __name__ == '__main__':
	main()

## THE END
