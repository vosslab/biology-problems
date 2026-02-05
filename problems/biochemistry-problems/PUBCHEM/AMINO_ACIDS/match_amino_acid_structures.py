#!/usr/bin/env python3

# external python/pip modules
import os
import sys
import random

# local repo modules
import bptools

def get_pubchem_dir():
	git_root = bptools._get_git_root(os.path.dirname(__file__))
	if git_root is None:
		raise RuntimeError("Unable to locate git root for PubChem imports.")
	return os.path.join(git_root, 'problems', 'biochemistry-problems', 'PUBCHEM')


_PUBCHEM_DIR = get_pubchem_dir()
if _PUBCHEM_DIR not in sys.path:
	sys.path.insert(0, _PUBCHEM_DIR)

import pubchemlib
import moleculelib
import aminoacidlib

bptools.allow_insert_hidden_terms = False
bptools.allow_no_click_div = False

SCENARIOS: list[str] = []
GLOBAL_PCL = None

#======================================
#======================================
def td_header(color_id):
	return f'<tr><td style="background-color: {color_id};">'

#======================================
#======================================
def get_question_text():
	question_text = ""
	question_text += moleculelib.generate_load_script()
	question_text += "<h3>Match the amino acid structures to their names.</h3>"
	question_text += '<p><i>Note:</i> Each choice will be used exactly once.</p>'

	return question_text

#======================================
#======================================
def write_question(N: int, args) -> str:
	if N > 20 or N > len(SCENARIOS):
		return None
	idx = N - 1
	answer_amino_acid_name = SCENARIOS[idx]
	# Add more to the question based on the given letters

	matching_list = aminoacidlib.get_similar_amino_acids(
		answer_amino_acid_name, num=args.num_choices - 1, pcl=GLOBAL_PCL
	)
	matching_list.append(answer_amino_acid_name)

	answers_list = []
	for amino_acid_name in matching_list:
		molecule_data = GLOBAL_PCL.get_molecule_data_dict(amino_acid_name)
		if molecule_data is None:
			print(f"FAIL: {amino_acid_name}")
			sys.exit(1)
		smiles = molecule_data.get('SMILES')
		pubchem_image = moleculelib.generate_html_for_molecule(smiles, '', width=480, height=320)
		answers_list.append(pubchem_image)

	question_text = get_question_text()
	if question_text is None:
		return None

	# Complete the question formatting
	complete_question = bptools.formatBB_MAT_Question(N, question_text, answers_list, matching_list)

	return complete_question

#======================================
#======================================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate amino acid structure matching questions.")
	parser = bptools.add_choice_args(parser, default=4)
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
	outfile = bptools.make_outfile(f"{args.num_choices}_choices")

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
