#!/usr/bin/env python3

import math

import bptools
import gene_map_class_lib as gmc
import genemaplib as gml

debug = False

#=====================
#=====================
#=====================
#=====================
def get_question_text(gene_order_str, question_type):
	"""
	Generates the question text for an interference-related genetic mapping question.

	Args:
		gene_order_str (str): A string representing the order of genes, e.g., 'ABC'.
		question_type (str): Type of question ('mc' for multiple-choice, other types for numeric calculation).

	Returns:
		str: HTML-formatted question text.
	"""
	question_string = ''

	# Introduction to interference in genetic studies
	question_string += '<p>In genetic studies, interference refers to the phenomenon where the '
	question_string += 'occurrence of a crossover in one region of a chromosome reduces the likelihood '
	question_string += 'of another crossover occurring nearby, thereby affecting the expected genetic ratios.</p> '

	# Question prompt
	question_string += '<h6>Question</h6> '
	question_string += '<p>Based on the traits expressed in the offspring, '

	# Adjust the question based on the type of question (multiple-choice or numeric)
	if question_type == "mc":
		question_string += '<strong>select the correct fraction that represents the interference level</strong> '
	else:
		question_string += '<strong>calculate the percentage of interference</strong> '

	# Specify the genes being analyzed
	question_string += f'between genes {gene_order_str[0]} and {gene_order_str[-1]}.</p> '

	# HTML validation check
	if gml.is_valid_html(question_string) is False:
		print(question_string)
		raise ValueError("Generated HTML is not well-formed.")

	return question_string

#===========================================================
#===========================================================
def get_interference_steps():
	"""
	Returns the HTML formatted step-by-step instructions for calculating interference.

	Returns:
		str: HTML formatted string with step-by-step instructions.
	"""
	steps = '<h6>Step-by-Step Instructions for Calculating Interference</h6>'
	steps += '<ul>'
	steps += ' <li>Step 1: Count the observed number of double crossovers from the data table.</li>'
	steps += ' <li>Step 2: Calculate the probability of independent crossovers between distant genes.</li>'
	steps += '   <ul><li>Multiply the two individual crossover probabilities (based on their distance) for both adjacent gene pairs.</li></ul>'
	steps += ' <li>Step 3: Determine the expected number of double crossovers.</li>'
	steps += '   <ul><li>Multiply the combined probability (from Step 2) by the total progeny count.</li></ul>'
	steps += ' <li>Step 4: Calculate the Coefficient of Coincidence (CoC).</li>'
	steps += '   <ul><li>Divide the observed number of double crossovers (from Step 1) by the expected number (from Step 3).</li></ul>'
	steps += ' <li>Step 5: Calculate Interference.</li>'
	steps += '   <ul><li>Interference is given by the formula: Interference = 1 - CoC.</li></ul>'
	steps += '</ul>'

	# Validate the HTML (raise ValueError if invalid)
	if gml.is_valid_html(steps) is False:
		print(steps)
		raise ValueError("Generated HTML is not well-formed.")
	return steps

#===========================================================
#===========================================================
def get_important_tips():
	"""
	Returns the HTML formatted hints for solving the problem.

	Returns:
		str: HTML formatted string with hints.
	"""
	tips = '<h6>Important Answer Guidelines</h6>'
	tips += '<p><ul>'
	tips += '<li><i>Important Tip 1:</i> '
	tips += '  Your calculated distance between the pair of genes should be a whole number. '
	tips += '  Finding a decimal in your answer, such as 5.5, indicates a mistake was made. '
	tips += '  Please provide your answer as a complete number without fractions or decimals.</li>'
	tips += '<li><i>Important Tip 2:</i> '
	tips += '  Your answer should be written as a numerical value only, '
	tips += '  with no spaces, commas, or units such as "cM" or "map units". '
	tips += '  For example, if the distance is fifty one centimorgans, simply write "51".</li>'
	tips += '</ul></p>'
	if gml.is_valid_html(tips) is False:
		print(tips)
		raise ValueError
	return tips

