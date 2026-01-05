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
# This function generates and returns the main question text.
def get_question_text() -> str:
	"""
	Generates and returns the main text for the question.

	Returns:
		str: A string containing the main question text.
	"""
	# Initialize an empty string for the question text
	question_text = ""

	# Add the actual question text to the string
	question_text += "This is a hard question?"

	# Return the complete question text
	return question_text

#===========================================================
#===========================================================
def get_Henderson_Hasselbalch_equation(
	pH=None, pKa=None, HA=None, A_=None,
	words=False, plus=None, wrong=False):

	open_bracket = "<mo stretchy='true'>[</mo>"
	close_bracket = "<mo stretchy='true'>]</mo>"
	# Define MathML representation for the weak acid (HA)
	if HA is None:
		# Symbolic HA if no value is provided
		if words is True:
			ha_conj_base = open_bracket + "<mi>Acid</mi>" + close_bracket
		else:
			ha_conj_base = open_bracket + "<mi>HA</mi>" + close_bracket
	else:
		# Numeric HA value if provided
		ha_conj_base = open_bracket + f"<mn>{HA:.2f}</mn>" + close_bracket
	# Define MathML representation for the conjugate base (A⁻)
	if A_ is None:
		# Symbolic A⁻ if no value is provided
		a_mathml = "<msup><mi mathvariant='normal'>A</mi><mo>&#8211;</mo></msup>"
		if words is True:
			a__conj_acid = open_bracket + "<mi>Base</mi>" + close_bracket
		else:
			a__conj_acid = open_bracket + a_mathml + close_bracket
	else:
		# Numeric A⁻ value if provided
		a__conj_acid = open_bracket + f"<mn>{A_:.2f}</mn>" + close_bracket
	# Determine the correct or intentionally incorrect structure of the equation
	# Set whether [HA] appears in the numerator
	if wrong is False:
		# Correct format: [A⁻] / [HA]
		ha_on_top = False
	else:
		# Incorrect format: [HA] / [A⁻]
		ha_on_top = True
	# Initialize the MathML string for the equation
	equation_text = ""
	equation_text += "<p><math xmlns='http://www.w3.org/1998/Math/MathML'>"
	# Add pH to the equation
	if pH is None:
		# Symbolic pH if no value is provided
		equation_text += "<mi>pH</mi><mo>&#8201;</mo><mo>=</mo><mo>&#8201;</mo>"
	else:
		# Numeric pH value if provided
		equation_text += f"<mn>{pH:.2f}</mn><mo>&#8201;</mo><mo>=</mo><mo>&#8201;</mo>"
	# Add pKa to the equation
	if pKa is None:
		# Symbolic pKa if no value is provided
		equation_text += "<msub><mi>pK</mi><mi>a</mi></msub>"
	else:
		# Numeric pKa value if provided
		equation_text += f"<mn>{pKa:.2f}</mn>"
	# Add the plus or minus sign based on the 'plus' argument
	if plus == "-" or plus == "minus":
		# Add minus sign and flip numerator and denominator
		equation_text += "<mo>&#160;</mo><mo>&ndash;</mo><mo>&#8201;</mo>"
		ha_on_top = not ha_on_top
	else:
		# Add plus sign
		equation_text += "<mo>&#160;</mo><mo>+</mo><mo>&#8201;</mo>"
	# Add the log function and start the fraction
	equation_text += "<msub><mo>log</mo><mn>10</mn></msub>"
	# Begin the numerator of the fraction
	equation_text += "<mfenced><mfrac><mrow>"
	# Insert the numerator based on the 'ha_on_top' flag
	if ha_on_top is False:
		# A⁻ goes on top in the correct format
		equation_text += a__conj_acid
	else:
		# HA goes on top in the incorrect format
		equation_text += ha_conj_base
	# Close the numerator
	equation_text += "</mrow><mrow>"
	# Insert the denominator based on the 'ha_on_top' flag
	if ha_on_top is False:
		# HA goes on bottom in the correct format
		equation_text += ha_conj_base
	else:
		# A⁻ goes on bottom in the incorrect format
		equation_text += a__conj_acid
	# Close the denominator and log function
	equation_text += "</mrow></mfrac></mfenced>"
	# Complete the MathML structure
	equation_text += "</math></p>"
	# Return the final MathML equation string
	return equation_text


