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
def get_question_text(molecule_name, pcl):
	molecule_data = pcl.get_molecule_data_dict(molecule_name)
	if molecule_data is None:
		print(f"FAIL: {molecule_name}")
		sys.exit(1)
	#info_table = pcl.generate_molecule_info_table(molecule_data)
	smiles = molecule_data.get('SMILES')
	pubchem_image = moleculelib.generate_html_for_molecule(smiles, '', width=480, height=320)

	question_text = ""
	question_text += moleculelib.generate_load_script()
	question_text += pubchem_image
	question_text +=  "<h3>Which amino acid is represented by the chemical structure shown above?</h3>"

	return question_text

#======================================
#======================================
def write_question(N: int, amino_acid_name: str, pcl: object, num_choices: int, args) -> str:

	question_text = get_question_text(amino_acid_name, pcl)
	if question_text is None:
		return None

	if args.question_type == 'fib':
		answers_set = set()
		answers_set.add(amino_acid_name)
		answers_set.add(amino_acid_name.title())
		answers_set.add(amino_acid_name.replace(' ', ''))
		answers_set.add(amino_acid_name.title().replace(' ', ''))
		answers_list = sorted(answers_set)
		# Complete the question formatting
		complete_question = bptools.formatBB_FIB_Question(N, question_text, answers_list)
	else:
		choices_list = aminoacidlib.get_similar_amino_acids(amino_acid_name, num=num_choices-1, pcl=pcl)
		choices_list.append(amino_acid_name)
		choices_list.sort()
		complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, amino_acid_name)

	return complete_question

#======================================
#======================================
def write_question_batch(start_num: int, args) -> list[str]:
	questions = []
	pcl = pubchemlib.PubChemLib()
	N = start_num
	for amino_acid_name in aminoacidlib.amino_acids_fullnames:
		complete_question = write_question(N, amino_acid_name, pcl, args.num_choices, args)
		if complete_question is None:
			continue
		questions.append(complete_question)
		N += 1
		if args.max_questions is not None and len(questions) >= args.max_questions:
			break
	pcl.close()
	return questions

#======================================
#======================================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate amino acid ID questions.", batch=True)
	parser = bptools.add_choice_args(parser, default=7)
	parser = bptools.add_question_format_args(
		parser,
		types_list=['mc', 'fib'],
		required=False,
		default='mc'
	)
	args = parser.parse_args()
	return args

#======================================
#======================================
def main():
	args = parse_arguments()
	outfile_suffix = args.question_type.upper()
	if args.question_type == 'mc':
		outfile = bptools.make_outfile(outfile_suffix, f"{args.num_choices}_choices")
	else:
		outfile = bptools.make_outfile(outfile_suffix)
	questions = bptools.collect_question_batches(write_question_batch, args)
	bptools.write_questions_to_file(questions, outfile)

#======================================
#======================================
if __name__ == '__main__':
	main()
