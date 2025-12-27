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
	"""
	Create an inline HTML table representing (n over r) with flattened parentheses.

	- Enlarged and lightened parentheses.
	- Adds slightly more horizontal spacing (~3/4 character) between parentheses and numbers.
	- ASCII-safe with HTML numeric entities.
	"""
	choose = ""
	choose += (
		"<table style='display:inline-table;vertical-align:middle;"
		"border-collapse:collapse;border:0;position:relative;top:-0.2em;'>"
	)

	# First row: left paren and top number with wider spacing
	choose += "<tr>"
	choose += (
		" <td rowspan='2' style='text-align:center;vertical-align:middle;padding:0;"
		"margin-right:0.05em;'>"
		"<span style='font-size:xx-large;"
		"transform:scale(1.35);display:inline-block;margin-right:0.05em;'>"
		"&#10222;</span>&nbsp;</td>"
	)
	choose += f" <td style='text-align:center;vertical-align:bottom;padding:0;'>{n}</td>"
	choose += (
		" <td rowspan='2' style='text-align:center;vertical-align:middle;padding:0;"
		"margin-left:0.05em;'>"
		"&nbsp;<span style='font-size:xx-large;"
		"transform:scale(1.35);display:inline-block;margin-left:0.05em;'>"
		"&#10223;</span></td>"
	)
	choose += "</tr>"

	# Second row: bottom number with same spacing
	choose += "<tr>"
	choose += f" <td style='text-align:center;vertical-align:top;padding:0;'>{r}</td>"
	choose += "</tr>"

	choose += "</table>"
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
	if numerator == 1:
		if denominator == 2:
			return "&frac12;"
		elif denominator == 3:
			return "&frac13;"
		elif denominator == 4:
			return "&frac14;"
	elif numerator == 2:
		if denominator == 3:
			return "&frac23;"
	elif numerator == 3:
		if denominator == 4:
			return "&frac34;"

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
	"""
	Generate the full HTML formula for the binomial probability calculation.

	Args:
		n (int): total number of trials.
		s (int): number of successes.
		t (int): number of failures.
		p (float): probability of success.
		q (float): probability of failure.

	Returns:
		str: HTML string containing a formatted equation showing the
		     binomial computation step by step.
	"""
	# Calculate the final probability value
	final_value = choose(n, s) * p**s * q**t

	# Start the HTML table for displaying the full equation
	formula = f"<table style='border-collapse: collapse; border: 1px solid white;'>"
	formula += "<tr>"

	# First term: choose function C(n, s)
	formula += " <td>"
	formula += makeChoose(n, s)
	formula += "</td><td>"

	# Add p^s and q^t components
	ptxt = percent_to_fraction(p)
	formula += f"({ptxt})<sup>{s}</sup>"
	qtxt = percent_to_fraction(q)
	formula += f"&sdot;({qtxt})<sup>{t}</sup>"

	# Begin showing expanded equality steps
	formula += "</td><td>"
	formula += "&nbsp;=&nbsp;"
	formula += "</td><td>"
	formula += makeChooseLong(n, s)
	formula += "</td><td>"

	# Show power terms depending on whether p and q are equal
	if abs(p - q) < 1e-4:
		formula += f"({ptxt})<sup>{n}</sup>"
	else:
		formula += f"({ptxt})<sup>{s}</sup>"
		formula += f"&sdot;({qtxt})<sup>{t}</sup>"

	# Continue equality chain
	formula += "</td><td>"
	formula += "&nbsp;=&nbsp;"
	formula += "</td><td>"
	formula += makeChooseCancelled(n, s)
	formula += "</td><td>"
	formula += "&times;"
	formula += "</td><td>"

	# Multiply the fraction components
	if abs(p - q) < 1e-4:
		formula += combinePowerFractions(p, n, 1, 1)
	else:
		formula += combinePowerFractions(p, s, q, t)

	formula += "</td><td>"
	formula += "&nbsp;=&nbsp;"
	formula += "</td><td>"

	# Compute numeric combination and fraction breakdown
	c = choose(n, s)
	a, b = decimal_to_fraction_parts(p**s * q**t)

	# Display fractions in simplified or raw form
	if 1 < a < 1000:
		formula += makeFraction(f"{c}&times;{a}", f"{b}")
	elif a == 1:
		formula += makeFraction(f"{c}", f"{b}")

	# Display final numeric and percentage results
	formula += "</td><td>"
	formula += "&nbsp;=&nbsp;"
	formula += "</td><td>"
	formula += f"{final_value:.4f}"
	formula += "</td><td>"
	formula += "<strong>&nbsp;=&nbsp;</strong>"
	formula += "</td><td>"
	formula += f"<strong>{final_value * 100:.1f}%</strong>"
	formula += "</td>"
	formula += "</tr></table>"

	# Return the complete formula HTML
	return formula

#============================================================
#============================================================
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
	question_text += f"<p style='margin:2px 0;color:#444;'>"
	question_text += f"<strong>Model:</strong> Binomial &rarr; "
	question_text += f"{makeChoose('n', 'k')}&sdot;p<sup>k</sup>&sdot;q<sup>n-k</sup>"
	question_text += f"</p>"

	question_text += f"<p>"
	question_text += f"In this scenario, assume that each child is born independently "
	question_text += f"with the same chance of being either sex. The event outcomes "
	question_text += f"are mutually exclusive, so we can apply the binomial model to "
	question_text += f"determine the probability of a specific combination.</p>"

	# Main question stem
	question_text += f"<p>"
	question_text += f"A woman has <strong>{num2txt[total_offspring]} "
	question_text += f"({total_offspring})</strong> children. "
	question_text += f"What is the probability that she has exactly "
	question_text += f"<span style='color:{color_boys};'><strong>{num2txt[male_offspring]} "
	question_text += f"({male_offspring}) boys &male;</strong></span> and "
	question_text += f"<span style='color:{color_girls};'><strong>{num2txt[female_offspring]} "
	question_text += f"({female_offspring}) girls &female;</strong></span>? "
	question_text += f"</p>"

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




