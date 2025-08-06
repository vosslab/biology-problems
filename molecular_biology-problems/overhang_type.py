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
import restrictlib

#=====================
#=====================
def explore_object(obj, depth=1, max_depth=5):
	if depth > max_depth:
		return "Max depth reached"

	for attr_name in dir(obj):
		if attr_name.startswith('_'):
			continue
		# Exclude dunder methods
		if not attr_name.startswith('__'):
			attr_value = getattr(obj, attr_name, 'N/A')
			print(f"{'  ' * depth}{attr_name} = {attr_value}")

			# Check if this is a bound method
			if callable(attr_value):
				try:
					# Invoke the bound method and explore it
					method_result = attr_value()
					print(f"{'  ' * (depth + 1)}Result of invoking method = {method_result}")
					explore_object(method_result, depth + 1)
				except Exception as e:
					print(f"{'  ' * (depth + 1)}Exception while invoking: {e}")

			# If it's a class, explore its attributes recursively
			elif not isinstance(attr_value, (int, float, str, list, tuple, dict)):
				explore_object(attr_value, depth + 1)

choice_color_map = {
	"5' overhang": '<span style="color: #e60000;">5&prime; overhang</span>', #RED
	"3' overhang": '<span style="color: #0039e6;">3&prime; overhang</span>', #BLUE
	'blunt': '<span style="color: #009900;">blunt</span>', #GREEN

	'sticky end': '<span style="color: #b30077;">sticky end</span>', #MAGENTA
	'blunt end': '<span style="color: #009900;">blunt end</span>', #GREEN
	'hanger end': '<span style="color: #0a9bf5;">hanger end</span>', #SKY BLUE
	'straight edge': '<span style="color: #004d99;">straight edge</span>', #NAVY
	'overhang end': '<span style="color: #e65400;">overhang end</span>', #DARK ORANGE
}

#=====================
#=====================
def write_question(N, enzyme_class, use_overhang_type):
	name = restrictlib.html_monospace(enzyme_class.__name__)
	cut_description = restrictlib.html_monospace(restrictlib.format_enzyme(enzyme_class))
	web_data = restrictlib.get_web_data(enzyme_class)
	organism = web_data.get('Organism')

	# Constructing the quiz question
	opening =  '<p>Restriction enzymes are proteins that cut DNA at specific sequences to produce fragments for further study.'
	source = "These enzymes are obtained from various types of bacteria and "
	source += "have the ability to recognize short nucleotide sequences within a larger DNA molecule.</p>"
	setup = f"<p>The restriction enzyme we are focusing on is <strong><i>{name}</i></strong> and is obtained from the bacteria {organism}.</p>"
	cut_info = f"<p><strong><i>{name}</i></strong> cuts the DNA sequence as follows: {cut_description} where the '|' indicates the cut location.</p>"
	prompt = "<p>Based on this info, can you identify the type of cut this enzyme makes?</p>"

	question = " ".join([opening, source, setup, cut_info, prompt])
	#print(question)
	#sys.exit(0)

	overhang = enzyme_class.overhang()

	answer_text = None
	choices_list = []
	if use_overhang_type is True:
		answer_text = overhang
		choices_list = ["5' overhang", "3' overhang", "blunt"]
		choices_list.sort()
	else:
		if overhang.endswith("overhang"):
			answer_text = "sticky end"
		elif overhang == "blunt":
			answer_text = "blunt end"
		# actual choices
		choices_list = ["sticky end", "blunt end"]
		# wrong choices
		choices_list.extend(["hanger end", "straight edge", "overhang end", ])
		random.shuffle(choices_list)

	styled_choices_list = [choice_color_map[choice_key] for choice_key in choices_list]
	styled_answer_text = choice_color_map[answer_text]
	bbquestion = bptools.formatBB_MC_Question(N, question, styled_choices_list, styled_answer_text)
	return bbquestion


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
	parser = argparse.ArgumentParser(description="Generate restriction enzyme questions.")

	# Add an argument to specify the number of duplicate questions to generate
	parser.add_argument(
		'-d', '--duplicates', metavar='#', type=int, dest='duplicates',
		help='Number of duplicate runs to do or number of questions to create',
		default=1
	)

	parser.add_argument("-o", "--overhang_type", default=True, dest='use_overhang_type',
		action="store_true", help="Whether to use overhang type or use end type.")

	parser.add_argument("-e", "--end_type", default=True, dest='use_overhang_type',
		action="store_false", help="Whether to use overhang type or use end type.")

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

	# Generate the output file name based on the script name and question type
	script_name = os.path.splitext(os.path.basename(__file__))[0]
	suffix = 'overhang_type' if args.use_overhang_type else 'end_type'
	outfile = (
		'bbq'
		f'-{script_name}'  # Add the script name to the file name
		f'-{suffix}'
		'-questions.txt'  # Add the file extension
	)

	enzyme_names = restrictlib.get_enzyme_list()
	print(f"Found {len(enzyme_names)} valid restriction enzymes...")
	random.shuffle(enzyme_names)

	# Print a message indicating where the file will be saved
	print(f'Writing to file: {outfile}')

	# Open the output file in write mode
	with open(outfile, 'w') as f:
		# Initialize the question number counter
		N = 0

		# Generate the specified number of questions
		for _ in range(args.duplicates):
			enzyme_name = enzyme_names[N % (len(enzyme_names))]
			enzyme_class = restrictlib.enzyme_name_to_class(enzyme_name)

			# Generate the complete formatted question
			complete_question = write_question(N+1, enzyme_class, args.use_overhang_type)

			# Write the question to the file if it was generated successfully
			if complete_question is not None:
				N += 1
				f.write(complete_question)

	# If the question type is multiple choice, print a histogram of results
	bptools.print_histogram()

	# Print a message indicating how many questions were saved
	print(f'saved {N} questions to {outfile}')

#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END

