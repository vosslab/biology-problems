#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

# Import built-in Python modules
# Provides functions for interacting with the operating system
import os
# Provides functions to generate random numbers and selections
import random
# Provides custom functions, such as question formatting and other utilities
import statistics

# Import external modules (pip-installed)
# No external modules are used here currently

# Import local modules from the project
# Provides custom functions, such as question formatting and other utilities
import bptools


# fixed names file
NAMES_FILE = os.path.abspath(
	os.path.join(os.path.dirname(__file__), "..", "data", "student_names.txt")
)

#============================================
def load_unique_initial_names(k: int = 8) -> list[str]:
	"""
	Load names from student_names.txt and return k names with unique initials.

	Args:
		k (int): Number of names to select.

	Returns:
		list[str]: Selected names with distinct initials.
	"""
	assert k < 25

	with open(NAMES_FILE, 'r', encoding='ascii') as f:
		all_names = [line.strip() for line in f if line.strip()]

	random.shuffle(all_names)

	seen = set()
	chosen = []
	for name in all_names:
		initial = name[0].upper()
		if initial not in seen:
			seen.add(initial)
			chosen.append(name)
			if len(chosen) == k:
				break

	chosen.sort()
	assert len(chosen) == k
	return chosen

#============================================
def synthesize_bp_dataset(mu: int = 120, sd: int = 15) -> list[int]:
	"""
	Build an 8-value systolic BP dataset by sampling Z-brackets relative to a
	population mean and SD, then return integer BP values.
	"""
	# epsilon keeps samples away from exact bin edges
	eps = 0.06
	brackets = [
		(-3.0, -2.1),
		(-1.4, -1.2),
		( 1.2,  1.4),
		( 2.1,  2.8),
		(-0.7,  0.0),
		( 0.0,  0.7),
		(-0.7,  0.0),
		( 0.0,  0.7),
	]

	z_vals = []
	for low, high in brackets:
		z = random.uniform(low + eps, high - eps)
		z = round(z, 3)
		z_vals.append(z)

	z_vals.sort()

	mean_val = statistics.mean(z_vals)
	std_val = statistics.stdev(z_vals)
	print(z_vals)
	print(f"mean_val= {mean_val}")
	print(f"std_val= {std_val}")

	# convert Z to BP values
	values = []
	for z in z_vals:
		v = int(round(mu + z * sd))
		values.append(v)
	print(values)

	# light shuffle for presentation
	random.shuffle(values)

	# simple assertion test for count only
	assert len(values) == 8

	return values

#============================================
def make_copy_paste_block(names: list[str], bp: list[int]) -> str:
	"""
	Build an HTML table block for Name + BP spreadsheet copy.

	Args:
		names (list[str]): Patient names.
		bp (list[int]): Systolic BP values.

	Returns:
		str: HTML table wrapped in a <p> block.
	"""
	rows = "".join(f"<tr><td>{n}</td><td>{v}</td></tr>" for n, v in zip(names, bp))

	block_html = ""
	block_html += "<br/>"
	block_html += (
		"<table border='1' style='border-collapse:collapse; "
		"font-family: monospace; background-color:#eee;'>"
		"<tr><th>Patient Name</th><th>Systolic BP (mmHg)</th></tr>"
		f"{rows}</table><br/>"
	)

	return block_html

