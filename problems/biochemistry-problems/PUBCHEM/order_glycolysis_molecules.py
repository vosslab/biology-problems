#!/usr/bin/env python3

# external python/pip modules
import os
import yaml
#import random
import argparse

# local repo modules
import bptools
import moleculelib

bptools.use_insert_hidden_terms = False

#======================================
#======================================
def load_molecules(molecule_file=None):
	if molecule_file is None:
		molecule_file = 'glycolysis.yml'
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
def write_question(N: int, molecule_data: list, num_choices: int) -> str:

	molecule_start_index = N % (len(molecule_data)-num_choices+1)
	molecules_to_use = molecule_data[molecule_start_index:molecule_start_index+num_choices]
	print(molecules_to_use[-1])

	# Add more to the question based on the given letters
	question_text = get_question_text(molecules_to_use, num_choices)

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
def main():
	# Define argparse for command-line options
	parser = argparse.ArgumentParser(description="Generate questions.")
	parser.add_argument('-d', '--duplicates', type=int, default=99, help="Number of questions to create.")
	parser.add_argument('-n', '--num_choices', type=int, default=4, help="Number of choices to create.")
	args = parser.parse_args()

	# Output file setup
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print(f'writing to file: {outfile}')

	molecule_data = load_molecules()

	# Create and write questions to the output file
	with open(outfile, 'w') as f:
		N = 1
		for d in range(args.duplicates):
			complete_question = write_question(N, molecule_data, args.num_choices)
			if complete_question is not None:
				N += 1
				f.write(complete_question)
	bptools.print_histogram()


#======================================
#======================================
if __name__ == '__main__':
	main()
