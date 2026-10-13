#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
# Import external modules (pip-installed)
# No external modules are used here currently

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities
import random

import bptools


# genotypes are dominant first, because female / male are interchangable in this context
PUNNETT_CONTEXTS = [
	("AA x AA", "a cross of two different true-breeding purple flower plants?"),

	("AA x Aa", "a backcross between a true-breeding purple flower plant from the P generation and a purple F<sub>1</sub> hybrid plant?"),
	("AA x Aa", "a cross between a true-breeding purple-flowered plant and a purple hybrid from the F<sub>1</sub> generation?"),

	("AA x aa", "the first cross between the parental generation to produce the F<sub>1</sub> hybrids in a monohybrid cross?"),
	("AA x aa", "a cross between a true-breeding purple flower plant and a true-breeding white flower plant?"),
	("AA x aa", "a monohybrid cross between two true-breeding parents, one with purple dominant and one with white recessive phenotypes?"),

	("Aa x Aa", "the cross between the hybrids of the F<sub>1</sub> generation to produce the F<sub>2</sub> generation in a monohybrid cross?"),
	("Aa x Aa", "the cross between two different F<sub>1</sub> hybrid plants that have purple flowers?"),
	("Aa x Aa", "a cross between two purple-flowered plants, both from the F<sub>1</sub> generation?"),
	("Aa x Aa", "a mating between two F<sub>1</sub> hybrids that each came from true-breeding purple and white parents?"),

	("Aa x aa", "a backcross between a true-breeding white flower plant from the P generation and a purple F<sub>1</sub> hybrid plant?"),
	("Aa x aa", "a backcross between a purple F<sub>1</sub> hybrid plant and a true-breeding white flower plant?"),

	("aa x aa", "a cross of two different white flower plants of unknown genotype?"),
	("aa x aa", "a cross between two true-breeding white-flowered plants?"),
]

#===========================================================
#===========================================================
# This function generates and returns the main question text.
def get_question_text(N) -> tuple:
	"""
	Generates and returns the main text for the question.
	"""
	# Initialize an empty string for the question text
	# Shared Mendel intro
	MENDEL_INTRO = (
		"In his experiments, Mendel discovered that the purple flower phenotype "
		"was dominant to the white flower phenotype."
	)

	# Shared ending prompt
	PUNNETT_PROMPT = (
		"Which one of the following Punnett squares represents "
	)

	context_tuple = random.choice(PUNNETT_CONTEXTS)
	answer_genotypes_key = context_tuple[0]
	context = context_tuple[1]
	question_text = f"{MENDEL_INTRO}\n\n{PUNNETT_PROMPT}{context}"

	# Return the complete question text
	return question_text, answer_genotypes_key


#==========================
def get_cell_html(geno: str) -> str:
	"""
	Returns HTML <td> for a given genotype with color formatting.

	Args:
		geno (str): Genotype string (e.g., 'AA', 'Aa', 'aa').

	Returns:
		str: HTML string for one cell of the Punnett square.
	"""
	if geno == 'AA':
		return '<td align="center" bgcolor="black"><span style="color: #f8f8f8; font-family: monospace;">AA</span></td>'
	elif geno in ['Aa', 'aA']:
		return '<td align="center" bgcolor="#777"><span style="color: #f8f8f8; font-family: monospace;">Aa</span></td>'
	elif geno == 'aa':
		return '<td align="center" bgcolor="#CCC"><span style="color: #080808; font-family: monospace;">aa</span></td>'
	raise ValueError

