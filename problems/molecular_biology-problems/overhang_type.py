#!/usr/bin/env python3
# ^^ Specifies the Python3 environment to use for script execution

import random

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

SCENARIOS: list[object] = []

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


def parse_arguments():
	parser = bptools.make_arg_parser(
		description="Generate restriction enzyme overhang questions.",
		batch=True
	)
	parser = bptools.add_scenario_args(parser)

	parser.add_argument(
		'-o', '--overhang-type', '--overhang_type', dest='use_overhang_type',
		action='store_true', help='Use overhang type choices.'
	)
	parser.add_argument(
		'-e', '--end-type', '--end_type', dest='use_overhang_type',
		action='store_false', help='Use end type choices.'
	)
	parser.set_defaults(use_overhang_type=True)

	args = parser.parse_args()
	return args


#===========================================================
def write_question_batch(start_num, args):
	if len(SCENARIOS) == 0:
		return []

	remaining = None
	if args.max_questions is not None:
		remaining = args.max_questions - (start_num - 1)
		if remaining <= 0:
			return []

	batch_size = len(SCENARIOS) if remaining is None else min(len(SCENARIOS), remaining)
	questions = []
	for offset in range(batch_size):
		question_num = start_num + offset
		idx = (question_num - 1) % len(SCENARIOS)
		enzyme_class = SCENARIOS[idx]

		question_text = write_question(
			question_num,
			enzyme_class,
			args.use_overhang_type
		)
		if question_text is None:
			continue
		questions.append(question_text)
	return questions


#===========================================================
#===========================================================
#===========================================================
# This function serves as the entry point for generating and saving questions.
def main():
	args = parse_arguments()

	global SCENARIOS

	suffix = '5_3_blunt' if args.use_overhang_type else 'blunt_v_sticky'
	outfile = bptools.make_outfile(suffix)

	enzyme_names = restrictlib.get_enzyme_list()
	enzyme_classes = [restrictlib.enzyme_name_to_class(name) for name in enzyme_names]
	if args.scenario_order == 'sorted':
		enzyme_classes.sort(key=lambda x: x.__name__)
	else:
		random.shuffle(enzyme_classes)
	SCENARIOS = enzyme_classes

	questions = bptools.collect_question_batches(write_question_batch, args)
	bptools.write_questions_to_file(questions, outfile)

#===========================================================
#===========================================================
# This block ensures the script runs only when executed directly
if __name__ == '__main__':
	# Call the main function to run the program
	main()

## THE END
