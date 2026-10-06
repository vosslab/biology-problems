#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

"""
Template for a multiple choice question generator.

Design the puzzle first, then write the thinnest wrapper around it. Wording and distractor
rules live in docs/QUESTION_PEDAGOGY_GUIDE.md and docs/QUESTION_VOICE_GUIDE.md.
"""

# Import built-in Python modules
# Provides functions to generate random numbers and selections
import random
# Provides exact fractions, so the arithmetic of each choice stays exact
import fractions

# Import external modules (pip-installed)
# No external modules are used here currently

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities
import bptools

# Stock volumes in microliters; write_question draws the scenario at random
ALIQUOTS_UL = (10, 20, 25, 50)

# How many times larger the total volume is than the stock volume, so every key is 1/fold
DILUTION_FOLDS = (4, 5, 10, 20)

# The two parts of the new solution a question can ask about; each gives a different answer
ASKED_PARTS = ('stock solution', 'distilled water')

#===========================================================
#===========================================================
# This function generates and returns the main question text.
def get_question_text(aliquot_ul: int, diluent_ul: int, asked_part: str) -> str:
	"""
	Generates and returns the main text for the question.

	Stem order is rule (only when the student needs one), case, question, with no preamble.

	Args:
		aliquot_ul (int): Volume of stock solution added, in microliters.
		diluent_ul (int): Volume of distilled water added, in microliters.
		asked_part (str): The part of the new solution the question asks about.

	Returns:
		str: A string containing the main question text.
	"""
	# Show numbers and units in monospace, with the same unit throughout
	aliquot_text = f"<span style='font-family: monospace;'>{aliquot_ul} &micro;L</span>"
	diluent_text = f"<span style='font-family: monospace;'>{diluent_ul} &micro;L</span>"

	# Initialize an empty string for the question text
	question_text = ""

	# Case sentence: the data
	question_text += f"You add {aliquot_text} of stock solution "
	question_text += f"to {diluent_text} of distilled water. "

	# Question: use the course lead-in and underline only the words that change the answer
	question_text += "Which one of the following is the fraction of the new solution that is "
	question_text += f"<u>{asked_part}</u>?"

	# Return the complete question text
	return question_text

#===========================================================
#===========================================================
# This function turns a fraction into the fixed "numerator/denominator" choice format.
def fraction_label(fraction: fractions.Fraction) -> str:
	"""
	Formats a fraction as a choice label such as "1/10".

	Args:
		fraction (fractions.Fraction): The fraction to format.

	Returns:
		str: The numerator and denominator joined by a slash.
	"""
	# Fraction reduces itself, so 50/500 prints as 1/10
	label = f"{fraction.numerator}/{fraction.denominator}"

	# Return the finished label
	return label

