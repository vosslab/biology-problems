#!/usr/bin/env python3

# external python/pip modules
import sys

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
def write_question_batch(start_num: int, args) -> list[str]:
	questions = []
	pcl = pubchemlib.PubChemLib()
	N = start_num
	for amino_acid_name in aminoacidlib.amino_acids_fullnames:
		complete_question = write_question(N, amino_acid_name, pcl, args.num_choices)
		if complete_question is None:
			continue
		questions.append(complete_question)
		N += 1
	pcl.close()
	return questions

#======================================
#======================================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate amino acid structure matching questions.", batch=True)
	parser = bptools.add_choice_args(parser, default=4)
	args = parser.parse_args()
	return args

#======================================
#======================================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile(f"{args.num_choices}_choices")
	questions = bptools.collect_question_batches(write_question_batch, args)
	bptools.write_questions_to_file(questions, outfile)

#======================================
#======================================
if __name__ == '__main__':
	main()
