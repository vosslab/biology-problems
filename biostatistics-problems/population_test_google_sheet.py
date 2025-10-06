#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
# Provides functions for interacting with the operating system
import os
import time
import math
# Provides functions to generate random numbers and selections
import random
# Provides tools to parse command-line arguments
import argparse
import statistics

# Import external modules (pip-installed)
# No external modules are used here currently

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities
import bptools

#============================================
def normal_cdf(z: float) -> float:
	"""
	Compute Phi(z), the standard normal CDF, using math.erf.

	Args:
		z (float): Z value.

	Returns:
		float: Cumulative probability P(Z <= z).
	"""
	p = 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))
	return p

# Simple assertion test for the function: 'normal_cdf'
assert 0.499 < normal_cdf(0.0) < 0.501

#============================================
def generate_baby_weights(n: int, mu: float = 7.5, sigma: float = 1.5) -> list[float]:
	"""
	Generate n baby weights in pounds with one decimal place, sampled around
	mu plus a small positive shift so xbar > mu.

	Args:
		n (int): Sample size.
		mu (float): Population mean.
		sigma (float): Population standard deviation.

	Returns:
		list[float]: List of n weights rounded to one decimal place.
	"""
	# shift keeps the one tailed direction consistent
	shift = round(random.uniform(0.10, 0.60), 2)
	target_mu = mu + shift

	values = []
	for _ in range(n):
		# Box Muller like sampling via Gaussian from random
		v = random.gauss(target_mu, sigma)
		# keep weights in a reasonable newborn range
		v = max(4.0, min(12.0, v))
		# one decimal place as in typical clinical recording
		values.append(round(v, 1))

	# ensure at least slight elevation of mean
	if statistics.mean(values) <= mu:
		# nudge the largest value up by 0.2 if needed
		i = max(range(n), key=lambda k: values[k])
		values[i] = round(min(12.0, values[i] + 0.2), 1)

	# simple assertion tests
	assert len(values) == n
	assert min(values) >= 4.0 and max(values) <= 12.0

	return values

#============================================
def compute_one_tailed_pvalue(weights: list[float], mu: float, sigma: float) -> tuple[float, float]:
	"""
	Compute Z and one tailed p value for testing mean > mu with known sigma.

	Args:
		weights (list[float]): Sample data.
		mu (float): Population mean.
		sigma (float): Population standard deviation.

	Returns:
		tuple[float, float]: (z_stat, p_one_tailed)
	"""
	n = len(weights)
	xbar = statistics.fmean(weights)
	z = (xbar - mu) / (sigma / math.sqrt(n))
	p = 1.0 - normal_cdf(z)
	return z, p
# Simple assertion test for the function: 'compute_one_tailed_pvalue'
_test = [7.6, 7.7, 7.8, 7.9, 8.0, 7.6, 7.7, 7.8, 7.9, 8.0]
_z, _p = compute_one_tailed_pvalue(_test, 7.5, 1.5)
assert 0.0 <= _p <= 1.0

#============================================
def format_question_html(weights: list[float]) -> str:
	"""
	Build the Blackboard FIB_PLUS stem. Students compute a one tailed p value.

	Args:
		weights (list[float]): Baby weights in pounds.

	Returns:
		str: HTML formatted question stem with a single blank [PVALUE].
	"""
	rows = "<br/>".join(f"{w:.1f}" for w in weights)
	tutorial_link = "https://docs.google.com/document/d/1ZOLIw-JlNA6Mry1w0t5I5Ffgi7RMiBCSr7VtyNgsdt0/edit"

	q = ""
	q += "<p><b>Joe's Hospital of Fried Foods vs National Average</b></p>"
	q += "<p>Use a one tailed Z test for H1: mu_hospital > mu.</p>"
	q += "<p>Fixed population values: &mu; = 7.5 lbs, &sigma; = 1.5 lbs.</p>"
	q += "<p>Sample weights (lbs), enter into a single column in Google Sheets:</p>"
	q += f"<p><span style='font-family: monospace; background-color:#eee;'>{rows}</span></p>"
	q += "<p>Compute the one tailed p value using the tutorial workflow, "
	q += "from last week: "
	q += f"<a href='{tutorial_link}' target='_blank' rel='noopener'>link here</a>"
	q += "</p>"
	q += "<p>Your answer will be a decimal value between 0 and 1.</p>"
	return q

#===========================================================
#===========================================================
# This function creates and formats a complete question for output.
def write_question(N: int) -> str:
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
	n = random.randint(25, 39)
	weights = generate_baby_weights(n)
	question_text = format_question_html(weights)
	z_stat, p_value = compute_one_tailed_pvalue(weights, 7.5, 1.5)

	answer_float = p_value
	#tolerance range of 1%
	tolerance_float = answer_float * 0.01

	# Format the question using a helper function from the bptools module
	complete_question = bptools.formatBB_NUM_Question(N, question_text, answer_float,
										tolerance_float, tol_message=False)

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