#===========================================================
#===========================================================
# This function generates multiple answer choices for a question.
def generate_choices(num_choices: int, aliquot_ul: int, diluent_ul: int,
		asked_part: str) -> (list, str):
	"""
	Generates a list of answer choices along with the correct answer.

	Every wrong choice is the answer one named student error produces.

	Args:
		num_choices (int): The total number of answer choices to generate.
		aliquot_ul (int): Volume of stock solution added, in microliters.
		diluent_ul (int): Volume of distilled water added, in microliters.
		asked_part (str): The part of the new solution the question asks about.

	Returns:
		tuple: A tuple containing:
			- list: A list of answer choices in ascending numeric order.
			- str: The correct answer text.
	"""
	# The total volume is the denominator of a fraction of the new solution
	total_ul = aliquot_ul + diluent_ul

	# The asked part and the other part (stock solution is the aliquot)
	part_volumes = {'stock solution': aliquot_ul, 'distilled water': diluent_ul}
	asked_ul = part_volumes[asked_part]
	other_ul = total_ul - asked_ul

	# Correct answer: the asked part out of the total volume (1/10 for 50 uL stock, 450 uL water)
	answer_fraction = fractions.Fraction(asked_ul, total_ul)

	# Wrong fractions are each computed from a named student error.  The varied pool lets a
	# naturally sorted choice list put the key in different positions across scenarios.
	wrong_fractions = []
	# error: divides by the other part, not the total
	wrong_fractions.append(fractions.Fraction(asked_ul, other_ul))
	# error: reports the other part's fraction, swapping stock and water
	wrong_fractions.append(fractions.Fraction(other_ul, total_ul))
	# error: inverts the fraction, putting the total over the asked part
	wrong_fractions.append(fractions.Fraction(total_ul, asked_ul))
	# error: counts the asked part twice when calculating the total volume
	wrong_fractions.append(fractions.Fraction(asked_ul, total_ul + asked_ul))
	# error: counts the other part twice when calculating the total volume
	wrong_fractions.append(fractions.Fraction(asked_ul, total_ul + other_ul))
	# error: doubles the total volume before making the fraction
	wrong_fractions.append(fractions.Fraction(asked_ul, 2 * total_ul))
	# error: treats the stock volume as the whole new solution
	wrong_fractions.append(fractions.Fraction(asked_ul, aliquot_ul))
	# error: treats the water volume as the whole new solution
	wrong_fractions.append(fractions.Fraction(asked_ul, diluent_ul))
	# optional course voice: none of the new solution is the asked part
	wrong_fractions.append(fractions.Fraction(0, 1))

	# Remove duplicates and any wrong fraction equal to the correct answer
	unique_wrong = []
	for fraction in wrong_fractions:
		if fraction != answer_fraction and fraction not in unique_wrong:
			unique_wrong.append(fraction)

	# A two-choice item needs its sole distractor to represent a meaningful arithmetic error.
	# The optional absurd choice is available only when additional choices leave room for that.
	if num_choices == 2:
		unique_wrong.remove(fractions.Fraction(0, 1))

	# Fail loudly when more choices are requested than the puzzle defines
	if num_choices - 1 > len(unique_wrong):
		raise ValueError(f"This puzzle defines {len(unique_wrong) + 1} choices, not {num_choices}")

	# Randomly choose named errors; true randomness prevents either asked part from predicting
	# the key position. Numeric choices retain their natural ascending order below.
	selected_wrong = random.sample(unique_wrong, num_choices - 1)

	# Keep the answer plus the selected wrong choices
	choice_fractions = [answer_fraction] + selected_wrong

	# Fractions have a natural order, so sort ascending instead of shuffling
	choice_fractions.sort()

	# Convert every fraction to its label
	choices_list = [fraction_label(fraction) for fraction in choice_fractions]
	answer_text = fraction_label(answer_fraction)

	# Return the list of choices and the correct answer
	return choices_list, answer_text

#===========================================================
#===========================================================
# This function creates and formats a complete question for output.
def write_question(N: int, args) -> str:
	"""
	Creates a complete formatted question for output.

	Args:
		N (int): The question number, used for labeling the question.
		args (argparse.Namespace): Parsed command-line arguments.

	Returns:
		str: A formatted question string containing the question text,
		answer choices, and the correct answer.
	"""
	# Pick the scenario at random; the volumes and the asked part change the data, not the wording
	aliquot_ul = random.choice(ALIQUOTS_UL)
	diluent_ul = aliquot_ul * (random.choice(DILUTION_FOLDS) - 1)
	asked_part = random.choice(ASKED_PARTS)

	# Generate the main question text
	question_text = get_question_text(aliquot_ul, diluent_ul, asked_part)

	# Generate answer choices and the correct answer
	choices_list, answer_text = generate_choices(
		args.num_choices, aliquot_ul, diluent_ul, asked_part
	)

	# Format the question using a helper function from the bptools module
	complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)

	# Return the formatted question string
	return complete_question

#===========================================================
#===========================================================
# This function handles the parsing of command-line arguments.
def parse_arguments():
	"""
	Parses command-line arguments for the script.

	Returns:
		argparse.Namespace: Parsed arguments with attributes `duplicates`,
		`max_questions`, `num_choices`, and `question_type`.
	"""
	# Create an argument parser with a description of the script's functionality
	parser = bptools.make_arg_parser()

	# Add standard argument bundles
	parser = bptools.add_choice_args(parser)
	parser = bptools.add_hint_args(parser)
	parser = bptools.add_question_format_args(parser, required=True)

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
	3. Generate and write formatted questions using shared helpers.
	4. Print status.
	"""

	# Parse arguments from the command line
	args = parse_arguments()

	# Generate the output file name based on the script name and arguments
	hint_mode = 'with_hint' if args.hint else 'no_hint'
	outfile = bptools.make_outfile(
		args.question_type.upper(),
		hint_mode,
		f"{args.num_choices}_choices"
	)

	# Collect and write questions using shared helper
	bptools.collect_and_write_questions(write_question, args, outfile)

#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END
