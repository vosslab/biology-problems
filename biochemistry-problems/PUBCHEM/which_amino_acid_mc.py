#!/usr/bin/env python3

# external python/pip modules
import os
import sys
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
def get_question_text(molecule_name, pcl):
	molecule_data = pcl.get_molecule_data_dict(molecule_name)
	if molecule_data is None:
		print(f"FAIL: {molecule_name}")
		sys.exit(1)
	#info_table = pcl.generate_molecule_info_table(molecule_data)
	smiles = molecule_data.get('SMILES')
	pubchem_image = moleculelib.generate_html_for_molecule(smiles, '', width=480, height=512)

	question_text = ""
	question_text += moleculelib.generate_load_script()
	question_text += pubchem_image
	question_text +=  "<h3>Which one of the followung amino acids is represented by the chemical structure shown above?</h3>"
	question_text += moleculelib.generate_load_script()

	return question_text

#======================================
#======================================
def write_question(N: int, amino_acid_name: str, pcl: object, num_choices: int) -> str:
	# Add more to the question based on the given letters

	choices_list = aminoacidlib.get_similar_amino_acids(amino_acid_name, num=num_choices-1, pcl=pcl)
	choices_list.append(amino_acid_name)
	choices_list.sort()

	question_text = get_question_text(amino_acid_name, pcl)
	if question_text is None:
		return None

	# Complete the question formatting
	complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, amino_acid_name)

	return complete_question

#======================================
#======================================
def main():
	# Define argparse for command-line options
	parser = argparse.ArgumentParser(description="Generate questions.")
	parser.add_argument('-d', '--duplicates', type=int, default=95, help="Number of questions to create.")
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
