#!/usr/bin/env python3


# general built-in/pip libraries
import os
import re
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

#===============================
#===============================
def read_wordle():
	"""
	Reads amino acid words from the wordle file.
	Only words composed of valid amino acid letters and of length 5 are considered valid.
	Returns a list of valid words.
	"""
	valid_words = []
	wordle_file = bptools.get_repo_data_path('real_wordles.txt')
	with open(wordle_file, 'r') as file:
		for line in file:
			# Skip comment lines in the wordle file
			if line.startswith('#'):
				continue
			word = line.strip().upper()
			# Validate if word contains only VALID_AMINO_ACID_LETTERS and is of length 5
			if re.fullmatch("[" + VALID_AMINO_ACID_LETTERS + "]{5}", word):
				valid_words.append(word)
	print(f'Found {len(valid_words)} valid words from file')
	return valid_words

#===============================
#===============================
def generate_question_text():
	"""
	Generates the static text for the question.
	Helps students decode a pentapeptide from a given representation.
	Returns a formatted question text.
	"""
	question_text = """
<p>A pentapeptide is made up of 5 amino acids. The figure above shows one such peptide chain with an unknown sequence. Your task is to find out the sequence of this pentapeptide.</p>

<p>Here is a step-by-step guide to help you:</p>
<ol>
	<li style="margin-bottom: 20px;">Looking at an amino acid guide can help. There is a PDF guide on Blackboard under "Exam and Quiz" with the "Old Exams" and the filename <a href="https://drive.google.com/file/d/1Mgum_TmZ71-XIjb38sStEpzzZLqkQb-W/view?usp=sharing">bchm_exam-help_sheet.pdf</a>. You can also search online to find a visual grid that shows all 20 amino acids with their single-letter codes.</li>
	<li style="margin-bottom: 20px;">First, identify the amino-terminal end, which is represented as <span style="padding: 2px; color: #0000cc; background-color: #66ff66;">NH<sub>3</sub><sup>+</sup></span> and highlighted in bright green. It's important to differentiate between the general nitrogens found in amino acid backbones (denoted as <span style="color:#0000cc">NH</span>) and the nitrogen in the side chains of amino acids. Among amino acids, only lysine has a side chain with three hydrogens, resembling the <span style="color:#0000cc">NH<sub>3</sub><sup>+</sup></span> of the amino-terminal end.
	<li style="margin-bottom: 20px;">The peptide bonds are highlighted in <span style="background-color: #00FF00; padding: 2px;">bright green</span>, helping you see the different amino acids.</li>
	<li style="margin-bottom: 20px;">Look at the side chains of each amino acid to figure out their single-letter amino acid code.</li>
	<li style="margin-bottom: 20px;">Once you know the single-letter codes for the 5 side chains, list them in the amino to carboxyl (N&rarr;C) direction. This is the accepted way to write peptide sequences.</li>
	<li style="margin-bottom: 20px;">The correct sequence of letters will be a five-letter English word. This word is also an answer in the New York Times Wordle&trade; game.</li>
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
def generate_html_content(word):
	"""Generate the HTML content for amino acid visualization."""
	# Start by generating the HTML header for the amino acid visualization
	html_content = aminoacidlib.generate_load_script()

	# Convert the word (amino acid sequence) to its peptide representation
	poly_peptide_smiles = aminoacidlib.make_polypeptide_smiles_from_sequence(word)
	#molecule_name = 'pentapeptide '+word
	crc16 = bptools.getCrc16_FromString(word)
	molecule_name = 'peptide_'+crc16
	html_content += aminoacidlib.generate_html_for_molecule(poly_peptide_smiles, molecule_name)

	return html_content

#===============================
#===============================
def generate_complete_question(N, word, debug=False):
	"""
	Given a word (amino acid sequence), generate a complete question.
	The question has an HTML visual representation of the amino acid and related question text.
	Returns a formatted question.
	"""
	question_text = generate_question_text()
	html_content = generate_html_content(word)

	# Combine the molecule visualization with the question text
	complete_question = html_content + question_text

	# Format the question for the Blackboard system
	answers_list = [word,]
	bbformat = bptools.formatBB_FIB_Question(N, complete_question, answers_list)

	if debug:
		html_file = 'pentapeptide_wordle.html'
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
	parser = argparse.ArgumentParser(description='Generate pentapeptide questions.')
	parser.add_argument('-x', '--max_questions', '--max', dest='max_questions', type=int, metavar='#',
		help='Maximum number of questions to generate', default=9)
	args = parser.parse_args()

	# Read and shuffle the valid amino acid words
	valid_words = read_wordle()
	random.shuffle(valid_words)
	selected_words = valid_words[:args.max_questions]

	# Generate the output filename
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: ' + outfile)

	# Write the generated questions to the output file
	with open(outfile, 'w') as file:
		N = 0
		for word in selected_words:
			N += 1
			bbformat = generate_complete_question(N, word)
			file.write(bbformat)
	print(f'saved {N} questions to {outfile}')


#===============================
#===============================
# Starting point of the script
if __name__ == '__main__':
	main()
