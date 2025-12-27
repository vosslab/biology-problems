#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
# Provides functions to generate random numbers and selections
import random

# Import external modules (pip-installed)
# No external modules are used here currently

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities
import bptools

#===========================================================
phenotypes = ['O', 'A', 'B', 'AB']
alleles = ['O', 'A', 'B']
pmap = {
	'O': 'OO',
	'A': 'AO',
	'B': 'BO',
	'AB': 'AB',
}
pmaplist = {
	'O': ['OO'],
	'A': ['AO', 'AA'],
	'B': ['BO', 'BB'],
	'AB': ['AB'],
}
gmap = {
	'OO': 'O',
	'AO': 'A',
	'OA': 'A',
	'AA': 'A',
	'BO': 'B',
	'OB': 'B',
	'BB': 'B',
	'AB': 'AB',
	'BA': 'AB',
}


#===========================================================
def get_possible_mom_genotypes(dad_geno: str, kid_geno: str) -> set[str]:
	"""
	Find all possible maternal genotypes consistent with given father and child genotypes.

	Args:
		dad_geno (str): Genotype of the father (e.g., 'AO').
		kid_geno (str): Genotype of the child (e.g., 'AB').

	Returns:
		set[str]: Set of maternal genotypes that could explain the child's genotype.
	"""
	answers = set()
	kid_list = list(kid_geno)

	for dad_allele in dad_geno:
		if dad_allele in kid_list:
			kid_list.remove(dad_allele)

	if len(kid_list) == 2:
		return set()

	required = kid_list[0] if len(kid_list) == 1 else None

	for dad_allele in dad_geno:
		kid_list = list(kid_geno)
		if dad_allele not in kid_list:
			continue
		kid_list.remove(dad_allele)

		if required and kid_list[0] != required:
			continue

		kid_allele = kid_list[0]
		for mom_allele in alleles:
			geno = ''.join(sorted([mom_allele, kid_allele]))
			answers.add(geno)

	return answers

#===========================================================
def get_possible_mom_phenotypes(dad_pheno: str, kid_pheno: str) -> list[str]:
	"""
	Given phenotypes of dad and child, return list of valid maternal phenotypes.

	Args:
		dad_pheno (str): Blood type of the father.
		kid_pheno (str): Blood type of the child.

	Returns:
		list[str]: Valid maternal phenotypes (e.g., ['A', 'B'])
	"""
	possible_phenos = set()
	dad_genos = pmaplist[dad_pheno]
	kid_genos = pmaplist[kid_pheno]

	for dad_geno in dad_genos:
		for kid_geno in kid_genos:
			mom_genos = get_possible_mom_genotypes(dad_geno, kid_geno)
			for geno in mom_genos:
				pheno = gmap[geno]
				possible_phenos.add(pheno)

	return sorted(list(possible_phenos))

#===========================================================
def write_question(N: int, dad_pheno: str, kid_pheno: str) -> str:
	"""
	Generate a formatted multiple-answer question string.

	Args:
		N (int): Question number.
		dad_pheno (str): Blood type of the father.
		kid_pheno (str): Blood type of the child.

	Returns:
		str: Formatted question string.
	"""
	offspring = random.choice(('daughter &female;', 'son &male;'))

	question_text = ''
	question_text += (
		"<p>For the ABO blood group in humans, the i<sup>A</sup> and i<sup>B</sup> alleles are codominant "
		"and the i allele is recessive.</p>"
	)
	question_text += (
		f"<p>A father &male; with <u>blood type {dad_pheno}</u> has a {offspring} with "
		f"<u>blood type {kid_pheno}</u>.</p>"
	)
	question_text += (
		"<p>Which of the following blood types could the mother &female; possibly have? "
		"Check all that apply.</p>"
	)

	# Generate choices and correct answers
	choices_list = [f"Type {pheno} blood" for pheno in phenotypes]
	correct_phenos = get_possible_mom_phenotypes(dad_pheno, kid_pheno)
	answer_list = [f"Type {pheno} blood" for pheno in correct_phenos]

	# If no valid types, add "None of the above" as correct
	none_choice = (
		"None of the above are possible; the father &male; is not related to his " + offspring
	)
	if not answer_list:
		answer_list = [none_choice]
	choices_list.append(none_choice)

	# Format question using bptools
	question = bptools.formatBB_MA_Question(N, question_text, choices_list, answer_list, min_answers_required=1)
	return question


#===========================================================
def main():
	"""
	Generates all combinations of father/child blood types as multiple-answer questions.
	"""
	parser = bptools.make_arg_parser(
		description="Generate blood type mother questions.",
		batch=True
	)
	args = parser.parse_args()

	outfile = bptools.make_outfile(None)
	questions = bptools.collect_question_batches(write_question_batch, args)
	bptools.write_questions_to_file(questions, outfile)

#===========================================================
def write_question_batch(start_num: int, args) -> list:
	questions = []
	remaining = None
	if args.max_questions is not None:
		remaining = args.max_questions - (start_num - 1)
		if remaining <= 0:
			return questions
	N = start_num
	for dad_pheno in phenotypes:
		for kid_pheno in phenotypes:
			question = write_question(N, dad_pheno, kid_pheno)
			questions.append(question)
			N += 1
			if remaining is not None and len(questions) >= remaining:
				return questions
	return questions

#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END
