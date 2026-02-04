#!/usr/bin/env python3

# external python/pip modules
import os
import sys
import random

# local repo modules
import bptools

def get_pubchem_dir():
	git_root = bptools._get_git_root(os.path.dirname(__file__))
	if git_root is None:
		raise RuntimeError("Unable to locate git root for PubChem imports.")
	return os.path.join(git_root, 'problems', 'biochemistry-problems', 'PUBCHEM')


_PUBCHEM_DIR = get_pubchem_dir()
if _PUBCHEM_DIR not in sys.path:
	sys.path.insert(0, _PUBCHEM_DIR)

import moleculelib

bptools.use_insert_hidden_terms = False
bptools.use_add_no_click_div = False
bptools.use_nocopy_script = False

ALANINE_STATES = [
	{
		'state_id': 1,
		'smiles': 'C[C@@H](C(=O)O)[NH3+]',
		'carboxyl': 'COOH',
		'amino': 'NH<sub>3</sub><sup>+</sup>',
	},
	{
		'state_id': 2,
		'smiles': 'C[C@@H](C(=O)[O-])[NH3+]',
		'carboxyl': 'COO<sup>-</sup>',
		'amino': 'NH<sub>3</sub><sup>+</sup>',
	},
	{
		'state_id': 3,
		'smiles': 'C[C@@H](C(=O)[O-])N',
		'carboxyl': 'COO<sup>-</sup>',
		'amino': 'NH<sub>2</sub>',
	},
	{
		'state_id': 4,
		'smiles': 'C[C@@H](C(=O)O)N',
		'carboxyl': 'COOH',
		'amino': 'NH<sub>2</sub>',
	},
]

PH_MIN = 1.0
PH_MAX = 12.5
PH_STEP = 0.1
PH_TENTH_MIN = int(round(PH_MIN * 10))
PH_TENTH_MAX = int(round(PH_MAX * 10))

SCENARIOS = []

#======================================
#======================================
def format_ph_value(ph_value: float) -> str:
	"""Format the pH value to one decimal place for consistent display."""
	formatted = f"{ph_value:.1f}"
	return formatted

#======================================
#======================================
def state_for_ph(ph_value: float) -> int:
	"""Return the alanine state id for a given pH value."""
	if ph_value < 2.34:
		return 1
	if ph_value < 9.69:
		return 2
	return 3

#======================================
#======================================
def build_ph_scenarios() -> list[dict]:
	"""Generate all unique pH scenarios with one-decimal precision."""
	ph_tenths = list(range(PH_TENTH_MIN, PH_TENTH_MAX + 1))
	scenarios = []
	for ph_tenth in ph_tenths:
		ph_value = ph_tenth / 10.0
		state_id = state_for_ph(ph_value)
		scenarios.append({'ph': ph_value, 'state_id': state_id})
	return scenarios

#======================================
#======================================
def sort_by_ph(entry: dict) -> float:
	"""Sort helper for pH scenarios."""
	return entry['ph']

#======================================
#======================================
def build_question_text(ph_value: float) -> str:
	"""Assemble the HTML question text with emphasized pH."""
	ph_text = format_ph_value(ph_value)
	ph_emph = (
		"<span style='color:#0066cc;font-size:1.35em;font-weight:700;"
		"background-color:#e6f2ff;padding:0.1em 0.4em;border-radius:4px;'>"
		f"pH {ph_text}</span>"
	)
	question_text = moleculelib.generate_load_script()
	question_text += "<h3>Alanine Charge States</h3>"
	question_text += "<p>Alanine has two pKa values: 2.34 and 9.69.</p>"
	question_text += (
		"<p><strong>Question:</strong> Which one of the following is the correct "
		f"charge state of alanine at {ph_emph}?</p>"
	)
	question_text += "<p>Select one answer.</p>"
	return question_text

#======================================
#======================================
def build_choice_html(question_num: int, state: dict) -> str:
	"""Build a single HTML choice block with a canvas and charge labels."""
	state_label = f"State {state['state_id']}"
	crc_code = bptools.getCrc16_FromString(f"{question_num}-{state_label}-{state['smiles']}")
	canvas_id = f"canvas_alanine_{crc_code}"
	canvas_html = f"<canvas id='{canvas_id}' width='320' height='240'></canvas>"
	script_html = moleculelib.generate_js_functions(state['smiles'], canvas_id, None)

	details_html = (
		"<div style='font-size:0.9em;line-height:1.4;'>"
		f"Carboxyl: <strong>{state['carboxyl']}</strong><br/>"
		f"Amino: <strong>{state['amino']}</strong>"
		"</div>"
	)
	choice_html = (
		"<div style='border:1px solid #ddd;border-radius:8px;padding:0.8em;'>"
		"<div style='display:flex;align-items:center;gap:1.2em;'>"
		f"<div style='flex-shrink:0;'>{canvas_html}</div>"
		f"<div style='flex-grow:1;'>{details_html}</div>"
		"</div></div>"
		f"{script_html}"
	)
	return choice_html

#======================================
#======================================
def write_question(question_num: int, args) -> str:
	"""Generate one alanine protonation-state question."""
	if question_num > len(SCENARIOS):
		return None
	scenario = SCENARIOS[question_num - 1]
	ph_value = scenario['ph']
	correct_label = f"State {scenario['state_id']}"

	question_text = build_question_text(ph_value)
	state_pool = list(ALANINE_STATES)
	random.shuffle(state_pool)

	choices_list = []
	answer_text = None
	for state in state_pool:
		choice_html = build_choice_html(question_num, state)
		choices_list.append(choice_html)
		if f"State {state['state_id']}" == correct_label:
			answer_text = choice_html

	if answer_text is None:
		raise ValueError("No correct answer was assigned for the selected pH.")

	complete_question = bptools.formatBB_MC_Question(
		question_num, question_text, choices_list, answer_text
	)
	return complete_question

#======================================
#======================================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate alanine protonation-state questions.")
	parser = bptools.add_scenario_args(parser)
	args = parser.parse_args()
	return args

#======================================
#======================================
def main():
	global SCENARIOS
	args = parse_arguments()
	SCENARIOS = build_ph_scenarios()
	if args.scenario_order == 'sorted':
		SCENARIOS.sort(key=sort_by_ph)
	else:
		random.shuffle(SCENARIOS)
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)

#======================================
#======================================
if __name__ == '__main__':
	main()
