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

bptools.use_insert_hidden_terms = False
bptools.use_add_no_click_div = False

amino_acids = [
	"alanine",
	"arginine",
	"asparagine",
	"aspartic acid",
	"cysteine",
	"glutamic acid",
	"glutamine",
	"glycine",
	"histidine",
	"isoleucine",
	"leucine",
	"lysine",
	"methionine",
	"phenylalanine",
	"proline",
	"serine",
	"threonine",
	"tryptophan",
	"tyrosine",
	"valine"
]

#======================================
#======================================
def parse_formula(formula):
	"""Parse a chemical formula into a dictionary of elements and their counts."""
	import re
	pattern = r'([A-Z][a-z]*)(\d*)'
	elements = re.findall(pattern, formula)
	return {element: int(count) if count else 1 for element, count in elements}

#======================================
#======================================
def formula_disimilarity(formula1, formula2):
	"""Calculate similarity between two chemical formulas."""
	parsed1 = parse_formula(formula1)
	parsed2 = parse_formula(formula2)
	backbone_formula = 'C2H3NO'
	backbone_parsed = parse_formula(backbone_formula)

	# Subtract the backbone elements from each formula
	for element, count in backbone_parsed.items():
		parsed1[element] = max(parsed1.get(element, 0) - count, 0)
		parsed2[element] = max(parsed2.get(element, 0) - count, 0)

	common_elements = set(parsed1.keys()) & set(parsed2.keys())
	total_elements = set(parsed1.keys()) | set(parsed2.keys())

	disimilarity = sum(abs(parsed1[el] - parsed2[el]) for el in common_elements)
	total_counts = sum(parsed1.get(el, 0) + parsed2.get(el, 0) for el in total_elements)

	return disimilarity / total_counts if total_counts else 0

#======================================
#======================================
def get_similar_amino_acids(aa_name, pcl, num=5):
	target_data = pcl.get_molecule_data_dict(aa_name)
	disimilarities = []

	#print(f"search amino acid '{aa_name}'")
	for other_aa_name in amino_acids:
		if other_aa_name == aa_name:
			continue

		data = pcl.get_molecule_data_dict(other_aa_name)

		#glycine_mw = 75.07
		weight_diff = abs(target_data["Molecular weight"] - data["Molecular weight"])/target_data["Molecular weight"]
		formula_disim = formula_disimilarity(target_data["Molecular formula"], data["Molecular formula"])

		# Combine the weight difference and formula similarity into a single score
		# Adjust the formula to prioritize either property
		score = (formula_disim*100 + weight_diff*20)
		#print(f'score={score:.2f} form->{formula_disim*100:.2f}, mass->{weight_diff*60:.2f} :: {other_aa_name}')

		disimilarities.append((other_aa_name, score))

	# Sort by the score in descending order and return the top `num` amino acids
	disimilarities.sort(key=lambda x: x[1], reverse=False)

	return [aa for aa, _ in disimilarities[:num]]


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
def write_question(N: int, pcl: object, num_choices: int) -> str:
	# Add more to the question based on the given letters

	answer_amino_acid = random.choice(amino_acids)

	choices_list = get_similar_amino_acids(answer_amino_acid, pcl, num=num_choices-1)
	choices_list.append(answer_amino_acid)
	choices_list.sort()

	question_text = get_question_text(answer_amino_acid, pcl)
	if question_text is None:
		return None

	# Complete the question formatting
	complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_amino_acid)

	return complete_question

#======================================
#======================================
def main():
	# Define argparse for command-line options
	parser = argparse.ArgumentParser(description="Generate questions.")
	parser.add_argument('-d', '--duplicates', type=int, default=95, help="Number of questions to create.")
	parser.add_argument('-c', '--num_choices', type=int, default=7, help="Number of choices to create.")
	args = parser.parse_args()

	# Output file setup
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print(f'writing to file: {outfile}')

	pcl = pubchemlib.PubChemLib()

	# Create and write questions to the output file
	with open(outfile, 'w') as f:
		N = 1
		for d in range(args.duplicates):
			complete_question = write_question(N, pcl, args.num_choices)
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
