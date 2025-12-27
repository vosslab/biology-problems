#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules

# Import external modules (pip-installed)
# No external modules are used here currently

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities
import bptools
import genotypelib

# Function to write a question based on the genotype
def write_question(N, args):
	# Initialize the question string
	question = ""

	# Add contextual information and the actual question text
	question += '<h3>Gamete Diversity in Sexual Reproduction</h3>'
	question += '<p>In sexual reproduction, the potential diversity of gametes &ndash; such as '
	question += 'sperm and eggs in animals, or pollen and ovules in plants &ndash; can be calculated '
	question += 'based on the genotype of an individual.</p>'

	# Add the main question
	question += '<p>How many unique <span style="color: Green;"><strong>GAMETES</strong></span> could be produced'
	question += ' through the process of independent assortment by '
	question += ' an individual with the following genotype?</p> '

	# If hint is True, add a hint
	if args.hint:
		question += '<p><i>Hint: Remember, each heterozygous gene pair (like `Aa` or `Bb`)'
		question += ' can give rise to two (2) different gametes,'
		question += ' while homozygous pairs (like `AA`, `BB`, and `aa`, `bb`)'
		question += ' can only give rise to one gamete.</i></p>'

	# Calculate the gamete count; ensure it falls within specified range
	gamete_count = 1
	while gamete_count < 4 or gamete_count > 32:
		genotype_code, gamete_count = genotypelib.createGenotype(args.num_genes)

	# Add genotype to the question
	question += '<p><strong>Genotype:</strong>&nbsp;'
	question += genotypelib.genotype_code_format_text(genotype_code)
	question += '</p>'

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
	# Add shared argument bundles
	parser = bptools.add_base_args(parser)
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
