#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
# Provides functions for interacting with the operating system
import os
import time
# Provides functions to generate random numbers and selections
import random
# Provides tools to parse command-line arguments
import argparse
# Provides custom functions, such as question formatting and other utilities
import statistics

# Import external modules (pip-installed)
# No external modules are used here currently

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities
import bptools

#============================================
def get_raw_data() -> list[int]:
	"""
	Return the raw dataset used in the question.

	Returns:
		list[int]: A list of integers for descriptive statistics.
	"""
	#list must have a whole number mean, median
	#list must contain an explicit mode value
	#values are unique: mean != median != mode
	#numbers are less than 10? less than 100?
	#generate exactly 10 integers

	# sample 9 unique ints
	data = random.sample(range(10, 90), 9)
	data.sort()

	# choose an index to duplicate that will not be part of the median pair after append+sort
	# valid indices avoid 3,4,5 which become near-median positions; also leave a high slot to tune mean
	valid_choices = [0, 1, 2, 6, 7]
	mode_value = data[random.choice(valid_choices)]
	#print(f"mode_value: {mode_value}")

	# duplicate to create a clear mode
	data.append(mode_value)
	data.sort()
	#print(f"initial data: {data}")

	#fix half median values
	#print(f"median_value: {(data[4] + data[5])/2.0:.1f}")
	print(data)

	if (data[4] + data[5]) % 2 == 1:
		data[5] += 1
		# preserve strict increase and avoid a new duplicate
		if data[5] == data[6]:
			data[6] += 1
			if data[6] == data[7]:
				data[7] += 1
				if data[7] == data[8]:
					data[8] += 1
					if data[8] == data[9]:
						data[9] += 1
	#print(f"fixed data: {data}")
	#print(f"median_value: {(data[4] + data[5])/2.0:.1f}")

	remainder = sum(data) % 10
	data[-1] += (10 - remainder)
	#print(f"data sum: {sum(data)}")

	data.sort()
	#print(f"final data: {data}\n")

	# validations
	median_is_int = ((data[4] + data[5]) % 2 == 0)
	sum_is_multiple_of_10 = (sum(data) % 10 == 0)
	unique_count = len(set(data))
	mode_count = max({x: data.count(x) for x in data}.values())
	mode_key = max({x: data.count(x) for x in data}, key=lambda k: data.count(k))

	print(data)

	# basic assertions within 100 chars
	assert len(data) == 10
	assert unique_count == 9
	assert median_is_int
	assert sum_is_multiple_of_10
	assert mode_count >= 2
	assert mode_key == mode_value
	assert 1 <= min(data) and max(data) <= 99

	random.shuffle(data)
	return data

# Simple assertion test for the function: 'get_raw_data'
assert len(get_raw_data()) == 10

#============================================
def get_question_text(data) -> str:
	"""
	Generates and returns the main text for the Blackboard FIB_PLUS question.

	Returns:
		str: The HTML-formatted question stem.
	"""
	# make sure we only print integers
	data_html = "<br/>".join(f"{x:d}" for x in data)

	question_text = ""

	question_text += "<p><b>Purpose:</b> "
	question_text += "This assignment will help you practice making your own copy of a  "
	question_text += "Google Sheet template and using with for statistical calculations. "
	question_text += "Throughout this course, we will use Google Sheets regularly. "
	question_text += "Take some time to look at the formulas in the sheet and notice how they work.</p>"

	question_text += "<p>Follow these steps carefully:</p> "
	question_text += "<p>(1) Open the Google Sheet Template: "
	question_text += "<a href='https://docs.google.com/spreadsheets/d/"
	question_text += "1aFRtB8W_01eL-4hUyB5DiiuhRD-vd1Tn0mpCfSQN96g/edit' target='_blank' rel='noopener'>"
	question_text += "Google Sheet Template</a></p> "
	question_text += "<p>(2) Go to <b>File &rarr; Make a copy</b> to create your own version.</p> "
	question_text += "<p>(3) Enter the following numbers into the <b>Raw Data</b> column:</p> "
	question_text += "<p>"
	question_text += f"<span style='font-family: monospace; background-color:#eee;'>{data_html}</span> "
	question_text += "</p>"
	question_text += "<p>(4) Once the data is entered, look at the "
	question_text += "<b>Descriptive Statistics</b> column and enter the following values here:</p> "
	question_text += "<ul><li>Mean [MEAN]</li><li>Median [MEDIAN]</li>"
	question_text += "<li>Mode [MODE]</li><li>Range [RANGE]</li></ul> "
	question_text += "<p><b>Important:</b> Report each answer as a whole number only "
	question_text += "(no decimals).</p>"
	return question_text

#============================================
def generate_answer_map(data: list) -> dict:
	"""
	Generates the FIB_PLUS answer map by computing
	descriptive statistics from the dataset.

	Args:
		num_choices (int): Unused for FIB_PLUS, but kept for compatibility.

	Returns:
		dict: Mapping of variable names to lists of accepted answers.
	"""
	answer_map = {
		"MEAN": [f"{statistics.mean(data):.0f}"],
		"MEDIAN": [f"{statistics.median(data):.0f}"],
		"MODE": [f"{statistics.mode(data):.0f}"],
		"RANGE": [f"{max(data) - min(data):d}"],
	}
	return answer_map

#============================================
def write_question(N: int) -> str:
	"""
	Creates a complete formatted FIB_PLUS question row.

	Args:
		N (int): Question number.
		num_choices (int): Kept for API compatibility.

	Returns:
		str: Formatted Blackboard FIB_PLUS question row.
	"""
	data = get_raw_data()
	question_text = get_question_text(data)
	answer_map = generate_answer_map(data)
	complete_question = bptools.formatBB_FIB_PLUS_Question(N, question_text, answer_map)
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

	# Create the specified number of questions
	for _ in range(args.duplicates):
		# Generate gene letters (if needed by question logic)
		gene_letters_str = bptools.generate_gene_letters(3)

		# Create a full formatted question (Blackboard format)
		t0 = time.time()
		complete_question = write_question(N+1)
		if time.time() - t0 > 1:
			print(f"Question {N+1} complete in {time.time() - t0:.1f} seconds")

		# Append question if successfully generated
		if complete_question is not None:
			N += 1
			question_bank_list.append(complete_question)

		if N >= args.max_questions:
			break

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
