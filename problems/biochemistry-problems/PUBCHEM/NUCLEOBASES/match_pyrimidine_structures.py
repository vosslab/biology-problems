#!/usr/bin/env python3

"""Blackboard BBQ generator: match pyrimidine structures to names.

Each question shows all three canonical pyrimidines (cytosine, thymine,
uracil) plus one non-canonical pyrimidine (5-methylcytosine,
5-hydroxymethylcytosine, or dihydrouracil) as a distractor.
"""

# Standard Library
import os
import sys
import random

# local repo modules
import bptools


#======================================
#======================================
def get_pubchem_dir():
	git_root = bptools._get_git_root(os.path.dirname(__file__))
	if git_root is None:
		raise RuntimeError("Unable to locate git root for PubChem imports.")
	return os.path.join(git_root, 'problems', 'biochemistry-problems', 'PUBCHEM')


_PUBCHEM_DIR = get_pubchem_dir()
if _PUBCHEM_DIR not in sys.path:
	sys.path.insert(0, _PUBCHEM_DIR)

# nucleobaselib lives alongside this script in NUCLEOBASES/
_NUCLEOBASES_DIR = os.path.dirname(os.path.abspath(__file__))
if _NUCLEOBASES_DIR not in sys.path:
	sys.path.insert(0, _NUCLEOBASES_DIR)

import pubchemlib
import moleculelib
import nucleobaselib

bptools.allow_insert_hidden_terms = False
bptools.allow_no_click_div = False

SCENARIOS: list[str] = []
GLOBAL_PCL = None


#======================================
#======================================
def get_question_text():
	question_text = ""
	question_text += moleculelib.generate_load_script()
	question_text += "<h3>Match the pyrimidine structures to their names.</h3>"
	question_text += '<p><i>Note:</i> Each choice will be used exactly once.</p>'
	return question_text


#======================================
#======================================
def write_question(N: int, args) -> str:
	if N > len(SCENARIOS):
		return None
	idx = N - 1
	distractor_name = SCENARIOS[idx]

	# build the list of names shown in this question
	matching_list = nucleobaselib.build_question_names('pyrimidine', distractor_name)

	# render each structure as an RDKit canvas
	answers_list = []
	for base_name in matching_list:
		molecule_data = GLOBAL_PCL.get_molecule_data_dict(base_name)
		if molecule_data is None:
			print(f"FAIL: {base_name}")
			sys.exit(1)
		smiles = molecule_data['SMILES']
		# Use moleculelib (not aminoacidlib) so the rendered JS matches the
		# minimal Blackboard-sanitizer-friendly format used by the working
		# amino-acid BBQ script: single script block, inline initRDKitModule
		# promise, no peptide-bond highlighting, no extra DOM hooks.
		base_image = moleculelib.generate_html_for_molecule(
			smiles, '', width=480, height=320)
		answers_list.append(base_image)

	question_text = get_question_text()
	complete_question = bptools.formatBB_MAT_Question(
		N, question_text, answers_list, matching_list)
	return complete_question


#======================================
#======================================
def parse_arguments():
	parser = bptools.make_arg_parser(
		description="Generate pyrimidine structure matching questions (canonical + 1 distractor)."
	)
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

	# one scenario per non-canonical distractor; cycle if duplicates exceed pool
	base_scenarios = list(nucleobaselib.noncanonical_pyrimidines)
	if args.scenario_order == 'sorted':
		base_scenarios.sort()
	else:
		random.shuffle(base_scenarios)

	max_q = args.max_questions if args.max_questions is not None else args.duplicates
	if max_q is None or max_q < 1:
		max_q = len(base_scenarios)
	SCENARIOS = []
	while len(SCENARIOS) < max_q:
		SCENARIOS.extend(base_scenarios)
	SCENARIOS = SCENARIOS[:max_q]

	if args.duplicates < len(SCENARIOS):
		args.duplicates = len(SCENARIOS)

	outfile = bptools.make_outfile(f"{args.num_choices}_choices")

	GLOBAL_PCL = pubchemlib.PubChemLib()
	bptools.collect_and_write_questions(write_question, args, outfile)
	GLOBAL_PCL.close()


#======================================
#======================================
if __name__ == '__main__':
	main()
