#!/usr/bin/env python3

# Standard Library
import random

# local repo modules
import bptools

# HTML emphasis spans for law labels
FIRST_EMPH = "<span style='color:#0077bb;font-weight:700;'>First</span>"
SECOND_EMPH = "<span style='color:#cc6600;font-weight:700;'>Second</span>"

# core correct statements (both always present as choices)
ENERGY_STATEMENT = (
	"the total energy of a system and its surroundings is constant"
)
ENTROPY_STATEMENT = (
	"the total entropy of a system and its surroundings "
	"increases for a spontaneous process"
)

# misconception distractor pool (pick 2 per question)
DISTRACTOR_POOL = [
	"energy is always increasing in a spontaneous process",
	"entropy of the system always increases for a spontaneous process",
	"entropy of the universe is constant",
	"a spontaneous process always releases heat",
	"free energy of the universe always decreases",
	"temperatures will always decrease in a spontaneous process",
]

# stem wording templates (%s is replaced with the law label)
STEM_TEMPLATES = [
	"The %s Law of Thermodynamics states:",
	"Which statement best describes the %s Law of Thermodynamics?",
	"Select the statement that matches the %s Law of Thermodynamics.",
]


#======================================
#======================================
def write_question(question_num: int, args) -> str:
	"""
	Create a complete formatted MC question about identifying
	the First or Second Law of Thermodynamics.

	Args:
		question_num (int): the question number for labeling.
		args (argparse.Namespace): parsed command-line arguments.

	Returns:
		str: a formatted BBQ question string.
	"""
	# pick which law to ask about (0 = First, 1 = Second)
	law_index = random.randint(0, 1)

	# pick a stem wording
	stem_template = random.choice(STEM_TEMPLATES)

	# set the correct answer and label based on the chosen law
	if law_index == 0:
		law_label = FIRST_EMPH
		answer_text = ENERGY_STATEMENT
	else:
		law_label = SECOND_EMPH
		answer_text = ENTROPY_STATEMENT

	# build the question stem
	question_text = stem_template % (law_label,)

	# pick 2 distractors from pool
	picked_distractors = random.sample(DISTRACTOR_POOL, 2)

	# assemble 4 choices: both core statements + 2 distractors
	choices_list = [ENERGY_STATEMENT, ENTROPY_STATEMENT] + picked_distractors
	random.shuffle(choices_list)

	# format as a standard MC question
	complete_question = bptools.formatBB_MC_Question(
		question_num, question_text, choices_list, answer_text
	)
	return complete_question


#======================================
#======================================
def parse_arguments():
	"""
	Parse command-line arguments for the script.

	Returns:
		argparse.Namespace: parsed arguments.
	"""
	parser = bptools.make_arg_parser(
		description="Generate thermodynamics law identification MC questions."
	)
	args = parser.parse_args()
	return args


#======================================
#======================================
def main():
	"""
	Main function that orchestrates question generation and file output.
	"""
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)


#======================================
#======================================
if __name__ == "__main__":
	main()
