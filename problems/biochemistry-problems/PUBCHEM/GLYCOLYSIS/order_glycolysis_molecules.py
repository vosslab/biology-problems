#!/usr/bin/env python3

# external python/pip modules
import os
import sys
import yaml
#import random

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

import moleculelib

bptools.allow_insert_hidden_terms = False
GLOBAL_MOLECULE_DATA = None

#======================================
#======================================
def load_molecules(molecule_file=None):
	if molecule_file is None:
		molecule_file = 'glycolysis.yml'
	molecule_file = os.path.join(os.path.dirname(__file__), molecule_file)
	with open(molecule_file, 'r') as file:
		molecule_data = yaml.safe_load(file)
	#print(molecule_data)
	return molecule_data

def random_hex_string(length=2):
	return os.urandom(length).hex()

#======================================
#======================================
def get_question_text(molecules_to_use: list, num_choices: int):
	question_text = "<p>Glycolysis is an important metabolic pathway that breaks down glucose to produce energy. During the process known as glycolysis, molecules undergo transformations in a specific sequence. Understanding the order of these molecular transformations is a fundamental concept in biology.</p>"

	cardinal = bptools.number_to_cardinal(num_choices)
	question_text += f"<p>Please place the following {cardinal} ({num_choices}) "
	question_text += "molecular structures of glycolysis in the correct order. "

	question_text += 'The correct sequence of the molecule names is as follows:<ul>'
	for i, molecule_dict in enumerate(molecules_to_use):
		question_text += f"<li>{i+1}. {molecule_dict['name']} ({molecule_dict['abbreviation']})</li>"
	question_text += '</ul>'

	question_text += f"Identify which chemical structure corresponds to each of the {cardinal} ({num_choices})"
	question_text += " molecule names listed above. This will help you visualize the steps each molecule undergoes during glycolysis.</p>"

	question_text += "<p>Here are some tips:<ul>"
	question_text += "<li>Think about what changes occur from one molecule to the next.</li>"
	question_text += "<li>Consider the number of carbons and phosphates each molecule contains.</li>"
	question_text += "<li>Molecules that are next to each other in the pathway are often similar.</li>"
	question_text += "<li>Sometimes, working backwards can be helpful.</li>"
	question_text += "</ul></p>"
	question_text += moleculelib.generate_load_script()
	return question_text

#======================================
#======================================
def write_question(N: int, args) -> str:
	molecule_data = GLOBAL_MOLECULE_DATA

	molecule_start_index = N % (len(molecule_data) - args.num_choices + 1)
	molecules_to_use = molecule_data[molecule_start_index:molecule_start_index + args.num_choices]

	# Add more to the question based on the given letters
	question_text = get_question_text(molecules_to_use, args.num_choices)

	ordered_answers_list = []
	matches_list = []
	for molecule_dict in molecules_to_use:
		smiles_text = molecule_dict['SMILES']
		name_text = f"{molecule_dict['name']} ({molecule_dict['abbreviation']})"
		randhex = random_hex_string(length=2)
		html_content = moleculelib.generate_html_for_molecule(smiles_text, molecule_name=randhex, width=512, height=256)
		ordered_answers_list.append(html_content+'<hr/>')
		matches_list.append(name_text)

	# Complete the question formatting
	complete_question = bptools.formatBB_ORD_Question(N, question_text, ordered_answers_list)
	#complete_question = bptools.formatBB_MAT_Question(N, question_text, ordered_answers_list, matches_list)

	return complete_question

#======================================
#======================================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate glycolysis ordering questions.")
	parser = bptools.add_choice_args(parser, default=4)
	args = parser.parse_args()
	return args

#======================================
#======================================
def main():
	args = parse_arguments()
	global GLOBAL_MOLECULE_DATA
	GLOBAL_MOLECULE_DATA = load_molecules()
	outfile = bptools.make_outfile("ORD", f"{args.num_choices}_choices")
	bptools.collect_and_write_questions(write_question, args, outfile)


#======================================
#======================================
if __name__ == '__main__':
	main()