#===========================================================
#===========================================================
# This function generates multiple answer choices for a question.
def generate_choices(num_choices: int) -> (list, str):
	"""
	Generates a list of answer choices along with the correct answer.

	Args:
		num_choices (int): The total number of answer choices to generate.

	Returns:
		tuple: A tuple containing:
			- list: A list of answer choices (mixed correct and incorrect).
			- str: The correct answer text.
	"""
	# Define a list of correct answer choices
	choices_list = [
		'competitive inhibitor',
		'non-competitive inhibitor',
	]

	# Randomly select one correct answer from the list
	answer_text = random.choice(choices_list)

	# Define a list of incorrect answer choices
	wrong_choices_list = [
		'molecular stopper',
		'metabolic blocker',
	]

	# Shuffle the incorrect choices to add randomness
	random.shuffle(wrong_choices_list)

	# Add incorrect choices to the choices list to reach the desired number of choices
	choices_list.extend(wrong_choices_list[:num_choices - len(choices_list)])

	# Shuffle all the choices to randomize their order
	random.shuffle(choices_list)

	# Return the list of choices and the correct answer
	return choices_list, answer_text

#===========================================================
#===========================================================
# This function creates and formats a complete question for output.
def write_equation_question(N: int) -> str:
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
	question_text = "<p>Which one of the following equations is the correct form of the "
	question_text += "Henderson-Hasselbalch equation?</p>"

	words_bool = (N%2 == 0)
	if (N // 2) % 2 == 0:
		answer_html = get_Henderson_Hasselbalch_equation(
			plus='plus', wrong=False, words=words_bool)
	else:
		answer_html = get_Henderson_Hasselbalch_equation(
			plus='minus', wrong=False, words=words_bool)
	if (N // 4) % 2 == 0:
		wrong_html = get_Henderson_Hasselbalch_equation(
			plus='plus', wrong=True, words=words_bool)
	else:
		wrong_html = get_Henderson_Hasselbalch_equation(
			plus='minus', wrong=True, words=words_bool)

	# Generate answer choices and the correct answer
	if (N // 8) % 2 == 0:
		choices_list = [answer_html, wrong_html]
	else:
		choices_list = [wrong_html, answer_html]

	# Format the question using a helper function from the bptools module
	complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_html)

	# Return the formatted question string
	return complete_question

#===========================================================
#===========================================================
def write_question(N: int, args) -> str:
	if args.question_type == 'equation':
		return write_equation_question(N)
	if args.question_type == 'ratio':
		question_text = get_question_text()
		choices_list, answer_text = generate_choices(args.num_choices)
		return bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)
	raise NotImplementedError("question_type is not implemented in this script.")

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
	parser = bptools.make_arg_parser(description="Generate Henderson-Hasselbalch questions.")
	parser = bptools.add_choice_args(parser, default=4)
	question_group = parser.add_mutually_exclusive_group(required=False)

	# Add an option to manually set the question type
	question_group.add_argument(
		'-t', '--type', dest='question_type', type=str,
		choices=('equation', 'pH', 'pKa', 'ratio'),
		help='Set the question type: num (numeric) or mc (multiple choice)'
	)

	# Add a shortcut option to set the question type to 'equation'
	question_group.add_argument(
		'-e', '--equation', dest='question_type', action='store_const', const='equation',
		help='Set question type to equation'
	)

	# Add a shortcut option to set the question type to 'pH'
	question_group.add_argument(
		'-p', '--ph', '--pH', dest='question_type', action='store_const', const='pH',
		help='Set question type to pH'
	)

	# Add a shortcut option to set the question type to 'pKa'
	question_group.add_argument(
		'-k', '--pka', '--pKa', dest='question_type', action='store_const', const='pKa',
		help='Set question type to pKa'
	)

	# Add a shortcut option to set the question type to 'ratio'
	question_group.add_argument(
		'-r', '--ratio', dest='question_type', action='store_const', const='ratio',
		help='Set question type to ratio'
	)
	parser.set_defaults(question_type='equation')

	# Parse the provided command-line arguments and return them
	args = parser.parse_args()
	return args

#===========================================================
#===========================================================
# This function serves as the entry point for generating and saving questions.
def main():
	"""
	Main function that orchestrates question generation and file output.
	"""

	# Parse arguments from the command line
	args = parse_arguments()

	if args.question_type == 'equation' and args.duplicates > 16:
		args.duplicates = 16
	outfile = bptools.make_outfile(None, args.question_type)
	bptools.collect_and_write_questions(write_question, args, outfile)

#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END
