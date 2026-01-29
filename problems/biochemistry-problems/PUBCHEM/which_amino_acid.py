#!/usr/bin/env python3

# external python/pip modules
import sys
import random

# local repo modules
import bptools
import pubchemlib
import moleculelib
import aminoacidlib

bptools.use_insert_hidden_terms = False
bptools.use_add_no_click_div = False

SCENARIOS: list[str] = []
GLOBAL_PCL = None

#======================================
#======================================
def td_header(color_id):
	return f'<tr><td style="background-color: {color_id};">'

#======================================
#======================================
def get_question_text(molecule_name, pcl):
	molecule_data = pcl.get_molecule_data_dict(molecule_name)
	if molecule_data is None:
		print(f"FAIL: {molecule_name}")
		sys.exit(1)
	#info_table = pcl.generate_molecule_info_table(molecule_data)
	smiles = molecule_data.get('SMILES')
	pubchem_image = moleculelib.generate_html_for_molecule(smiles, '', width=480, height=320)

	question_text = ""
	question_text += moleculelib.generate_load_script()
	question_text += pubchem_image
	question_text +=  "<h3>Which amino acid is represented by the chemical structure shown above?</h3>"

	return question_text

#======================================
#======================================
def write_question(N: int, args) -> str:
	if N > 20 or N > len(SCENARIOS):
		return None
	idx = N - 1
	amino_acid_name = SCENARIOS[idx]

	question_text = get_question_text(amino_acid_name, GLOBAL_PCL)
	if question_text is None:
		return None

	if args.question_type == 'fib':
		answers_set = set()
		answers_set.add(amino_acid_name)
		answers_set.add(amino_acid_name.title())
		answers_set.add(amino_acid_name.replace(' ', ''))
		answers_set.add(amino_acid_name.title().replace(' ', ''))
		answers_list = sorted(answers_set)
		# Complete the question formatting
		complete_question = bptools.formatBB_FIB_Question(N, question_text, answers_list)
	else:
		choices_list = aminoacidlib.get_similar_amino_acids(
			amino_acid_name, num=args.num_choices - 1, pcl=GLOBAL_PCL
		)
		choices_list.append(amino_acid_name)
		choices_list.sort()
		complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, amino_acid_name)

	return complete_question

#======================================
#======================================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate amino acid ID questions.")
	parser = bptools.add_choice_args(parser, default=7)
	parser = bptools.add_question_format_args(
		parser,
		types_list=['mc', 'fib'],
		required=False,
		default='mc'
	)
	parser = bptools.add_scenario_args(parser)
	args = parser.parse_args()
	return args

#======================================
#======================================
def main():
	global SCENARIOS
	global GLOBAL_PCL

	args = parse_arguments()
	if args.max_questions is None or args.max_questions > 20:
		args.max_questions = 20
	if args.duplicates < args.max_questions:
		args.duplicates = args.max_questions
	outfile_suffix = args.question_type.upper()
	if args.question_type == 'mc':
		outfile = bptools.make_outfile(outfile_suffix, f"{args.num_choices}_choices")
	else:
		outfile = bptools.make_outfile(outfile_suffix)

	SCENARIOS = list(aminoacidlib.amino_acids_fullnames)
	if args.scenario_order == 'sorted':
		SCENARIOS.sort()
	else:
		random.shuffle(SCENARIOS)

	GLOBAL_PCL = pubchemlib.PubChemLib()
	bptools.collect_and_write_questions(write_question, args, outfile)
	GLOBAL_PCL.close()

#======================================
#======================================
if __name__ == '__main__':
	main()
