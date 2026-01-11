#!/usr/bin/env python3

import copy
import random

import bptools

def format_amino_acid(amino_acid_num):
	return f"amino acid {amino_acid_num:d}"

#=====================
def format_amino_acid_pair(amino_acid_num, shift):
	choice_text = ""
	choice_text += f"amino acids {amino_acid_num-shift:d} "
	choice_text += f"and {amino_acid_num+shift:d} "
	if shift > 1:
		choice_text += f"(a residue shift of {shift} positions)"
	else:
		choice_text += f"(a residue shift of {shift} position)"
	return choice_text

#=====================
def get_choices_mc(amino_acid_num, num_choices):
	shift = 4
	answer_text = format_amino_acid_pair(amino_acid_num, shift)

	choices_list = []
	choices_list.append(answer_text)

	for shift in (3,5):
		choice = format_amino_acid_pair(amino_acid_num, shift)
		choices_list.append(choice)

	extra_choices = []
	for shift in (1,2,6,7,8,9,10):
		if shift >= amino_acid_num:
			#can't have a negative amino acid number
			continue
		choice = format_amino_acid_pair(amino_acid_num, shift)
		extra_choices.append(choice)
	random.shuffle(extra_choices)
	while len(extra_choices) > 0 and len(choices_list) < num_choices:
		choices_list.append(extra_choices.pop())
	choices_list = list(set(choices_list))
	#print(choices_list)
	#choices_list.sort()
	sorted_amino_list = sorted(choices_list, key=lambda x: int(x.split()[-2]))
	return sorted_amino_list, answer_text

#=====================
def get_choices_ma(amino_acid_num, num_choices):

	shift = 4
	answers_list = [
		format_amino_acid(amino_acid_num - shift),
		format_amino_acid(amino_acid_num + shift),
	]

	choices_list = copy.copy(answers_list)
	for shift in (1,5):
		choices_list.append(format_amino_acid(amino_acid_num - shift))
		choices_list.append(format_amino_acid(amino_acid_num + shift))

	extra_choices = []
	for shift in (0,2,3,6,7,8):
		if amino_acid_num - shift > 0:
			extra_choices.append(format_amino_acid(amino_acid_num - shift))
		extra_choices.append(format_amino_acid(amino_acid_num + shift))
	extra_choices = list(set(extra_choices))
	random.shuffle(extra_choices)
	while len(extra_choices) > 0 and len(choices_list) < num_choices:
		choices_list.append(extra_choices.pop())
	choices_list = list(set(choices_list))
	#print(choices_list)
	sorted_amino_list = sorted(choices_list, key=lambda x: int(x.split()[-1]))
	return sorted_amino_list, answers_list

#=====================
def write_question(N, args):
	amino_acid_num = random.randint(6,12)
	question_statement = ""
	question_statement += "<p>The &alpha;-helix is a right-handed coil in which "
	question_statement += "each backbone N&ndash;H group forms a hydrogen bond with "
	question_statement += "the C=O group of an amino acid located a few residues away. "
	question_statement += "The regular pattern of hydrogen bonding stabilizes the helix, "
	question_statement += "preventing it from unraveling.</p> "
	question_statement += f"<p>In a long &alpha;-helix, amino acid <b>number {amino_acid_num}</b>"
	question_statement += " would form a hydrogen bond with which two other amino acids?</p>"
	if args.question_type == "mc":
		question_statement += "<p>Select the correct pair of amino acids below.</p>"
		choices_list, answer_text = get_choices_mc(amino_acid_num, args.num_choices)
		complete_question = bptools.formatBB_MC_Question(N, question_statement, choices_list, answer_text)
	elif args.question_type == "ma":
		question_statement += "<p>Select two correct answers.</p>"
		choices_list, answers_list = get_choices_ma(amino_acid_num, args.num_choices)
		complete_question = bptools.formatBB_MA_Question(N, question_statement, choices_list, answers_list)
	else:
		raise ValueError
	return complete_question

#=====================
def parse_arguments():
	parser = bptools.make_arg_parser()
	parser = bptools.add_choice_args(parser, default=None)
	parser = bptools.add_question_format_args(
		parser,
		types_list=['ma', 'mc'],
		required=False,
		default='mc'
	)

	args = parser.parse_args()
	if args.num_choices is None:
		if args.question_type == "ma":
			args.num_choices = 9
		elif args.question_type == "mc":
			args.num_choices = 6
	else:
		if args.question_type == "ma" and args.num_choices < 6:
			raise ValueError("minimum choices for MA is 6")
		if args.question_type == "mc" and args.num_choices < 4:
			raise ValueError("minimum choices for MC is 4")

	return args

#======================================
#======================================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile(None, args.question_type.upper())
	bptools.collect_and_write_questions(write_question, args, outfile)

#======================================
#======================================
if __name__ == '__main__':
	main()

## THE END
