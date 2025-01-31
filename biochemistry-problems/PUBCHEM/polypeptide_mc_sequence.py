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
	#amino_acid_letters = list('ACDEFGHIKLMNPQRSTVWY')
	# no proline, too hard
	amino_acid_letters = list('ACDEFGHIKLMNQRSTVWY')
	# this is so amino acids are not repeated
	peptide_sequence_list = random.sample(amino_acid_letters, num_amino_acids)
	# list is already shuffled, but do it again to be sure
	random.shuffle(peptide_sequence_list)
	peptide_sequence_text = ''.join(peptide_sequence_list)
	print('peptide_sequence_text', peptide_sequence_text)
	return peptide_sequence_text

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

	<p>Here is a step-by-step guide to help you answer the question:</p>
	<ol>

		<li style="margin-bottom: 20px;">Consult an amino acid guide for reference. You can find a PDF guide on Blackboard under "Exam and Quiz" in the "Old Exams" section, with the filename <a href="https://drive.google.com/file/d/1Mgum_TmZ71-XIjb38sStEpzzZLqkQb-W/view?usp=sharing">bchm_exam-help_sheet.pdf</a>, or search online for a visual guide that shows all 20 amino acids with their single-letter codes.</li>

		<li style="margin-bottom: 20px;">Identify the amino-terminal end, represented as <span style="padding: 2px; color: #0000cc; background-color: #66ff66;">NH<sub>3</sub><sup>+</sup></span> and highlighted in bright green. Distinguish between the general nitrogens in amino acid backbones (denoted as <span style="color:#0000cc">NH</span>) and the nitrogen in amino acid side chains.</li>

		<li style="margin-bottom: 20px;">The {less_one_number_name} peptide bonds connecting the {number_name} amino acids are highlighted in <span style="background-color: #00FF00; padding: 2px;">bright green</span>, making it easier to distinguish the {number_name} amino acids.</li>

		<li style="margin-bottom: 20px;">Examine the side chain for each of the {number_name} amino acids to determine their single-letter amino acid code.</li>

		<li style="margin-bottom: 20px;">List the single-letter amino acid codes in the amino to carboxyl (N&rarr;C) direction. This is the standard method for writing peptide sequences.</li>
	</ol>

	<p>Select the correct peptide sequence from the options below:</p>
	"""
	# Remove any unnecessary newlines or tabs
	question_text = question_text.replace('\n', ' ')
	question_text = question_text.replace('\t', ' ')
	while '  ' in question_text:
		question_text = question_text.replace('  ', ' ')
	return question_text

#===============================
#===============================
def generate_html_content(peptide_sequence):
	"""Generate the HTML content for amino acid visualization."""
	# Start by generating the HTML header for the amino acid visualization
	html_content = aminoacidlib.generate_load_script()

	# Convert the word (amino acid sequence) to its peptide representation
	poly_peptide_smiles = aminoacidlib.make_polypeptide_smiles_from_sequence(peptide_sequence)
	#molecule_name = 'pentapeptide '+word
	crc16 = bptools.getCrc16_FromString(peptide_sequence)
	molecule_name = 'peptide_'+crc16
	html_content += aminoacidlib.generate_html_for_molecule(poly_peptide_smiles, molecule_name, width=480, height=512)

	return html_content

#===============================
#===============================
def generate_distractors(correct_sequence, num_distractors=3):
	"""
	Generates multiple-choice distractors for a peptide sequence question.

	Parameters:
	- correct_sequence (str): The correct peptide sequence.
	- num_distractors (int): Number of distractors to generate.

	Returns:
	- List[str]: A list of distractor sequences.
	"""
	# Amino acid single-letter codes
	amino_acids = "ACDEFGHIKLMNPQRSTVWY"

	distractors = set()
	while len(distractors) < num_distractors:
		# Start with the correct sequence and modify it slightly
		new_sequence = list(correct_sequence)

		# Apply random modifications
		for _ in range(random.randint(1, 3)):  # Randomly change 1 to 3 positions
			index = random.randint(0, len(new_sequence) - 1)
			new_amino_acid = random.choice(amino_acids)

			# Ensure the new amino acid is different from the current one
			while new_amino_acid == new_sequence[index]:
				new_amino_acid = random.choice(amino_acids)

			new_sequence[index] = new_amino_acid

		# Shuffle some part of the sequence for variety
		if random.random() < 0.5:
			start, end = sorted(random.sample(range(len(new_sequence)), 2))
			sub_seq = new_sequence[start:end + 1]
			random.shuffle(sub_seq)
			new_sequence[start:end + 1] = sub_seq

		# Join the modified sequence
		new_sequence_str = ''.join(new_sequence)

		# Ensure the distractor is not identical to the correct answer or other distractors
		if new_sequence_str != correct_sequence:
			distractors.add(new_sequence_str)

	return list(distractors)

#===============================
#===============================
def generate_complete_question(N, num_amino_acids, num_choices, debug=False):
	"""
	Given a word (amino acid sequence), generate a complete question.
	The question has an HTML visual representation of the amino acid and related question text.
	Returns a formatted question.
	"""
	peptide_sequence = get_peptide_sequence(num_amino_acids)

	question_text = generate_question_text(num_amino_acids)
	html_content = generate_html_content(peptide_sequence)

	# Combine the molecule visualization with the question text
	complete_question = html_content + question_text

	# Format the question for the Blackboard system
	answers_text = peptide_sequence

	choices_list = generate_distractors(answers_text, num_choices-1)
	choices_list.append(answers_text)
	choices_list = list(set(choices_list))
	random.shuffle(choices_list)

	bbformat = bptools.formatBB_MC_Question(N, complete_question, choices_list, answers_text)

	if debug:
		html_file = 'guess_peptide.html'
		with open(html_file, 'a') as file:
			file.write(html_content)
		print(f'saved html to {html_file}')

	return bbformat

#=====================
def parse_arguments():
	"""
	Parses command-line arguments for the script.

	Defines and handles all arguments for the script, including:
	- `duplicates`: The number of questions to generate.
	- `num_choices`: The number of answer choices for each question.
	- `question_type`: Type of question (numeric or multiple choice).

	Returns:
		argparse.Namespace: Parsed arguments with attributes `duplicates`,
		`num_choices`, and `question_type`.
	"""
	parser = argparse.ArgumentParser(description="Generate questions.")
	parser.add_argument(
		'-d', '--duplicates', metavar='#', type=int, dest='duplicates',
		help='Number of duplicate runs to do or number of questions to create', default=1
	)
	parser.add_argument(
		'-c', '--num_choices', type=int, default=5, dest='num_choices',
		help="Number of choices to create."
	)
	parser.add_argument('-n', '--num_amino', type=int, default=2,
		help="Number of amino acids in polypeptides.")

	args = parser.parse_args()
	return args

#======================================
#======================================
def main():
	"""
	Main function that orchestrates question generation and file output.
	"""
	# Parse arguments from the command line
	args = parse_arguments()

	# Generate the output filename
	outfile = ('bbq-'
		+ f'{args.num_amino}_amino_acids-'
		+ os.path.splitext(os.path.basename(__file__))[0]
		+ '-questions.txt')
	print(f'Writing to file: {outfile}')

	# Open the output file and generate questions
	with open(outfile, 'w') as f:
		N = 1  # Question number counter
		for _ in range(args.duplicates):
			complete_question = generate_complete_question(N, args.num_amino, args.num_choices)
			if complete_question is not None:
				N += 1
				f.write(complete_question)

	# Display histogram if question type is multiple choice
	bptools.print_histogram()
	print(f'saved {N} questions to {outfile}')

#===============================
#===============================
# Starting point of the script
if __name__ == '__main__':
	main()