#============================================
def get_question_text(names: list[str], bp: list[int], target_z_lower: int) -> str:
	"""
	Create the HTML stem instructing Sheets Z-score workflow.

	Args:
		names (list[str]): Patient names.
		bp (list[int]): BP values.
		target_z_lower (int): Lower bound of target Z bracket (-3, -2, 1, or 2).

	Returns:
		str: HTML-formatted Blackboard question text.
	"""
	block_html = make_copy_paste_block(names, bp)

	google_drive_id = "1y-fVDSLoRPGuCABAD5gy-Ai4qzSFqqhnayOI4kMpPkQ"

	# start assembling the question stem
	question_text = ""
	question_text += "<p><b>Purpose:</b> Practice calculating Z-scores in Google Sheets "
	question_text += "using the population mean (&mu;, mu = 120) and population standard deviation "
	question_text += "(&sigma;, sigma = 15).</p>"
	question_text += "<p>Follow these steps:</p>"
	question_text += "<ol>"
	question_text += "<li>Open the Google Sheet Template: "
	question_text += f"<a href='https://docs.google.com/spreadsheets/d/{google_drive_id}/edit' "
	question_text += "target='_blank' rel='noopener'>Google Sheet Template</a></li>"
	question_text += "<li>File &rarr; Make a copy.</li>"
	question_text += "<li>Paste the table below into the sheet (two columns: Name and BP).</li>"
	question_text += "<li>Use &mu; = 120 and &sigma; = 15 to compute Z for each BP.</li>"
	question_text += "<li>Formula hint: "
	question_text += "<span style='font-family: monospace;'>(B2 - &mu;)/&sigma;</span>. "
	question_text += "Here <b>B2</b> means the first BP value in column B. "
	question_text += "After typing the formula in the first row, place your mouse on the small square "
	question_text += "in the bottom-right corner of the cell (the fill handle) and drag it down. "
	question_text += "The spreadsheet will automatically change B2 to B3 for the next row, then B4, and so on, "
	question_text += "so each patient's BP gets its own Z-score.</li>"
	question_text += "<li><i>Pro Tip:</i> Advanced users can highlight the formula cell and the rows below it, "
	question_text += "then press &#8984;D (Mac) or Ctrl+D (Windows) to autofill the formula quickly.</li>"
	question_text += "</ol>"

	# insert the data table
	question_text += block_html

	# add the targeted Z-score question
	question_text += "<p><b>Question:</b> Which named patient has a Z-score "
	question_text += f"between {target_z_lower:+d} and {target_z_lower+1:+d} standard deviations?</p>"

	# return the final HTML
	return question_text

#============================================
def generate_choices(target_z_lower: int, num_choices: int, names: list[str], bp: list[int]) -> tuple[list[str], str]:
	"""
	Generate multiple choice options in the format 'Name with a BP of X' and
	return both the list of choices and the correct answer.

	Always includes the min and max BP values. If the correct answer is the min,
	then also include the second min. If the correct answer is the max, then also
	include the second max.

	Args:
		target_z_lower (int): Lower bound of the target Z bracket (-3, -2, 1, or 2).
		num_choices (int): Number of answer options to output.
		names (list[str]): Patient names.
		bp (list[int]): Systolic BP values.

	Returns:
		tuple: (choices_list, answer_text)
	"""
	mu = 120
	sigma = 15

	pairs = list(zip(names, bp))
	z_by_pair = {pair: (pair[1] - mu) / sigma for pair in pairs}

	# pick correct pair from target interval
	z_lo, z_hi = float(target_z_lower), float(target_z_lower + 1)
	correct_pair = None
	for pair, z in z_by_pair.items():
		if z_lo < z < z_hi:
			correct_pair = pair
			break
	if correct_pair is None:
		center = (z_lo + z_hi) / 2.0
		correct_pair = min(z_by_pair.keys(), key=lambda p: abs(z_by_pair[p] - center))

	# find min/max and second min/max
	sorted_pairs = sorted(pairs, key=lambda p: p[1])
	min_pair = sorted_pairs[0]
	second_min_pair = sorted_pairs[1]
	max_pair = sorted_pairs[-1]
	second_max_pair = sorted_pairs[-2]

	# required choices
	required = {correct_pair, min_pair, max_pair}

	# if correct is min → add second min
	if correct_pair == min_pair:
		required.add(second_min_pair)

	# if correct is max → add second max
	if correct_pair == max_pair:
		required.add(second_max_pair)

	# fill in remaining choices
	others = [p for p in pairs if p not in required]
	random.shuffle(others)
	while len(required) < num_choices and others:
		required.add(others.pop())

	# final choice list and answer
	choice_pairs = list(required)
	choices_list = [f"{n} with a BP of {v}" for (n, v) in choice_pairs]
	answer_text = f"{correct_pair[0]} with a BP of {correct_pair[1]}"

	# optional stable sort (or shuffle if you prefer random order)
	choices_list.sort()

	return choices_list, answer_text

#============================================
def write_question(N: int, args) -> str:
	"""
	Create one Blackboard MC question row with Z-score targeting.

	Args:
		N (int): Question number.
		num_choices (int): Number of answer options.

	Returns:
		str: Blackboard formatted MC question.
	"""
	names = load_unique_initial_names(8)
	bp = synthesize_bp_dataset()

	target_z_lower = random.choice([-3,-2,1,2])

	question_text = get_question_text(names, bp, target_z_lower)
	choices_list, answer_text = generate_choices(target_z_lower, args.num_choices, names, bp)

	# Uses the provided bptools function signature
	complete_question = bptools.formatBB_MC_Question(
		N,
		question_text,
		choices_list,
		answer_text
	)
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

	outfile = bptools.make_outfile(None)
	bptools.collect_and_write_questions(write_question, args, outfile)

#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END
