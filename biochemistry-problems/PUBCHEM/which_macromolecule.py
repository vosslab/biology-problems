#!/usr/bin/env python3

import yaml

import bptools
import pubchemlib

def load_molecules():
	macro_file = 'macromolecules.yml'
	with open(macro_file, 'r') as file:
		macro_data = yaml.safe_load(file)
	return macro_data

def get_guide_text():
	html_text = """
	<ul>
		<li><span style="color: goldenrod;">Carbohydrates</span> have about the same number of oxygens as carbons &ndash; base unit of CH<sub>2</sub>O</li>
		<li><span style="color: navyblue;">Proteins</span> always have a nitrogen (amino&ndash;&xrarr;NH<sub>3</sub><sup>+</sup>) and also look for the carboxyl groups (acid&ndash;&xrarr;COO<sup>&ndash;</sup>) and common side chains</li>
		<li><span style="color: darkred;">Nucleic</span> acids have carbon rings with nitrogens in the ring.</li>
		<li><span style="color: darkgreen;">Lipids</span> are mostly carbon and hydrogen, with very few, if any, oxygens or nitrogens.</li>
		<li><span style="color: purple;">Phosphates</span> can be found in any of the macromolecules above, so don't let them fool you.</li>
	</ul>
	"""
	html_text = html_text.replace('\n', ' ')
	html_text = html_text.replace('  ', ' ')




def main():
	pcl = pubchemlib.PubChemLib()
	macro_data = load_molecules()
	categories = macro_data.keys()
	print(categories)
	pcl.close()

if __name__ == '__main__':
	main()
