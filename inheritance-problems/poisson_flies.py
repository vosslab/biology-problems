#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
# Provides functions for interacting with the operating system
import os
# Provides functions to generate random numbers and selections
import random
# Provides tools to parse command-line arguments
import argparse

# Import external modules (pip-installed)
# No external modules are used here currently

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities
import bptools

#===========================================================
#===========================================================
def geno2pheno(genotype):
	if genotype.startswith('+'):
		phenotype = "red"
	else:
		phenotype = "white"
	if '-' in genotype:
		phenotype += " male"
	else:
		phenotype += " female"
	return phenotype

#===========================================================
#===========================================================
def get_answer(female_genotype, male_genotype):
	if female_genotype == "++":
		return 0
	elif female_genotype == "+w":
		if male_genotype == "+-":
			return 1
		elif male_genotype == "w-":
			return 2
	elif female_genotype == "ww":
		if male_genotype == "+-":
			return 3
		elif male_genotype == "w-":
			return 4

#===========================================================
#===========================================================
def cross_experiment(female_genotype, male_genotype, progeny_size=400):
	distribution = {}
	for i in range(progeny_size):
		a = random.choice(list(female_genotype))
		b = random.choice(list(male_genotype))
		offspring = [a,b]
		offspring.sort()
		offspring_str = offspring[0]+offspring[1]
		distribution[offspring_str] = distribution.get(offspring_str, 0) + 1
	#sys.exit(1)
	return distribution

#===========================================================
#===========================================================
def print_distribution_string(distribution):
	keys = list(distribution.keys())
	keys.sort()
	pcount = {}
	for key in keys:
		phenotype = geno2pheno(key)
		pcount[phenotype] = pcount.get(phenotype,0) + distribution[key]

	pkeys = list(pcount.keys())
	pkeys.sort()
	mystr = ""
	for pkey in pkeys:
		mystr += "{0}: {1:d}, ".format(pkey, pcount[pkey])
	print(mystr)

#===========================================================
#===========================================================
def print_distribution_table(distribution):
	keys = list(distribution.keys())
	keys.sort()
	pcount = {}
	for key in keys:
		phenotype = geno2pheno(key)
		pcount[phenotype] = pcount.get(phenotype,0) + distribution[key]

	pkeys = list(pcount.keys())
	pkeys.sort()
	mystr = '<table cellpadding="2" cellspacing="2" style="border-collapse: collapse; text-align:center; border: 1px solid black; font-size: 14px;">'
	mystr += "<tr><th>phenotype</th><th>female &female;</th><th>male &male;</th></tr> "
	mystr += "<tr><td><span style='color: darkred;'>red-eyed (wildtype)</span></td> "
	mystr +=   f"<td align='center'>{pcount.get('red female', 0)}</td>"
	mystr +=   f"<td align='center'>{pcount.get('red male', 0)}</td></tr> "
	mystr += "<tr><td>white-eyed (mutant)</td> "
	mystr +=   f"<td align='center'>{pcount.get('white female', 0)}</td>"
	mystr +=   f"<td align='center'>{pcount.get('white male', 0)}</td></tr> "
	mystr += "</table><br/>"
	return mystr

#===========================================================
#===========================================================
def write_question(N, female_genotype, male_genotype, progeny_size):
	choices_list = [
		'homozygous wildtype female (++) and male of unknown genotype',
		'heterozygous female (+w) and wildtype male (+&ndash;)',
		'heterozygous female (+w) and mutant male (w&ndash;)',
		'homozygous mutant female (ww) and wildtype male (+&ndash;)',
		'homozygous mutant female (ww) and mutant male (w&ndash;)',
	]

	pre_question = "<p>The white-eyed phenotype is an X-linked recessive disorder in fruit flies. The red allele, +, is dominant to the white allele, w. The offspring of size {0} from the mating of a single female and a single male are shown in the table below:</p>".format(progeny_size)

	post_question = "<p><strong>What are the genotypes of the parents in this cross?</strong></p>"


	#print(female_genotype)
	#print(male_genotype)
	distribution = cross_experiment(female_genotype, male_genotype, progeny_size)
	answer_id = get_answer(female_genotype, male_genotype)
	answer_txt = choices_list[answer_id]

	bad_cross = False
	for key in distribution:
		if distribution[key] % 5 == 0:
			bad_cross = True
	if bad_cross is True:
		return None
	print_distribution_string(distribution)
	table = print_distribution_table(distribution)

	question_txt = pre_question + table + post_question

	random.shuffle(choices_list)
	bbformat = bptools.formatBB_MC_Question(N, question_txt, choices_list, answer_txt)
	return bbformat


