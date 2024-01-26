#!/usr/bin/env python3

# external python/pip modules
import os
import sys
import random
import argparse

# local repo modules
import bptools
import pubchemlib
import moleculelib
import aminoacidlib

bptools.use_insert_hidden_terms = False
bptools.use_add_no_click_div = False

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
def write_question(N: int, answer_amino_acid_name: str, pcl: object, num_choices: int) -> str:
	# Add more to the question based on the given letters

	matching_list = aminoacidlib.get_similar_amino_acids(answer_amino_acid_name, num=num_choices-1, pcl=pcl)
	matching_list.append(answer_amino_acid_name)

	answers_list = []
	for amino_acid_name in matching_list:
		molecule_data = pcl.get_molecule_data_dict(amino_acid_name)
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
def main():
	# Define argparse for command-line options
	parser = argparse.ArgumentParser(description="Generate questions.")
	parser.add_argument('-c', '--num_choices', type=int, default=4, help="Number of choices to create.")
	args = parser.parse_args()

	# Output file setup
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print(f'writing to file: {outfile}')

	pcl = pubchemlib.PubChemLib()

	# Create and write questions to the output file
	with open(outfile, 'w') as f:
		N = 1
		for amino_acid_name in aminoacidlib.amino_acids_fullnames:
			complete_question = write_question(N, amino_acid_name, pcl, args.num_choices)
			if complete_question is None:
				continue
			N += 1
			f.write(complete_question)
	pcl.close()
	bptools.print_histogram()
	print(f'saved {N} questions to {outfile}')

#======================================
#======================================
if __name__ == '__main__':
	main()