#=====================
def describe_gene_map(GMC):
	describe_gene_map_string = ''
	up_genes = GMC.gene_order_str.upper()
	distances_dict = GMC.distances_dict
	describe_gene_map_string += '<p><ul> '
	describe_gene_map_string += '<li>The distance between genes '
	describe_gene_map_string += f'{up_genes[0]} and {up_genes[1]} is {distances_dict[(1,2)]} cM</li>'
	describe_gene_map_string += '<li>The distance between genes '
	describe_gene_map_string += f'{up_genes[0]} and {up_genes[2]} is {distances_dict[(1,3)]} cM</li>'
	describe_gene_map_string += '<li>The distance between genes '
	describe_gene_map_string += f'{up_genes[1]} and {up_genes[2]} is {distances_dict[(2,3)]} cM</li>'
	describe_gene_map_string += f'<li>The correct gene order determined from these distances is <strong>{up_genes}</strong></li>'
	describe_gene_map_string += '</ul></p> '
	return describe_gene_map_string

#=====================
#=====================
def make_choice_text_from_fraction(a,b):
	gcd = math.gcd(a,b)
	a //= gcd
	b //= gcd
	decimal = a/float(b)
	percent = (100*a)/float(b)
	percent = int(round(percent))
	text = f'<sup>{a}</sup>/<sub>{b}</sub> = {decimal:.4f} = {percent:d}%'
	return text, percent

