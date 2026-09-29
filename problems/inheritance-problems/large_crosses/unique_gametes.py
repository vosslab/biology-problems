#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
import os
import sys

# Import external modules (pip-installed)
# No external modules are used here currently

# Extend sys.path so the sibling `genotypelib` module under inheritance-problems is importable
inheritance_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if inheritance_root not in sys.path:
	sys.path.insert(0, inheritance_root)

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities
import bptools
import genotypelib
import cross_table

# Function to write a question based on the genotype
def write_question(N, args):
	# Initialize the question string
	question = ""
	names = cross_table.choose_student_names(1)

	# Add contextual information and the actual question text
	question += '<h3>Gamete Diversity in Sexual Reproduction</h3>'
	question += '<p>Assume independent assortment for all genes.</p>'

	# Add the main question
	question += '<p>How many unique <span style="color: Green;"><strong>GAMETES</strong></span> could be produced'
	question += ' through the process of independent assortment by '
	question += f' {names[0]}, who has the following genotype?</p> '

	# If hint is True, add a hint
	if args.hint:
		question += '<p><i>Hint: At each gene, a heterozygous pair (Aa) provides two '
		question += 'possible alleles for a gamete; a homozygous pair (AA or aa) provides '
		question += 'one. Multiply the counts across all genes.</i></p>'

	# Calculate the gamete count; ensure it falls within specified range
	gamete_count = 1
	while gamete_count < 4 or gamete_count > 32:
		gene_list = genotypelib.createGenotypeList(args.num_genes)
		_, gamete_count = genotypelib.createGenotypeStringFromList(gene_list)

	# Add genotype to the question
	question += cross_table.work_table_instructions()
	question += cross_table.make_work_table(gene_list, names)

	# Create a list of answer choices
	choices_list = []
	for power in range(2, 7):
		value = 2**power
		choice = '2<sup>{0:d}</sup> = {1:d}'.format(power, value)
		if args.hint:
			choice += ' (i.e., {0} genes with two alternative forms each)'.format(bptools.number_to_cardinal(power))
		choices_list.append(choice)
		if value == gamete_count:
			answer = choice

	# Format the question using Blackboard-compatible markup
	bbformat = bptools.formatBB_MC_Question(N, question, choices_list, answer)
	return bbformat


#===========================================================
#===========================================================
def parse_arguments():
	parser = bptools.make_arg_parser()
	parser = bptools.add_hint_args(parser)
	# Add command line options for number of genes
	parser.add_argument('-n', '--num_genes', type=int, default=7, help='Number of genes')
	args = parser.parse_args()
	return args


#===========================================================
#===========================================================
def main():
	args = parse_arguments()
	hint_mode = 'with_hint' if args.hint else 'no_hint'
	outfile = bptools.make_outfile(hint_mode, f"{args.num_genes}_genes")
	bptools.collect_and_write_questions(write_question, args, outfile)

#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END
