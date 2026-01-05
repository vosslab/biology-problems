#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
import random

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
def get_possible_child_phenotypes(mom_pheno: str, dad_pheno: str) -> list[str]:
	"""
	Given phenotypes of the parents, compute possible blood types of their children.

	Args:
		mom_pheno (str): Mother's phenotype.
		dad_pheno (str): Father's phenotype.

	Returns:
		list[str]: Possible child phenotypes.
	"""
	geno1 = pmap[mom_pheno]
	geno2 = pmap[dad_pheno]
	phenos = set()
	for allele1 in geno1:
		for allele2 in geno2:
			child_geno = allele1 + allele2
			phenos.add(gmap[child_geno])
	return sorted(list(phenos))

#===========================================================
def build_question(N: int, mom_pheno: str, dad_pheno: str) -> str:
	"""
	Creates a complete formatted multiple-answer question string.

	Args:
		N (int): Question number.
		mom_pheno (str): Mother's blood type.
		dad_pheno (str): Father's blood type.

	Returns:
		str: Formatted question string.
	"""
	question_text = ""
	question_text += (
		"<p>For the ABO blood group in humans, the i<sup>A</sup> and i<sup>B</sup> alleles are codominant "
		"and the i allele is recessive.</p>"
	)
	question_text += (
		f"<p>If a female &female; with <u>type {mom_pheno} blood</u> marries a male &male; with "
		f"<u>type {dad_pheno} blood</u>, which of the following blood types could their children possibly have? "
		"Check all that apply.</p>"
	)

	choices_list = [f"Type {p} blood" for p in phenotypes]
	correct_phenos = get_possible_child_phenotypes(mom_pheno, dad_pheno)
	answer_list = [f"Type {p} blood" for p in correct_phenos]

	#print(choices_list, answer_list)

	question = bptools.formatBB_MA_Question(N, question_text, choices_list, answer_list,
						min_answers_required=1, allow_all_correct=True)
	return question

#===========================================================
def write_question(N: int, args) -> str:
	mom_pheno = random.choice(phenotypes)
	dad_pheno = random.choice(phenotypes)
	return build_question(N, mom_pheno, dad_pheno)

#===========================================================
def parse_arguments():
	"""
	Parse command-line arguments.
	"""
	parser = bptools.make_arg_parser(description="Generate ABO blood type offspring questions.")
	args = parser.parse_args()
	return args

#===========================================================
def main():
	"""
	Generates all combinations of mother/father blood types as multiple-answer questions.
	"""
	args = parse_arguments()
	outfile = bptools.make_outfile(None)
	bptools.collect_and_write_questions(write_question, args, outfile)

#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	main()

## THE END
