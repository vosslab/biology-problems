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
#===========================================================
def geno2pheno(genotype):
	if genotype.startswith('+'):
		phenotype = "red"
	else:
		phenotype = "white"
	if '-' in genotype:
		phenotype += " male (&male;)"
	else:
		phenotype += " female (&female;)"
	return phenotype

#===========================================================
#===========================================================
def geno_span(genotype_html):
	return (
		"<span style='font-family: monospace; font-size: 0.95em; font-weight: 600; "
		"text-transform: none; font-variant: normal;'>"
		f"{genotype_html}</span>"
	)

#===========================================================
#===========================================================
def sex_word_span(word, color_hex):
	return f"<span style='color: {color_hex}; font-weight: 600;'>{word}</span>"

#===========================================================
#===========================================================
def get_answer(female_genotype, male_genotype):
	if female_genotype == "++":
		return 4
	elif female_genotype == "+w":
		if male_genotype == "+-":
			return 1
		elif male_genotype == "w-":
			return 0
	elif female_genotype == "ww":
		if male_genotype == "+-":
			return 3
		elif male_genotype == "w-":
			return 2

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
	female_word = sex_word_span("female", "#990070")
	male_word = sex_word_span("male", "#002499")
	female_label = (
		f"{female_word} <span style='font-weight: 400;'>(</span>"
		"<span style='font-weight: 400;'>&female;</span>"
		"<span style='font-weight: 400;'>)</span>"
	)
	male_label = (
		f"{male_word} <span style='font-weight: 400;'>(</span>"
		"<span style='font-weight: 400;'>&male;</span>"
		"<span style='font-weight: 400;'>)</span>"
	)
	mystr = '<table cellpadding="2" cellspacing="2" style="border-collapse: collapse; text-align:center; border: 1px solid black; font-size: 14px;">'
	mystr += f"<tr><th>phenotype</th><th>{female_label}</th><th>{male_label}</th></tr> "
	mystr += "<tr><td><span style='color: darkred;'>red-eyed (wildtype)</span></td> "
	mystr +=   f"<td align='center'>{pcount.get('red female (&female;)', 0)}</td>"
	mystr +=   f"<td align='center'>{pcount.get('red male (&male;)', 0)}</td></tr> "
	mystr += "<tr><td><span style='color: #595959; font-weight: 600;'>white-eyed (mutant)</span></td> "
	mystr +=   f"<td align='center'>{pcount.get('white female (&female;)', 0)}</td>"
	mystr +=   f"<td align='center'>{pcount.get('white male (&male;)', 0)}</td></tr> "
	mystr += "</table><br/>"
	return mystr

#===========================================================
#===========================================================
def build_question(N, female_genotype, male_genotype, progeny_size):
	wildtype_word = "<span style='color: #8b0000; font-weight: 600;'>wildtype</span>"
	mutant_word = "<span style='color: #595959; font-weight: 600;'>mutant</span>"
	red_phenotype = "<span style='color: #8b0000; font-weight: 600;'>red-eyed (wildtype)</span>"
	white_phenotype = "<span style='color: #595959; font-weight: 600;'>white-eyed (mutant)</span>"
	female_word = sex_word_span("female", "#990070")
	male_word = sex_word_span("male", "#002499")
	female_label = (
		f"{female_word} <span style='font-weight: 400;'>(</span>"
		"<span style='font-weight: 400;'>&female;</span>"
		"<span style='font-weight: 400;'>)</span>"
	)
	male_label = (
		f"{male_word} <span style='font-weight: 400;'>(</span>"
		"<span style='font-weight: 400;'>&male;</span>"
		"<span style='font-weight: 400;'>)</span>"
	)

	choices_list = [
		f"heterozygous {female_label} {geno_span('+w')} and {mutant_word} {male_label} {geno_span('w-')}",
		f"heterozygous {female_label} {geno_span('+w')} and {wildtype_word} {male_label} {geno_span('+-')}",
		f"homozygous {mutant_word} {female_label} {geno_span('ww')} and {mutant_word} {male_label} {geno_span('w-')}",
		f"homozygous {mutant_word} {female_label} {geno_span('ww')} and {wildtype_word} {male_label} {geno_span('+-')}",
		f"homozygous {wildtype_word} {female_label} {geno_span('++')} and {male_label} of unknown genotype",
	]

	pre_question = (
		"<p>The "
		f"{white_phenotype} phenotype is an X-linked recessive disorder in fruit flies. "
		f"The {red_phenotype} allele, {geno_span('+')}, is dominant to the white ({mutant_word}) allele, {geno_span('w')}. "
		f"The offspring of size {{0}} from the mating of a single {female_label} and a single {male_label} "
		"are shown in the table below:</p>"
	).format(progeny_size)

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

	bbformat = bptools.formatBB_MC_Question(N, question_txt, choices_list, answer_txt)
	return bbformat

#===========================================================
#===========================================================
def write_question(N: int, args) -> str:
	female_types = ("++", "+w", "ww")
	male_types = ("+-", "w-")
	progeny_size_selection = (160, 200, 240, 320, 360, 400, 480, 600)

	progeny_size = random.choice(progeny_size_selection)
	female_genotype = female_types[(N - 1) % len(female_types)]
	if female_genotype == '++':
		male_genotype = 'w-'
	else:
		male_genotype = male_types[(N - 1) % len(male_types)]

	complete_question = build_question(N, female_genotype, male_genotype, progeny_size)
	return complete_question

#===========================================================
#===========================================================
# This function handles the parsing of command-line arguments.
def parse_arguments():
	"""
	Parses command-line arguments for the script.
	"""
	parser = bptools.make_arg_parser(description="Generate X-linked fly cross questions.")
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

	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)

#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END