#==========================
def make_punnett_square_html(female_geno: str, male_geno: str) -> str:
	"""
	Generates HTML table for a Punnett square given two parental genotypes.

	Args:
		female_geno (str): Genotype of the female parent (e.g., 'Aa').
		male_geno (str): Genotype of the male parent (e.g., 'Aa').

	Returns:
		str: HTML string representing the Punnett square.
	"""
	female_alleles = list(female_geno)
	male_alleles = list(male_geno)

	html = '<table border="1" cellpadding="4" cellspacing="0" style="margin: 2px; border-collapse: collapse;">'

	# Header row: male alleles
	html += '<tr><td></td>'
	for allele in male_alleles:
		html += f'<td align="center"><span style="font-family: monospace; font-weight: bold;">{allele}</span></td>'
	html += '</tr>'

	# Rows: female alleles
	for fa in female_alleles:
		html += f'<tr><td align="center"><span style="font-family: monospace; font-weight: bold;">{fa}</span></td>'
		for ma in male_alleles:
			child_geno = ''.join(sorted([fa, ma]))
			html += get_cell_html(child_geno)
		html += '</tr>'

	html += '</table><br/>'
	return html

#==========================
def generate_choices() -> str:
	"""
	Generates HTML for all 6 unique single-gene Punnett squares with color coding.

	Returns:
		str: Combined HTML for all Punnett squares in a flex container.
	"""
	genotype_pairs = [
		('AA', 'AA'),
		('AA', 'Aa'),
		('AA', 'aa'),
		('Aa', 'Aa'),
		('Aa', 'aa'),
		('aa', 'aa'),
	]

	all_punnett_squares_html_dict = {}

	for female, male in genotype_pairs:
		assert [female,male] == sorted([female,male])
		genotype_key = f"{female} x {male}"
		punnett_html = make_punnett_square_html(female, male)
		all_punnett_squares_html_dict[genotype_key] = punnett_html
	return all_punnett_squares_html_dict

_ALL_PUNNETT_SQUARES_HTML_DICT = None

#===========================================================
#===========================================================
# This function creates and formats a complete question for output.
def select_crosses(answer_key: str, num_choices: int) -> list[str]:
	"""Keep the closest parental-genotype errors, dropping the least plausible crosses."""
	if not 2 <= num_choices <= 6:
		raise ValueError('Punnett-square questions require 2 through 6 choices.')
	keys = sorted({context[0] for context in PUNNETT_CONTEXTS})
	# Confusing homozygous and heterozygous parents costs one allele change.
	# Reversing the parents is equivalent, so compare sorted allele counts.
	answer_counts = sorted(parent.count('A') for parent in answer_key.split(' x '))
	distractors = [key for key in keys if key != answer_key]
	random.shuffle(distractors)
	distractors.sort(key=lambda key: sum(
		abs(actual - wrong) for actual, wrong in zip(
			answer_counts, sorted(parent.count('A') for parent in key.split(' x '))
		)
	))
	selected = [answer_key] + distractors[:num_choices - 1]
	random.shuffle(selected)
	return selected


def _format_question(N: int, all_punnett_squares_html_dict: dict, num_choices: int) -> str:
	"""
	Creates a complete formatted question for output.

	Args:
		N (int): The question number, used for labeling the question.
		num_choices (int): The number of answer choices to include.

	Returns:
		str: A formatted question string containing the question text,
		answer choices, and the correct answer.
	"""
	# Generate the main question text
	question_text, answer_genotypes_key = get_question_text(N)

	# Generate answer choices and the correct answer
	keys = select_crosses(answer_genotypes_key, num_choices)
	choices_list = [all_punnett_squares_html_dict[key] for key in keys]
	answer_text = all_punnett_squares_html_dict[answer_genotypes_key]

	# Format the question using a helper function from the bptools module
	complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)

	# Return the formatted question string
	return complete_question

#===========================================================
#===========================================================
def write_question(N: int, args) -> str:
	global _ALL_PUNNETT_SQUARES_HTML_DICT
	if _ALL_PUNNETT_SQUARES_HTML_DICT is None:
		_ALL_PUNNETT_SQUARES_HTML_DICT = generate_choices()
	return _format_question(N, _ALL_PUNNETT_SQUARES_HTML_DICT, args.num_choices)

#===========================================================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate Punnett square questions.")
	bptools.add_choice_args(parser, default=6)
	args = parser.parse_args()
	if not 2 <= args.num_choices <= 6:
		parser.error('--num-choices must be between 2 and 6')
	return args

#===========================================================
def main():
	"""
	Main function that orchestrates question generation and file output.
	"""
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)

#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END
