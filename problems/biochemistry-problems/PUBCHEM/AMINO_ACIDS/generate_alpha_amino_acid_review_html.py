#!/usr/bin/env python3

import argparse
import os
import sys
import yaml

import bptools

def get_pubchem_dir():
	git_root = bptools._get_git_root(os.path.dirname(__file__))
	if git_root is None:
		raise RuntimeError("Unable to locate git root for PubChem imports.")
	return os.path.join(git_root, 'problems', 'biochemistry-problems', 'PUBCHEM')


_PUBCHEM_DIR = get_pubchem_dir()
if _PUBCHEM_DIR not in sys.path:
	sys.path.insert(0, _PUBCHEM_DIR)

import pubchemlib
import moleculelib


DEFAULT_CHOICES_FILE = "amino_acid_distractors.yml"
DEFAULT_OUTPUT_FILE = "alpha_amino_acid_review.html"


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
		if not isinstance(distractors, list) or len(distractors) < 3:
			raise ValueError(f"Need at least three distractors for {name}.")
	return sets


#======================================
#======================================
def get_smiles(pcl: pubchemlib.PubChemLib, name: str) -> str:
	"""Fetch SMILES for a molecule name using the PubChem cache."""
	molecule_data = pcl.get_molecule_data_dict(name)
	if molecule_data is None:
		raise ValueError(f"PubChem lookup failed for {name}")
	smiles = molecule_data.get("SMILES")
	if smiles is None:
		raise ValueError(f"Missing SMILES for {name}")
	return smiles


#======================================
#======================================
def build_card_html(label: str, name: str, smiles: str, accent: str) -> str:
	"""Build a single review card with RDKit canvas."""
	canvas_html = moleculelib.generate_html_for_molecule(smiles, None, width=320, height=240)
	return (
		"<div class='card'>"
		f"<div class='label' style='color:{accent};'>{label}: {name}</div>"
		f"{canvas_html}"
		"</div>"
	)


#======================================
#======================================
def build_section_html(set_name: str, alpha_name: str, distractors: list[str],
		pcl: pubchemlib.PubChemLib) -> str:
	"""Build the HTML section for one amino-acid set."""
	alpha_smiles = get_smiles(pcl, alpha_name)
	alpha_card = build_card_html("Alpha", alpha_name, alpha_smiles, "#0f766e")

	distractor_cards = []
	for name in distractors:
		smiles = get_smiles(pcl, name)
		distractor_cards.append(build_card_html("Distractor", name, smiles, "#b45309"))

	cards_html = alpha_card + "".join(distractor_cards)
	return (
		"<section class='set'>"
		f"<h2>{set_name.title()}</h2>"
		"<div class='grid'>"
		f"{cards_html}"
		"</div>"
		"</section>"
	)


#======================================
#======================================
def build_html(sets: dict[str, dict], pcl: pubchemlib.PubChemLib) -> str:
	"""Build the full instructor review HTML page."""
	sections = []
	for set_name in sorted(sets.keys()):
		entry = sets[set_name]
		alpha_name = entry.get("alpha")
		distractors = list(entry.get("distractors", []))
		sections.append(build_section_html(set_name, alpha_name, distractors, pcl))

	style_block = (
		"<style>"
		"body { font-family: Arial, sans-serif; margin: 24px; color: #111; }"
		"h1 { margin-bottom: 0.2em; }"
		".note { color: #555; margin-bottom: 1.5em; }"
		".set { border: 2px solid #e5e7eb; border-radius: 12px; padding: 16px; "
		"margin-bottom: 24px; background: #fafafa; }"
		".grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); "
		"gap: 16px; }"
		".card { border: 1px solid #e5e7eb; border-radius: 10px; padding: 12px; "
		"background: #fff; }"
		".label { font-weight: 700; margin-bottom: 8px; }"
		"</style>"
	)

	load_script = moleculelib.generate_load_script()

	body = (
		"<h1>Alpha-Amino Acid Review</h1>"
		"<div class='note'>RDKit canvas renders from PubChem SMILES. "
		"Each section shows the alpha amino acid and its aligned distractors.</div>"
		+ "".join(sections)
	)

	return (
		"<!DOCTYPE html>"
		"<html><head><meta charset='utf-8'>"
		f"{style_block}"
		f"{load_script}"
		"</head><body>"
		f"{body}"
		"</body></html>"
	)


#======================================
#======================================
def parse_arguments():
	parser = argparse.ArgumentParser(
		description="Generate an instructor review page for alpha-amino-acid choices."
	)
	parser.add_argument(
		'-f', '-y', '--file', metavar='<file>', type=str, dest='input_yaml_file',
		help='YAML file with alpha and distractor lists'
	)
	parser.add_argument(
		'-o', '--output', metavar='<file>', type=str, dest='output_file',
		help='HTML output file'
	)
	args = parser.parse_args()
	return args


#======================================
#======================================
def main():
	args = parse_arguments()
	if args.input_yaml_file is None:
		args.input_yaml_file = os.path.join(os.path.dirname(__file__), DEFAULT_CHOICES_FILE)
	if args.output_file is None:
		args.output_file = os.path.join(os.path.dirname(__file__), DEFAULT_OUTPUT_FILE)

	sets = load_choices(args.input_yaml_file)
	pcl = pubchemlib.PubChemLib()
	html_text = build_html(sets, pcl)
	pcl.close()

	with open(args.output_file, "w") as file:
		file.write(html_text)
	print(f"Wrote {args.output_file}")


#======================================
#======================================
if __name__ == "__main__":
	main()
