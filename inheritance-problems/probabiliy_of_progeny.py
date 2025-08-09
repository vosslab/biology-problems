#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
# Provides functions for interacting with the operating system
import os
# Provides functions to generate random numbers and selections
import random
# Provides tools to parse command-line arguments
import argparse
import math

# Import external modules (pip-installed)
# No external modules are used here currently

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities
import bptools

#===========================================================
#===========================================================
def choose(n, r):
	f = math.factorial
	nint = int(n)
	rint = int(r)
	c =  f(nint) // (f(rint) * f(nint - rint))
	return c

#===========================================================
#===========================================================
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
def makeChoose(n, r):
	choose = ""
	choose += "<table style='border-collapse: collapse; border: 1px solid white;'>"
	choose += "<tr>"
	choose += " <td rowspan='2' style='text-align: center; vertical-align: middle;'>"
	choose += "  <span style='font-size: x-large;'>&lpar;</span></td>"
	choose += " <td style='text-align: center; vertical-align: middle;'>{0}</td>".format(n)
	choose += " <td rowspan='2' style='text-align: center; vertical-align: middle;'>"
	choose += "  <span style='font-size: x-large;'>&rpar;</span></td>"
	choose += "</tr><tr>"
	choose += " <td style='text-align: center; vertical-align: middle;'>{0}</td>".format(r)
	choose += "</tr></table>"
	return choose

#===========================================================
#===========================================================
def makeChooseLong(n, r):
	numerator = "{0}!".format(n)
	denominator = "({0}&ndash;{1})!&nbsp;&sdot;&nbsp;{1}!".format(n, r)
	fraction = makeFraction(numerator, denominator)
	return fraction

#===========================================================
#===========================================================
def makeFraction(numerator, denominator):
	fraction = ""
	fraction += "<table style='border-collapse: collapse; border: 1px solid white;'>"
	fraction += "<tr>"
	fraction += " <td style='text-align: center; vertical-align: middle; border-bottom: 1px solid black;'>"
	fraction += "&nbsp;"+numerator+"&nbsp;"
	fraction += " </td>"
	fraction += "</tr><tr>"
	fraction += " <td style='text-align: center; vertical-align: middle; border-top: 1px solid black;'>"
	fraction += "&nbsp;"+denominator+"&nbsp;"
	fraction += " </td>"
	fraction += "</tr></table>"
	return fraction

#===========================================================
#===========================================================
def decimal_to_fraction_parts(p):
	if abs(p - 1/3.) < 1e-4:
		a = 1
		b = 3
	elif abs(p - 2/3.) < 1e-4:
		a = 2
		b = 3
	else:
		a, b = (p).as_integer_ratio()
	return a, b

#===========================================================
#===========================================================
def combinePowerFractions(p, s, q, t):
	a, b = decimal_to_fraction_parts(p)
	c, d = decimal_to_fraction_parts(q)
	numerator = ""
	if a > 1:
		numerator += "{0}<sup>{1}</sup>".format(a, s)
	if c > 1:
		numerator += "{0}<sup>{1}</sup>".format(c, t)
	if a == 1 and c == 1:
		numerator += "1"
	denominator = ""
	if b > 1:
		denominator += "{0}<sup>{1}</sup>".format(b, s)
	if d > 1:
		denominator += "{0}<sup>{1}</sup>".format(d, t)
	if b == 1 and d == 1:
		denominator += "1"

	fraction = makeFraction(numerator, denominator)
	return fraction

#===========================================================
#===========================================================
def makeChooseCancelled(n, r):
	numerator = ""
	if n == r:
		numerator += "{0}".format(1)
	elif n == r+1:
		numerator += "{0}".format(n)
	else:
		for i in range(n, r+1, -1):
			numerator += "{0}".format(i)
			numerator += "&sdot;"
		numerator += "{0}".format(r+1)

	denominator = ""
	if n == r:
		denominator += "{0}".format(1)
	elif n == r+1:
		denominator += "{0}".format(1)
	else:
		for i in range(r, 2, -1):
			denominator += "{0}".format(i)
			denominator += "&sdot;"
		denominator += "{0}".format(2)

	fraction = makeFraction(numerator, denominator)
	#fraction += "{0}&ndash;{1}".format(n, r)
	return fraction

#===========================================================
#===========================================================
def percent_to_fraction(p):
	if abs(p - 0.5) < 1e-4:
		ptxt = "<span style='font-size: large;'>&frac12;</span>"
	elif abs(p - 0.25) < 1e-4:
		ptxt = "<span style='font-size: large;'>&frac14;</span>"
	elif abs(p - 0.75) < 1e-4:
		ptxt = "<span style='font-size: large;'>&frac34;</span>"
	elif abs(p - 1/3.) < 1e-4:
		ptxt = "<span style='font-size: large;'>&#8531;</span>"
	elif abs(p - 2/3.) < 1e-4:
		ptxt = "<span style='font-size: large;'>&#8532;</span>"
	elif abs(p*10.0 - int(p*10)) < 1e-4:
		ptxt = "{0:.1f}".format(p)
	else:
		ptxt = "{0:.2f}".format(p)
	return ptxt

