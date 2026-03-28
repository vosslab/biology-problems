#!/usr/bin/env python3

# Standard Library
import math
import random

# Local repo modules
import bptools

# Fixed substrate concentrations spanning 5 orders of magnitude (mM)
S_VALUES = [
	0.001, 0.002, 0.005, 0.010, 0.020, 0.050,
	0.100, 0.200, 0.500, 1.000, 10.000, 100.000,
]

# Possible Km values are a subset of S_VALUES (middle of table range)
KM_CHOICES = [0.005, 0.010, 0.020, 0.050, 0.100]

# Module-level scenario list, initialized in main()
SCENARIOS = None

#============================================
#============================================
def michaelis_menten(substrate_conc: float, km: float, vmax: float) -> float:
	"""
	Calculate initial velocity using the Michaelis-Menten equation.

	Args:
		substrate_conc (float): Substrate concentration [S].
		km (float): Michaelis constant.
		vmax (float): Maximum velocity.

	Returns:
		float: Initial velocity V0 rounded to 1 decimal place.
	"""
	v0 = vmax * substrate_conc / (km + substrate_conc)
	# round to 1 decimal place
	v0_rounded = math.ceil(v0 * 10.0) / 10.0
	return v0_rounded

#============================================
#============================================
def make_data_table(km: float, vmax: float) -> str:
	"""
	Build an HTML table of substrate concentration vs initial velocity.

	Args:
		km (float): Michaelis constant.
		vmax (float): Maximum velocity.

	Returns:
		str: HTML table string.
	"""
	# monospace span for numeric alignment
	mono_span = "<span style='font-family: courier, monospace;'>"

	# start the table
	table = "<table cellpadding='2' cellspacing='2' "
	table += "style='text-align: center; border-collapse: collapse; "
	table += "border: 1px solid black; font-size: 14px;'>"

	# column widths
	col_width = 160
	for _ in range(2):
		table += f"<colgroup width='{col_width}'></colgroup> "

	# header row
	table += "<tr style='background-color: lightgray; border-bottom: 2px solid black;'>"
	table += "<th align='center' style='padding: 5px; font-size: 12px;'>"
	table += "substrate<br/>concentration, "
	table += "<span style='font-size: 14px;'>[S]</span></th>"
	table += "<th align='center' style='padding: 5px; font-size: 12px;'>"
	table += "initial reaction<br/>velocity<br/>"
	table += "<span style='font-size: 14px;'>V<sub>0</sub></span></th>"
	table += "</tr>"

	# data rows
	for i, s_val in enumerate(S_VALUES):
		v0 = michaelis_menten(s_val, km, vmax)
		# alternate row colors
		bgcolor = "#FFFFDD" if i % 2 == 0 else "#FFFFFF"
		table += f"<tr style='background-color: {bgcolor};'>"
		# format substrate concentration
		s_str = f"{s_val:.3f}"
		table += " <td style='border: 1px solid black;' align='right'>"
		table += f"{mono_span}{s_str}&nbsp;</span></td>"
		# format velocity
		table += " <td style='border: 1px solid black;' align='right'>"
		table += f"{mono_span}{v0:.1f}&nbsp;</span></td>"
		table += "</tr>"
		# stop if we are very close to Vmax
		if (vmax - v0) < 0.099:
			break

	table += "</table>"
	return table

#============================================
#============================================
def _get_scenarios() -> list:
	"""
	Generate all (Km, Vmax) scenario combinations.

	Returns:
		list: Each entry is (km, vmax).
	"""
	# Vmax choices: 80 to 200 in steps of 5
	vmax_choices = list(range(80, 201, 5))
	scenarios = []
	for km in KM_CHOICES:
		for vmax in vmax_choices:
			scenarios.append((km, vmax))
	return scenarios

#============================================
#============================================
def write_question(N: int, args) -> str:
	"""
	Creates a complete formatted MC question for Km determination from a table.

	Args:
		N (int): The question number.
		args (argparse.Namespace): Parsed command-line arguments.

	Returns:
		str: A formatted question string.
	"""
	if SCENARIOS is None:
		raise ValueError("Scenarios not initialized; run main().")
	# select scenario using modulo
	idx = (N - 1) % len(SCENARIOS)
	km, vmax = SCENARIOS[idx]

	# build the data table
	data_table = make_data_table(km, vmax)

	# build question text
	question_text = ""
	question_text += "<p><u>Michaelis-Menten question.</u> "
	question_text += "The following question refers to the table "
	question_text += "(<i>below</i>) of enzyme activity.</p>"
	question_text += data_table
	question_text += "<br/>"
	question_text += "<p>Using the table (<i>above</i>), calculate the value "
	question_text += "for the Michaelis-Menten constant, K<sub>M</sub>.</p>"

	# build choices: all 5 Km values in ascending order
	mono_span = "<span style='font-family: courier, monospace;'>"
	choices_list = []
	answer_text = None
	for k in KM_CHOICES:
		k_str = f"{k:g}"
		choice_text = f"K<sub>M</sub> = {mono_span}{k_str}</span> mM"
		choices_list.append(choice_text)
		if abs(k - km) < 1e-8:
			answer_text = choice_text

	# format as MC question
	complete_question = bptools.formatBB_MC_Question(
		N, question_text, choices_list, answer_text
	)
	return complete_question

#============================================
#============================================
def parse_arguments():
	"""
	Parses command-line arguments for the script.

	Returns:
		argparse.Namespace: Parsed arguments.
	"""
	parser = bptools.make_arg_parser(
		description="Generate Michaelis-Menten Km-from-table questions."
	)
	parser = bptools.add_scenario_args(parser)
	args = parser.parse_args()
	return args

#============================================
#============================================
def main():
	"""
	Main function that orchestrates question generation and file output.
	"""
	args = parse_arguments()

	# initialize scenarios
	global SCENARIOS
	SCENARIOS = _get_scenarios()
	if args.scenario_order == 'random':
		random.shuffle(SCENARIOS)
	if args.max_questions is None or args.max_questions > len(SCENARIOS):
		args.max_questions = len(SCENARIOS)

	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)

#============================================
#============================================
if __name__ == '__main__':
	main()

## THE END
