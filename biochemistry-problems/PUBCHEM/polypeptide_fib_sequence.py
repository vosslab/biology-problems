#!/usr/bin/env python3


# general built-in/pip libraries
import os
import re
import sys
import random
import argparse

# local libraries
import bptools
import aminoacidlib
bptools.use_insert_hidden_terms = False
bptools.use_add_no_click_div = False
bptools.use_nocopy_script = False


# Constant containing valid amino acid letters for reference
VALID_AMINO_ACID_LETTERS = 'ACDEFGHIKLMNQRSTVWY'
debug = False

peptide_name_map = {
	2: 'dipeptide',
	3: 'tripeptide',
	4: 'tetrapeptide',
	5: 'pentapeptide',
	6: 'hexapeptide',
}

#===============================
#===============================
def get_peptide_sequence(num_amino_acids):
	amino_acid_letters = list('ACDEFGHIKLMNPQRSTVWY')
	peptide_sequence = ''
	for i in range(num_amino_acids):
		peptide_sequence += random.choice(amino_acid_letters)
	return peptide_sequence

#===============================
#===============================
def generate_question_text(num_amino_acids):
	"""
	Generates the static text for the question.
	Helps students decode a pentapeptide from a given representation.
	Returns a formatted question text.
	"""
	peptide_name = peptide_name_map[num_amino_acids]
	cardinal_name = bptools.number_to_cardinal(num_amino_acids)
	number_name = f'{cardinal_name} ({num_amino_acids})'
	less_one_number_name = f'{bptools.number_to_cardinal(num_amino_acids-1)} ({num_amino_acids-1})'
	question_text = f"""
	<p>A {peptide_name} is made up of {number_name} amino acids. The figure above shows one such {peptide_name} with an unknown sequence. Your task is to find out the {number_name} letter sequence of this {peptide_name}.</p>

	<p>Here is a step-by-step guide to help you:</p>
	<ol>

		<li style="margin-bottom: 20px;">Consult an amino acid guide for reference. You can find a PDF guide on Blackboard under "Exam and Quiz" in the "Old Exams" section, with the filename <a href="https://drive.google.com/file/d/1Mgum_TmZ71-XIjb38sStEpzzZLqkQb-W/view?usp=sharing">bchm_exam-help_sheet.pdf</a>, or search online for a visual guide that shows all 20 amino acids with their single-letter codes.</li>

		<li style="margin-bottom: 20px;">Identify the amino-terminal end, represented as <span style="padding: 2px; color: #0000cc; background-color: #66ff66;">NH<sub>3</sub><sup>+</sup></span> and highlighted in bright green. Distinguish between the general nitrogens in amino acid backbones (denoted as <span style="color:#0000cc">NH</span>) and the nitrogen in amino acid side chains.</li>

		<li style="margin-bottom: 20px;">The {less_one_number_name} peptide bonds connecting the {number_name} amino acids is/are highlighted in <span style="background-color: #00FF00; padding: 2px;">bright green</span>, making it easier to distinguish the {number_name} amino acids.</li>

		<li style="margin-bottom: 20px;">Examine the side chain for each of the {number_name} amino acids to determine their single-letter amino acid code.</li>

		<li style="margin-bottom: 20px;">Once you have identified the single-letter codes for the {number_name} side chains, list them in the amino to carboxyl (N&rarr;C) direction. This is the standard method for writing peptide sequences.</li>

		<li style="margin-bottom: 20px;">You answer will consist only {number_name} letters</li>
	</ol>
	"""
	# Remove any unnecessary newlines or tabs
	question_text = question_text.replace('\n', ' ')
	question_text = question_text.replace('\t', ' ')
	while '  ' in question_text:
		question_text = question_text.replace('  ', ' ')
	return question_text

#===============================
#===============================
def generate_html_content(dipeptde):
	"""Generate the HTML content for amino acid visualization."""
	# Start by generating the HTML header for the amino acid visualization
	html_content = aminoacidlib.generate_load_script()

	# Convert the word (amino acid sequence) to its peptide representation
	poly_peptide_smiles = aminoacidlib.make_peptide_from_sequence(dipeptde)
	#molecule_name = 'pentapeptide '+word
	crc16 = bptools.getCrc16_FromString(dipeptde)
	molecule_name = 'peptide_'+crc16
	html_content += aminoacidlib.generate_html_for_molecule(poly_peptide_smiles, molecule_name)

	return html_content

#===============================
#===============================
def generate_complete_question(N, num_amino_acids, debug=False):
	"""
	Given a word (amino acid sequence), generate a complete question.
	The question has an HTML visual representation of the amino acid and related question text.
	Returns a formatted question.
	"""
	peptide = get_peptide_sequence(num_amino_acids)

	question_text = generate_question_text(num_amino_acids)
	html_content = generate_html_content(peptide)

	# Combine the molecule visualization with the question text
	complete_question = html_content + question_text

	# Format the question for the Blackboard system
	answers_list = [peptide,]
	bbformat = bptools.formatBB_FIB_Question(N, complete_question, answers_list)

	if debug:
		html_file = 'guess_peptide.html'
		with open(html_file, 'a') as file:
			file.write(html_content)
		print(f'saved html to {html_file}')

	return bbformat

#===============================
#===============================
def main():
	"""
	Main function to generate and save pentapeptide questions.
	"""
	# Argument parser for command-line options
	parser = argparse.ArgumentParser(description='Random polypeptide questions.')
	parser.add_argument('-d', '--duplicates', type=int, default=95, help="Number of questions to create.")
	parser.add_argument('-n', '--num_amino', type=int, default=2, help="Number of amino acids in polypeptides.")

	args = parser.parse_args()

	# Generate the output filename
	outfile = ('bbq-'
		+ f'{args.num_amino}-'
		+ os.path.splitext(os.path.basename(__file__))[0]
		+ '-questions.txt')
	print('writing to file: ' + outfile)

	# Create and write questions to the output file
	with open(outfile, 'w') as file:
		N = 1
		for d in range(args.duplicates):
			bbformat = generate_complete_question(N, args.num_amino)
			if bbformat is None:
				continue
			N += 1
			file.write(bbformat)
	bptools.print_histogram()
	print(f'saved {N} questions to {outfile}')


#===============================
#===============================
# Starting point of the script
if __name__ == '__main__':
	main()
