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
def random_dot_cell(dot: str, target_size: int, variable_range: int=5) -> str:
	"""
	Generates an HTML <td> element with a span containing a dot of random font size.

	Args:
		dot (str): The character to display (e.g., '&#x25CF;' or '.').
		target_size (int): target font size.
		variable_range (int)

	Returns:
		str: HTML <td> element as a string.
	"""
	font_size = target_size + random.randint(-variable_range//2, variable_range//2)
	cell = (
		f'<td style="border: 0px solid white;">'
		f'<span style="font-size: {font_size}px; color: darkred;">{dot}</span>'
		f'</td>'
	)
	return cell

#===========================================================
def coagulated_blood() -> str:
	"""
	Generates a small table of randomly sized coagulated blood dots.

	Returns:
		str: HTML string representing coagulated blood.
	"""
	table = ''
	table += (
		'<table style="border-collapse: collapse; border: 0px solid white;" '
		'cellpadding="0" cellspacing="150"><tbody>'
	)

	size_map = [
		[25, 25, 20, 25],
		[25, 30, 25, 15],
		[20, 25, 25, 25],
	]

	num_cols = len(size_map[0])

	for i in range(len(size_map)):
		table += '<tr>'
		for j in range(num_cols):
			dot = '&#x25CF;' if (i+j) % 2 == 0 else '.'
			size = size_map[i][j]
			table += random_dot_cell(dot, size, 5)
		table += '</tr>'

	table += '</tbody></table>'
	return table

#===========================================================
#===========================================================
def normal_blood():
	symbol = '<span style="font-size: 100px; color: red;">&#11054;</span>'
	return symbol

#===========================================================
#===========================================================
def createHtmlTable(code: str) -> str:
	"""
	Creates an HTML table visualizing a blood test result based on a binary code.

	Args:
		code (str): A string of 1s and 0s representing blood test results.
		            '1' indicates normal blood (reaction), '0' indicates coagulated blood (no reaction).

	Returns:
		str: HTML string representing the blood test result table.
	"""
	table = ''
	table += '<table style="border-collapse: collapse; border: 1px; border-color: black;">'
	table += '<tbody>'
	table += '<tr>'

	data_style = 'style="border: 2px solid gray; text-align: center; vertical-align: middle;"'
	empty_style = 'style="border: 0px solid white;"'

	# Blood result symbols row
	for c in code:
		table += f'<td {data_style}>'
		table += normal_blood() if c == '1' else coagulated_blood()
		table += '</td>'
		table += f'<td {empty_style}> </td>'
	table += '</tr>'
	table += '<tr>'

	# Labels row
	labels = ['A antigen', 'B antigen', 'D antigen', 'control']
	for label in labels:
		table += f'<td {data_style}>{label}</td>'
		table += f'<td {empty_style}> </td>'

	table += '</tr></tbody></table>'
	return table

#===========================================================
#===========================================================
code2type = {
	'111':	'O-',
	'011':	'A-',
	'101':	'B-',
	'001':	'AB-',
	'110':	'O+',
	'010':	'A+',
	'100':	'B+',
	'000':	'AB+',
}

#=========================
def getInvertCode(bcode: str) -> str:
	"""
	Returns the bitwise inversion of a binary blood type code.

	Each '0' becomes '1' and each '1' becomes '0'.

	Args:
		bcode (str): A string consisting of binary digits (e.g., "110").

	Returns:
		str: Inverted binary string (e.g., "001").
	"""
	# Validate that input contains only '0' and '1'
	assert all(bit in "01" for bit in bcode), f"Invalid binary code: {bcode}"

	# Translation table for flipping bits
	flip_table = str.maketrans("01", "10")
	return bcode.translate(flip_table)

#=========================
def flipPlace(bcode: str, place: int = 3) -> str:
	"""
	Returns a modified version of the binary code where a specific bit is flipped.

	Args:
		bcode (str): A binary string (e.g., "110").
		place (int): The 1-based position of the bit to flip (default is 3).

	Returns:
		str: Binary string with the specified bit inverted.
	"""
	assert all(bit in "01" for bit in bcode), f"Invalid binary code: {bcode}"
	assert 1 <= place <= len(bcode), f"Place {place} out of range for code of length {len(bcode)}"

	flipped_bit = getInvertCode(bcode[place - 1])
	return bcode[:place - 1] + flipped_bit + bcode[place:]

#===========================================================
#===========================================================
#===========================================================
def generate_choices(blood_type_code: str, num_choices: int) -> list:
	"""
	Generate multiple choice answers for a blood test question.

	Prioritizes plausible distractors and pads with flipped variants as needed.

	Args:
		bcode (str): Base binary string (e.g., '101')
		num_choices (int): Total number of choices to return

	Returns:
		list[str]: Shuffled list of binary string choices
	"""
	assert 2 <= num_choices <= 8, "Must request between 2 and 8 choices"

	choices_set = set()

	# correct answer with good control
	answer_full_code = blood_type_code + '1'
	invert_bt_code = getInvertCode(blood_type_code)

	# answer with bad control
	choices_set.add(blood_type_code + '0')
	# opposite with good control
	choices_set.add(invert_bt_code + '1')
	# opposite with bad control
	choices_set.add(invert_bt_code + '0')

	# If we already have enough distractors, trim and append answer
	if len(choices_set) >= num_choices - 1:
		choices_list = list(choices_set)
		random.shuffle(choices_list)
		choices_list = choices_list[:num_choices - 1]
		choices_list.append(answer_full_code)
		# choices_list.sort()
		random.shuffle(choices_list)
		return choices_list, answer_full_code

	# Not enough yet: add correct answer and pad with flipped variants
	choices_set.add(answer_full_code)
	for code in list(choices_set):
		# flip +/- (i.e., D antigen position)
		choices_set.add(flipPlace(code, 3))
		if len(choices_set) >= num_choices:
			break

	assert len(choices_set) == num_choices, "error in logic"

	choices_list = list(choices_set)
	#choices_list.sort()
	random.shuffle(choices_list)
	return choices_list, answer_full_code

#===========================================================
#===========================================================
def code2display(bcode):
	display_txt = bcode
	display_txt = display_txt.replace("0", "%")
	display_txt = display_txt.replace("1", "O")
	return display_txt

#===========================================================
def get_question_text(blood_type_code: str) -> str:
	"""
	Generates the main question prompt with contextual background.

	Args:
		blood_type_code (str): A binary string representing blood type.

	Returns:
		str: A question prompt with additional context.
	"""
	blood_type = code2type[blood_type_code]
	question_text = ''
	question_text += (
		"<p>During a blood typing test, anti-A, anti-B, and anti-D antibodies are added "
		"to a blood sample along with a control. A visible reaction "
		"indicates the presence or absence of the corresponding antigens.</p>"
	)
	question_text += (
		f"<p>What would the test results look like for someone with "
		f'<strong><span style="font-size: 1.2em;">{blood_type} blood type</span></strong>?</p>'
	)
	return question_text

#===========================================================
#===========================================================
def format_blood_type_code(blood_type_code: str) -> str:
	"""
	Formats a blood type code into an HTML string with table and display text.

	Args:
		blood_type_code (str): A binary string (e.g. '101') representing
		the blood type result.

	Returns:
		str: HTML-formatted string showing the table and visual code.
	"""
	table_html = createHtmlTable(blood_type_code)
	display_text = code2display(blood_type_code)
	monospace_span = (
		f'<span style="font-family: monospace; font-size: 1.2em; '
		f'color: darkred;">{display_text}</span>'
	)
	formatted_text = (
		f"<p>{table_html}</p>"
		f"<p>Visual representation of test reactions: {monospace_span}</p>"
	)
	return formatted_text

#===========================================================
#===========================================================
# This function creates and formats a complete question for output.
def write_question(N: int, args) -> str:
	"""
	Creates a complete formatted question for output.
	"""
	blood_type_codes = list(code2type.keys())
	blood_type_code = blood_type_codes[(N - 1) % len(blood_type_codes)]

	# Generate the main question text
	question_text = get_question_text(blood_type_code)

	# Generate answer choices
	choices_list, answer_code = generate_choices(blood_type_code, args.num_choices)

	formatted_choices_list = []
	for choice_code in choices_list:
		formatted_choice_text = format_blood_type_code(choice_code)
		if choice_code == answer_code:
			formatted_answer_text = formatted_choice_text
		formatted_choices_list.append(formatted_choice_text)

	# Format the question using a helper function from the bptools module
	complete_question = bptools.formatBB_MC_Question(N, question_text, formatted_choices_list, formatted_answer_text)

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
		`num_choices`, and `question_type`.
	"""
	# Create an argument parser with a description of the script's functionality
	parser = bptools.make_arg_parser(description="Generate questions.")
	parser = bptools.add_choice_args(parser, default=5)

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


	outfile = bptools.make_outfile(None)
	bptools.collect_and_write_questions(write_question, args, outfile)

#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END
