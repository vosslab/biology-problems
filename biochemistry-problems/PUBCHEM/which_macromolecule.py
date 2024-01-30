#!/usr/bin/env python3

# external python/pip modules
import os
import yaml
import random
import argparse

# local repo modules
import bptools
import pubchemlib
import moleculelib

bptools.use_insert_hidden_terms = False
bptools.use_add_no_click_div = False
used_macromolecule_names = {}


#======================================
#======================================
choices_dict = {
	'carbohydrates':	'<strong><span style="color: #0a9bf5;">Carbohydrates</span></strong>', #SKY BLUE
	'lipids': 			'<strong><span style="color: #e69100;">Lipids</span></strong>', #LIGHT ORANGE
	'proteins': 		'<strong><span style="color: #009900;">Proteins</span></strong>', #GREEN
	'nucleic acids':	'<strong><span style="color: #e60000;">Nucleic acids</span></strong>', #RED
}

#======================================
#======================================
choices_dict = {
	'carbohydrates':	'<strong><span style="color: #0a9bf5;">Carbohydrates (monosaccharides)</span></strong>', #SKY BLUE
	'lipids': 			'<strong><span style="color: #e69100;">Lipids (fatty acids)</span></strong>', #LIGHT ORANGE
	'proteins': 		'<strong><span style="color: #009900;">Proteins (amino acids and dipeptides)</span></strong>', #GREEN
	'nucleic acids':	'<strong><span style="color: #e60000;">Nucleic acids (nucleobases)</span></strong>', #RED
}

def td_header(color_id):
	return f'<tr><td style="background-color: {color_id};">'

#======================================
#======================================
def get_guide_text():
	ul_header = '<ul style="margin: 3px; font-size: 90%;">'

	html_text = f"""
	<table style="border-collapse: collapse; border: black solid 1px;">
	<tr><th style="background-color: #d3d3d3;">
	Guide to Identifying the Chemical Structures of Macromolecules
	</th></tr>

	{td_header('#e7f5fe')}
	{choices_dict['carbohydrates']}
	{ul_header}
		<li>Should have about the same number of oxygens as carbons.</li>
		<li>Look for hydroxyl groups (&ndash;OH) attached to the carbon atoms.</li>
		<li>Carbonyl groups (C=O) are often present as well.</li>
		<li>Look for the base unit of CH<sub>2</sub>O.</li>
		<li>Larger carbohydrates will form hexagon or pentagon ring-like structures.</li>
	</ul></td></tr>

	{td_header('#fff6e6')}
	{choices_dict['lipids']}
	{ul_header}
		<li>Contain mostly carbon and hydrogen.</li>
		<li>Very few oxygens and often no nitrogens.</li>
		<li>Fats and oils will have carboxyl groups (&ndash;COOH) and ester bonds</li>
		<li>Look for long chains or ring structures of only carbon and hydrogen.</li>
		<li>Steroids have four interconnected carbon rings.</li>
	</ul></td></tr>

	{td_header('#e6ffe6')}
	{choices_dict['proteins']}
	{ul_header}
		<li>Always have a nitrogen/amino group (&ndash;NH<sub>2</sub> or &ndash;NH<sub>3</sub><sup>+</sup>)</li>
		<li>Always have a carboxyl group (&ndash;COOH or &ndash;COO<sup>-</sup>)</li>
		<li>Identify the central C<sub>&alpha;</sub> (alpha-carbon) attached to an amino group and a carboxyl group</li>
		<li>Larger protein macromolecules will have a characteristic peptide bond (C&ndash;N)</li>
		<li>Try to identify common side chains (R groups).</li>
	</ul></td></tr>

	{td_header('#ffe6e6')}
	{choices_dict['nucleic acids']}
	{ul_header}
		<li>Must have a nucleobase, rings containing carbon and nitrogen.</li>
		<li>Larger nucleic acids will have a sugar backbone and phosphate groups.</li>
	</ul></td></tr>

	{td_header('#f7e8fc')}
	<strong><span style="color: #7b12a1;">Phosphate groups (&ndash;PO<sub>4</sub><sup>2-</sup>)</span></strong>
	{ul_header}
		<li>Found in all of the macromolecule types.</li>
		<li>It is best to ignore them to not let them confuse you.</li>
		<li>The breakdown of carbohydrates involves add phosphates.</li>
		<li>Membrane lipids have phosphate head groups.</li>
		<li>Many proteins are phosphorylated for regulatory purposes.</li>
		<li>DNA has a phosphate backbone.</li>
	</ul></td></tr>
	</table>
	"""
	html_text = html_text.replace('\n', ' ')
	html_text = html_text.replace('\t', ' ')
	while '  ' in html_text:
		html_text = html_text.replace('  ', ' ')
	return html_text

