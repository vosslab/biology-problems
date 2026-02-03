#!/usr/bin/env python3

import os
import random
import yaml

import bptools
import pubchemlib
import moleculelib

bptools.use_insert_hidden_terms = False
bptools.use_add_no_click_div = False
bptools.use_nocopy_script = False

PCL = None
AMINO_ACID_SETS: dict[str, dict] = {}

NUMERALS = ("I", "II", "III", "IV")
NUM_CHOICES = 4
NUM_DISTRACTORS = 3
DEFAULT_CHOICES_FILE = "amino_acid_distractors.yml"


#======================================
#======================================
def build_choice_html(numeral: str, smiles: str) -> str:
	"""Return an HTML choice block with a canvas and label."""
	crc_code = bptools.getCrc16_FromString(f"{numeral}-{smiles}")
	canvas_id = f"canvas_alpha_{crc_code}"
	canvas_html = f"<canvas id='{canvas_id}' width='260' height='200'></canvas>"
	script_html = moleculelib.generate_js_functions(smiles, canvas_id, None)
	choice_html = (
		"<div style='display:flex;align-items:center;gap:0.8em;'>"
		f"<div style='font-weight:700;font-size:1.1em;width:2.2em;'>{numeral}</div>"
		f"<div>{canvas_html}</div>"
		"</div>"
		f"{script_html}"
	)
	return choice_html


#======================================
#======================================
def get_smiles(molecule_name: str) -> str:
	"""Fetch the SMILES string for a molecule name using PubChem."""
	molecule_data = PCL.get_molecule_data_dict(molecule_name)
	if molecule_data is None:
		raise ValueError(f"PubChem lookup failed for {molecule_name}")
	smiles = molecule_data.get("SMILES")
	if smiles is None:
		raise ValueError(f"Missing SMILES for {molecule_name}")
	return smiles


#======================================
#======================================
def load_choices(input_yaml_file: str) -> dict[str, dict]:
	"""Load alpha/distractor sets from YAML."""
	with open(input_yaml_file, "r") as file:
		data = yaml.safe_load(file)
	sets = data.get("amino_acid_sets", {})
	if not isinstance(sets, dict) or len(sets) == 0:
		raise ValueError("No amino_acid_sets found in the choice YAML.")
	for name, entry in sets.items():
		alpha_name = entry.get("alpha")
		distractors = entry.get("distractors", [])
		if not alpha_name:
			raise ValueError(f"Missing alpha entry for {name}.")
		if not isinstance(distractors, list) or len(distractors) < NUM_DISTRACTORS:
			raise ValueError(f"Need at least three distractors for {name}.")
	return sets


#======================================
#======================================
def pick_choice_set(args) -> tuple[str, str, list[str]]:
	"""Return the chosen set name, alpha name, and distractors."""
	if args.amino_acid is not None:
		set_name = args.amino_acid.strip()
		entry = AMINO_ACID_SETS.get(set_name)
		if entry is None:
			raise ValueError(f"Unknown amino acid set: {set_name}")
	else:
		set_name = random.choice(sorted(AMINO_ACID_SETS.keys()))
		entry = AMINO_ACID_SETS[set_name]
	alpha_name = entry.get("alpha")
	distractors = list(entry.get("distractors", []))
	return set_name, alpha_name, distractors


#======================================
#======================================
def build_question_text() -> str:
	alpha_emph = "<span style='color:#0066cc;font-weight:700;'>&alpha;-amino acid</span>"
	return (
		"<p>Which of the following (I, II, III, IV) is an "
		f"{alpha_emph}?</p>"
		"<p>Select one answer.</p>"
	)


#======================================
#======================================
def write_question(question_num: int, args) -> str:
	"""Create a complete formatted question."""
	assert question_num > 0, "Question number must be positive"

	question_text = moleculelib.generate_load_script()
	question_text += build_question_text()

	_, alpha_name, distractors = pick_choice_set(args)
	distractors = random.sample(distractors, NUM_DISTRACTORS)
	options = [{"name": alpha_name, "is_alpha": True}]
	options += [{"name": name, "is_alpha": False} for name in distractors]
	random.shuffle(options)

	choices_list = []
	answer_text = None
	for idx in range(NUM_CHOICES):
		option = options[idx]
		numeral = NUMERALS[idx]
		smiles = get_smiles(option["name"])
		choice_html = build_choice_html(numeral, smiles)
		choices_list.append(choice_html)
		if option["is_alpha"]:
			answer_text = choice_html

	if answer_text is None:
		raise ValueError("No alpha-amino acid choice was selected.")

	return bptools.formatBB_MC_Question(question_num, question_text, choices_list, answer_text)


#======================================
#======================================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Identify an alpha-amino acid from structures.")
	parser.add_argument(
		'-f', '-y', '--file', metavar='<file>', type=str, dest='input_yaml_file',
		help='YAML file with alpha and distractor lists'
	)
	parser.add_argument(
		'-a', '--amino-acid', metavar='NAME', type=str, dest='amino_acid',
		help='Select a specific amino acid set from the YAML'
	)
	args = parser.parse_args()
	return args


#======================================
#======================================
def main():
	global PCL
	global AMINO_ACID_SETS
	args = parse_arguments()
	if args.input_yaml_file is None:
		args.input_yaml_file = os.path.join(os.path.dirname(__file__), DEFAULT_CHOICES_FILE)
	AMINO_ACID_SETS = load_choices(args.input_yaml_file)
	PCL = pubchemlib.PubChemLib()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)
	PCL.close()


#======================================
#======================================
if __name__ == '__main__':
	main()
