#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
# Provides functions to generate random numbers and selections
import random
import math

# Import external modules (pip-installed)
# No external modules are used here currently

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities
import bptools
import binomiallib

num2txt = {
	1: 'one',
	2: 'two',
	3: 'three',
	4: 'four',
	5: 'five',
	6: 'six',
	7: 'seven',
	8: 'eight',
	9: 'nine',
	10: 'ten',
}

#===========================================================
#===========================================================
def get_question_text(male_offspring: int, female_offspring: int,
	total_offspring: int) -> str:
	"""
	Generate the HTML question text with assumptions, model cue, and color legend.

	Args:
		male_offspring (int): Number of boys.
		female_offspring (int): Number of girls.
		total_offspring (int): Total number of children.

	Returns:
		str: HTML string for the question stem.
	"""

	# Color choices for emphasis (dark cyan for boys, dark pink for girls)
	color_boys = "#0086b3"
	color_girls = "#b30086"

	question_text = ""

	# Model badge with symbolic parameters only
	question_text += binomiallib.format_expression([
		'<strong>Model:</strong> Binomial &rarr;', binomiallib.binomial_coefficient('n', 'k'),
		'&sdot;p<sup>n-k</sup>&sdot;q<sup>k</sup>'])

	question_text += "<p>"
	question_text += "In this scenario, assume that each child is born independently "
	question_text += "with the same chance of being either sex. The event outcomes "
	question_text += "are mutually exclusive, so we can apply the binomial model to "
	question_text += "determine the probability of a specific combination.</p>"

	# Main question stem
	question_text += "<p>"
	question_text += f"A woman has <strong>{num2txt[total_offspring]} "
	question_text += f"({total_offspring})</strong> children. "
	question_text += "What is the probability that she has exactly "
	question_text += f"<span style='color:{color_boys};'><strong>{num2txt[male_offspring]} "
	question_text += f"({male_offspring}) boys &male;</strong></span> and "
	question_text += f"<span style='color:{color_girls};'><strong>{num2txt[female_offspring]} "
	question_text += f"({female_offspring}) girls &female;</strong></span>? "
	question_text += "</p>"

	return question_text

#===========================================================
#===========================================================
def write_question(N: int, args) -> str:
	total_offspring = random.randint(args.min_offspring, args.max_offspring)
	female_offspring = random.randint(2, total_offspring-2)
	male_offspring = total_offspring - female_offspring

	question_text = get_question_text(male_offspring, female_offspring, total_offspring)

	# Initialize the list of answer choices
	choices_list = []

	# Correct answer: probability with equal 0.5 chance for each sex
	answer_text = binomiallib.binomial_probability(total_offspring, female_offspring, 0.5, 0.5)
	choices_list.append(answer_text)

	# Errors: confuse the roles of the given counts, or substitute 3:1 probabilities.
	counts = {total_offspring, male_offspring, female_offspring}
	candidates = []
	for n in counts:
		for k in counts:
			if k > n:
				continue
			for p, q in ((0.5, 0.5), (0.25, 0.75), (0.75, 0.25)):
				candidates.append((n, k, p, q))
	random.shuffle(candidates)
	correct_value = math.comb(total_offspring, female_offspring) * 0.5 ** total_offspring
	used = {f"{correct_value * 100:.1f}"}
	for n, k, p, q in candidates:
		value = math.comb(n, k) * p ** (n - k) * q ** k
		if not 0.01 <= value <= 0.40:
			continue
		percentage = f"{float(value) * 100:.1f}"
		if percentage in used:
			continue
		choices_list.append(binomiallib.binomial_probability(n, k, p, q))
		used.add(percentage)
		if len(choices_list) == 5:
			break

	# Randomly shuffle the final list of choices
	random.shuffle(choices_list)

	complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)

	return complete_question

#===========================================================
#===========================================================
# This function handles the parsing of command-line arguments.
def parse_arguments():
	"""
	Parses command-line arguments for the script.
	"""
	parser = bptools.make_arg_parser(description="Generate probability of progeny questions.")
	parser.add_argument(
		'--min', '--min-offspring', type=int, dest='min_offspring',
		default=5, help='Minimum total number of offspring to consider.'
	)
	parser.add_argument(
		'--max', '--max-offspring', type=int, dest='max_offspring',
		default=10, help='Maximum total number of offspring to consider.'
	)
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
	2. Generate the output filename.
	3. Generate formatted questions using write_question().
	4. Write all formatted questions to the output file.
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