#======================================
#======================================
def get_question_text(molecule_name, pcl):
	question_text = ""
	question_text += moleculelib.generate_load_script()
	question_text += get_guide_text()

	molecule_data = pcl.get_molecule_data_dict(molecule_name)
	if molecule_data is None:
		print(f"FAIL: {molecule_name}")
		return None
	info_table = pcl.generate_molecule_info_table(molecule_data)
	smiles = molecule_data.get('SMILES')
	pubchem_image = moleculelib.generate_html_for_molecule(smiles, molecule_name, width=480, height=512)

	question_text += '<table style="border-collapse: collapse; border: 0px;"><tr><td>'
	question_text += pubchem_image
	question_text += '</td><td>'
	question_text += info_table
	question_text += '</td></tr></table>'

	question_text +=  f"<h3>Which one of the four main types of macromolecules is represented by the chemical structure of {molecule_name} shown above?</h3>"
	question_text += moleculelib.generate_load_script()

	return question_text


#======================================
#======================================
def get_random_molecule_name(macro_type, macro_data) -> str:
	molecule_name = select_random_molecule_name(macro_type, macro_data)
	rejections = 0
	while used_macromolecule_names.get(molecule_name) is True:
		rejections += 1
		print(f'USED ALREADY {rejections} :: molecule_name = {molecule_name}')
		molecule_name = select_random_molecule_name(macro_type, macro_data)
		if rejections > 5:
			return None
	used_macromolecule_names[molecule_name] = True
	return molecule_name

#======================================
#======================================
def select_random_molecule_name(macro_type, macro_data) -> str:
	group_name = random.choice(list(macro_data[macro_type].keys()))
	molecule_group_list = macro_data[macro_type][group_name]
	print(f'molecule_group = {group_name}'
		+ f'... {len(molecule_group_list)} molecules to choose from')
	molecule_name = random.choice(molecule_group_list)
	return molecule_name

#======================================
#======================================
def write_question(N: int, pcl, macro_data) -> str:
	# Add more to the question based on the given letters

	choices_list = list(choices_dict.values())
	macro_type = random.choice(list(choices_dict.keys()))
	answer_text = choices_dict[macro_type]
	molecule_name = get_random_molecule_name(macro_type, macro_data)
	if molecule_name is None:
		return None

	question_text = get_question_text(molecule_name, pcl)
	if question_text is None:
		return None

	# Complete the question formatting
	complete_question = bptools.formatBB_MC_Question(N, question_text, choices_list, answer_text)

	return complete_question

#======================================
#======================================
def load_molecules(macro_file=None):
	if macro_file is None:
		macro_file = 'macromolecules.yml'
	with open(macro_file, 'r') as file:
		macro_data = yaml.safe_load(file)
	return macro_data

#======================================
#======================================
def main():
	# Define argparse for command-line options
	parser = argparse.ArgumentParser(description="Generate questions.")
	parser.add_argument('-d', '--duplicates', type=int, default=95, help="Number of questions to create.")
	parser.add_argument('-f', '-y', '--file', metavar='<file>', type=str, dest='input_yaml_file',
		help='yaml input file to process')
	args = parser.parse_args()

	# Output file setup
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print(f'writing to file: {outfile}')

	pcl = pubchemlib.PubChemLib()
	macro_data = load_molecules(args.input_yaml_file)

	# Create and write questions to the output file
	with open(outfile, 'w') as f:
		N = 1
		for d in range(args.duplicates):
			complete_question = write_question(N, pcl, macro_data)
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