#===========================================================
#===========================================================
def makeFormula(n, s, t, p, q):
	###
	# n = total
	# s = # of p
	# t = # of q
	# p = prob. of s
	# q = prob. of t
	final_value = choose(n, s) * p**s * q**t
	formula = "<table style='border-collapse: collapse; border: 1px solid white;'>"
	formula += "<tr>"
	formula += " <td>"
	formula += makeChoose(n, s)
	formula += "</td><td>"
	ptxt = percent_to_fraction(p)
	formula += "({0})<sup>{1}</sup>".format(ptxt, s)
	qtxt = percent_to_fraction(q)
	formula += "&sdot;({0})<sup>{1}</sup>".format(qtxt, t)
	formula += "</td><td>"
	formula += "&nbsp;=&nbsp;"
	formula += "</td><td>"
	formula += makeChooseLong(n, s)
	formula += "</td><td>"
	if abs(p - q) < 1e-4:
		formula += "({0})<sup>{1}</sup>".format(ptxt, n)
	else:
		formula += "({0})<sup>{1}</sup>".format(ptxt, s)
		formula += "&sdot;({0})<sup>{1}</sup>".format(qtxt, t)
	formula += "</td><td>"
	formula += "&nbsp;=&nbsp;"
	formula += "</td><td>"
	formula += makeChooseCancelled(n, s)
	formula += "</td><td>"
	formula += "&times;"
	formula += "</td><td>"
	if abs(p - q) < 1e-4:
		formula += combinePowerFractions(p, n, 1, 1)
	else:
		formula += combinePowerFractions(p, s, q, t)
	formula += "</td><td>"
	formula += "&nbsp;=&nbsp;"
	formula += "</td><td>"
	c = choose(n, s)
	#formula += "{0:d}".format(c)
	#formula += "</td><td>"
	a, b = decimal_to_fraction_parts(p**s * q**t)
	if 1 < a < 1000:
		formula += makeFraction(str(c)+"&times;"+str(a), str(b))
	elif a == 1:
		formula += makeFraction(str(c), str(b))
	formula += "</td><td>"
	formula += "&nbsp;=&nbsp;"
	formula += "</td><td>"
	formula += "{0:.4f}".format(final_value)
	formula += "</td><td>"
	formula += "<strong>&nbsp;=&nbsp;</strong>"
	formula += "</td><td>"
	formula += "<strong>{0:.1f}%</strong>".format(final_value*100)
	formula += "</td>"
	formula += "</tr></table>"
	#print(formula)
	return formula

#===========================================================
#===========================================================
def write_question(N, min_offspring, max_offspring):
	total_offspring = random.randint(min_offspring, max_offspring)
	female_offspring = random.randint(2, total_offspring-2)
	male_offspring = total_offspring - female_offspring

	question_text = ""
	question_text += f"<p>A woman has {num2txt[total_offspring]} ({total_offspring}) children, "
	question_text += f"what is the probability that she has exactly "
	question_text += f"{num2txt[male_offspring]} ({male_offspring}) boys and "
	question_text += f"{num2txt[female_offspring]} ({female_offspring}) girls?</p>"

	# Initialize the list of answer choices
	choices_list = []

	# Correct answer: probability with equal 0.5 chance for each sex
	answer_text = makeFormula(total_offspring, male_offspring, female_offspring, 0.5, 0.5)
	choices_list.append(answer_text)

	# Wrong choice: probability assuming 0.75 male, 0.25 female
	wrong1 = makeFormula(total_offspring, male_offspring, female_offspring, 0.75, 0.25)
	choices_list.append(wrong1)

	# Wrong choice: probability assuming 0.25 male, 0.75 female
	wrong2 = makeFormula(total_offspring, male_offspring, female_offspring, 0.25, 0.75)
	choices_list.append(wrong2)

	# Pick the larger and smaller counts to avoid branching on sex
	big = max(male_offspring, female_offspring)
	small = min(male_offspring, female_offspring)

	# Always-generate wrong3; wrong4 only if counts are unequal
	wrong3 = makeFormula(big, small, big, 0.5, 0.5)
	choices_list.append(wrong3)
	if male_offspring != female_offspring:
		wrong4 = makeFormula(big, big, small, 0.5, 0.5)
		choices_list.append(wrong4)

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

	# Add argument for minimum offspring total
	parser.add_argument(
		'--min', '--min-offspring', type=int, dest='min_offspring',
		default=5, help='Minimum total number of offspring to consider.'
	)

	# Add argument for maximum offspring total
	parser.add_argument(
		'--max', '--max-offspring', type=int, dest='max_offspring',
		default=10, help='Maximum total number of offspring to consider.'
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
		complete_question = write_question(N+1, args.min_offspring, args.max_offspring)

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