#=====================
def generate_question(N, question_type, num_choices):
	"""
	Generates a formatted question string based on question type (multiple-choice or numeric answer).

	This function sets up a genetic mapping question using the `GeneMappingClass` (GMC), which
	generates the necessary progeny counts, interference fractions, and answer choices based on the
	type of question requested.

	Args:
		N (int): The question number, used to seed randomness in some cases.
		question_type (str): Type of question ('mc' for multiple-choice, 'num' for numeric answer).
		num_choices (int): Number of answer choices to provide in multiple-choice questions.

	Returns:
		str: A fully formatted question string ready to be displayed or saved.
	"""

	# Initialize the GeneMappingClass (GMC) for a 3-gene mapping question, setting `N` as the question number.
	GMC = gmc.GeneMappingClass(3, N)

	"""
	If the distance triplet list has already been cached, it randomly selects a triplet from the cache.
	If interference mode is enabled, it uses a different function to generate triplets.

	interference_mode = True:
		Generates a list of unique distance triplets based on interference fractions,
		with a fixed denominator of 100 for each fraction.
		interference is always a whole number when multiplied by 100

	interference_mode = False:
		uses a tuple representing the interference fraction (a, b).
		interference is a rational value or fraction value, such a 7/11
		interference may not be whole number when multiplied by 100
	"""
	if question_type == "mc":
		GMC.interference_mode = False
	else:
		GMC.interference_mode = True

	# Initialize the GMC question, setting up gene order, distance triplet list, and progeny counts.
	GMC.setup_question()

	# Print the ASCII table for the progeny, useful for debugging or previewing the question.
	print(GMC.get_progeny_ascii_table())

	# Retrieve the necessary components for displaying the question:
	# - `header`: The question header with background information.
	# - `phenotype_info_text`: A description of phenotypes related to the genes.
	# - `html_table`: An HTML table of progeny counts.
	# - `interference_steps`: Step-by-step instructions for calculating interference.
	header = GMC.get_question_header()
	phenotype_info_text = GMC.get_phenotype_info()
	html_table = GMC.get_progeny_html_table()
	interference_steps = get_interference_steps()
	describe_gene_map_string = describe_gene_map(GMC)
	question_string = get_question_text(GMC.gene_order_str.upper(), question_type)

	early_question = header + phenotype_info_text + html_table
	early_question += describe_gene_map_string + interference_steps + question_string

	# Verify that the parental genotypes are correctly identified by sorting genotype counts.
	# `parental_genotypes_tuple` contains the two highest-count genotypes (i.e., parental types).
	sorted_genotype_counts = sorted(GMC.genotype_counts.items(), key=lambda x: x[1], reverse=True)
	parental_genotypes_tuple = tuple(sorted((sorted_genotype_counts[0][0], sorted_genotype_counts[1][0])))
	if parental_genotypes_tuple != GMC.parental_genotypes_tuple:
		raise ValueError(f'parental_genotypes_tuple: {parental_genotypes_tuple} != {GMC.parental_genotypes_tuple}')

	# If the question type is multiple-choice (MC), generate a list of answer choices.
	if question_type == "mc":
		# Start with an initial choice for "no interference"
		choices_list = [ 'no interference, 0%', ]

		# Retrieve the interference fraction from GMC for genes 1 and 3.
		a, b = GMC.interference_dict[(1,3)]
		if (a, b) == (1, 2):
			# This case signifies a special condition where the question should not be generated.
			return None

		# Initialize a dictionary to store unique choices with their corresponding interference percentages.
		choices_dict = {
			100: 'complete interference, 100%',
			50: make_choice_text_from_fraction(1, 2)[0],
			0: 'no interference, 0%',
		}

		# Generate the correct answer text and interference percentage.
		answer_text, ans_percent = make_choice_text_from_fraction(a, b)
		choices_dict[ans_percent] = answer_text  # Add the correct answer to the choices dictionary.

		# Generate a plausible incorrect answer by flipping the interference fraction.
		wrong_text, wrong_percent = make_choice_text_from_fraction(b - a, b)
		choices_dict[wrong_percent] = wrong_text

		# Add more answer choices based on the denominator `b`.
		# If `b` is small, add more detailed choices by iterating over all possible numerators.
		# If `b` is large, add choices in steps to avoid cluttering with too many small increments.
		if b < 8:
			for i in range(1, b):
				if i*2 == b:
					# avoid 1/2 we have it already
					continue
				another_text, another_percent = make_choice_text_from_fraction(i, b)
				choices_dict[another_percent] = another_text
		else:
			for i in range(1, b, 2):
				if i*2 == b:
					# avoid 1/2 we have it already
					continue
				another_text, another_percent = make_choice_text_from_fraction(i, b)
				choices_dict[another_percent] = another_text

		# Sort the choices by percentage values and extract the text descriptions.
		choices_list = [value for (key, value) in sorted(choices_dict.items(), key=lambda x: x[0])]
		print(choices_list)

		# Combine all parts of the question into a single HTML string.
		full_question = early_question
		gml.is_valid_html(full_question)

		# Format the final question in multiple-choice format and return it.
		final_question = bptools.formatBB_MC_Question(N, full_question, choices_list, answer_text)
		return final_question

	# If the question type is numeric (FIB), generate a numeric answer question.
	else:
		# Retrieve additional instructions specific to numeric questions.
		fib_important_tips = get_important_tips()

		# Calculate the correct answer by taking the integer percentage for the interference fraction.
		a, b = GMC.interference_dict[(1,3)]
		answer = 100 * a // b

		# Generate the question text and validate the HTML.
		full_question = early_question + fib_important_tips
		GMC.is_valid_html(full_question)

		# Format the final question in numeric format (Fill-in-the-Blank) and return it.
		final_question = bptools.formatBB_NUM_Question(N, full_question, answer, tolerance_float=0.1, tol_message=False)
		return final_question

#=====================
def parse_arguments():
	parser = bptools.make_arg_parser(
		description="Generate three-point test cross interference questions."
	)
	parser = bptools.add_choice_args(parser, default=6)
	parser = bptools.add_question_format_args(parser, types_list=['mc', 'num'], required=True)
	args = parser.parse_args()
	return args

#=====================
def write_question(N: int, args) -> str | None:
	return generate_question(N, args.question_type, args.num_choices)

#=====================
#=====================
def main():
	args = parse_arguments()

	outfile_suffix = args.question_type.upper()
	if args.question_type == 'mc':
		outfile = bptools.make_outfile(outfile_suffix, f"{args.num_choices}_choices")
	else:
		outfile = bptools.make_outfile(outfile_suffix)
	bptools.collect_and_write_questions(write_question, args, outfile)

if __name__ == "__main__":
	main()

#THE END