def old_func():
	# Initialize argparse for command line arguments
	parser = argparse.ArgumentParser(description='Generate blackboard questions.')
	# Add command line options for number of genes and number of questions
	parser.add_argument('-x', '--num_questions', type=int, default=24, help='Number of questions')
	# Parse the command line arguments
	args = parser.parse_args()

	N = 0
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	female_genotype = random.choice(("++", "+w", "ww"))
	male_genotype = random.choice(("+-", "w-"))
	progeny_size_selection = (160, 200, 400, 600,)
	female_types = ("++", "+w", "ww")
	male_types = ("+-", "w-")
	for i in range(args.num_questions):
		progeny_size = random.choice(progeny_size_selection)
		female_genotype = random.choice(female_types)
		if female_genotype == '++':
			male_genotype = 'w-'
		else:
			male_genotype = random.choice(male_types)
		N += 1
		bbformat = make_question(N, female_genotype, male_genotype, progeny_size)
		if bbformat is not None:
			#only about 60-75% questions are not None
			f.write(bbformat)
	f.close()
	bptools.print_histogram()



#===========================================================
#===========================================================
# This function handles the parsing of command-line arguments.
def parse_arguments():
	"""
	Parses command-line arguments for the script.

	Returns:
		argparse.Namespace: Parsed arguments with attributes `duplicates`,
		`num_choices`, and `question_type`.
	"""
	# Create an argument parser with a description of the script's functionality
	parser = argparse.ArgumentParser(description="Generate questions.")

	# Add an argument to specify the number of duplicate questions to generate
	parser.add_argument(
		'-d', '--duplicates', metavar='#', type=int, dest='duplicates',
		help='Number of duplicate runs to do or number of questions to create',
		default=1
	)

	parser.add_argument(
		'-x', '--max-questions', type=int, dest='max_questions',
		default=99, help='Max number of questions'
	)

	# Parse the provided command-line arguments and return them
	args = parser.parse_args()
	return args

#===========================================================
#===========================================================
# This function serves as the entry point for generating and saving questions.
def main():
	"""
	Main function that orchestrates question generation and file output.

	Workflow:
	1. Parse command-line arguments.
	2. Generate the output filename using script name and args.
	3. Generate formatted questions using write_question().
	4. Shuffle and trim the list if exceeding max_questions.
	5. Write all formatted questions to output file.
	6. Print stats and status.
	"""

	# Parse arguments from the command line
	args = parse_arguments()

	# Generate the output file name based on the script name and arguments
	script_name = os.path.splitext(os.path.basename(__file__))[0]
	outfile = (
		'bbq'
		f'-{script_name}'              # Add the script name to the file name
		'-questions.txt'               # File extension
	)

	# Store all complete formatted questions
	question_bank_list = []

	# Initialize question counter
	N = 0

	female_genotype = random.choice(("++", "+w", "ww"))
	male_genotype = random.choice(("+-", "w-"))
	progeny_size_selection = (160, 200, 240, 320, 360, 400, 480, 600,)
	female_types = ("++", "+w", "ww")
	male_types = ("+-", "w-")

	# Create the specified number of questions
	for _ in range(args.duplicates):
		progeny_size = random.choice(progeny_size_selection)
		female_genotype = female_types[N % len(female_types)]
		if female_genotype == '++':
			male_genotype = 'w-'
		else:
			male_genotype = male_types[N % len(male_types)]

		# Create a full formatted question (Blackboard format)
		complete_question = write_question(N+1, female_genotype, male_genotype, progeny_size)

		# Append question if successfully generated
		if complete_question is not None:
			N += 1
			question_bank_list.append(complete_question)

		if N >= args.max_questions:
			break

	# Show a histogram of answer distributions for MC/MA types
	bptools.print_histogram()

	# Shuffle and limit the number of questions if over max
	if len(question_bank_list) > args.max_questions:
		random.shuffle(question_bank_list)
		question_bank_list = question_bank_list[:args.max_questions]

	# Announce where output is going
	print(f'\nWriting {len(question_bank_list)} question to file: {outfile}')

	# Write all questions to file
	write_count = 0
	with open(outfile, 'w') as f:
		for complete_question in question_bank_list:
			write_count += 1
			f.write(complete_question)

	# Final status message
	print(f'... saved {write_count} questions to {outfile}\n')

#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END
