"""Generate native or MC ordering questions from keyed YAML steps.

Each step supplies alternative presentations of the same position. Every step
is used. MC choices are permutations of the complete selected sequence.
"""

import os
import re
import sys
import random
import argparse
import functools

import bptools


#============================================
def ordered_steps(bank: dict) -> list[tuple[str, list]]:
	"""Read step ranks without depending on YAML mapping insertion order."""
	steps = bank['steps']
	ranked = []
	for key, alternatives in steps.items():
		if re.fullmatch(r'step [1-9][0-9]*', key) is None:
			raise ValueError(f'Invalid step key: {key!r}; use step 1, step 2, ...')
		if not isinstance(alternatives, list) or not alternatives:
			raise ValueError(f'{key} must contain a nonempty list of alternatives.')
		ranked.append((int(key.split()[1]), key, alternatives))
	if len(ranked) < 2:
		raise ValueError('An ordering bank needs at least two steps.')
	ranked.sort()
	result = [(key, alternatives) for _, key, alternatives in ranked]
	return result


#============================================
def render_molecules(molecules: list[dict]) -> tuple[list[str], str]:
	"""Reuse the existing glycolysis structures and ordered-name clue."""
	pubchem_dir = os.path.join(os.path.dirname(__file__), '..',
		'biochemistry-problems', 'PUBCHEM')
	if pubchem_dir not in sys.path:
		sys.path.insert(0, pubchem_dir)
	import moleculelib

	structures = []
	for molecule in molecules:
		structure = moleculelib.generate_html_for_molecule(
			molecule['SMILES'], molecule_name=' ', width=512, height=256)
		structures.append(structure)
	load_script = moleculelib.generate_load_script()
	return structures, load_script


#============================================
def question_content(bank: dict, steps: list[tuple[str, list]],
		mc: bool) -> tuple[str, list[str], str]:
	"""Choose one alternative per step and format each prose field once."""
	selected = [random.choice(alternatives) for _, alternatives in steps]
	rules = bank.get('replacement_rules')
	override = bank.get('question override')
	if override is not None:
		prompt = override
		lead_out = 'Which sequence gives the correct order?'
	elif mc:
		prompt = f"The following steps describe {bank['topic']}."
		lead_out = 'Which sequence puts these steps in order from first to last?'
	else:
		prompt = f"Place the following steps of {bank['topic']} in order from first to last."
		lead_out = ''
	prompt = f'<p>{prompt}</p>'
	if all(isinstance(value, dict) for value in selected):
		names = [f"{value['name']} ({value['abbreviation']})" for value in selected]
		prompt += '<p>The correct sequence of the molecule names is:</p><ol>'
		prompt += ''.join(f'<li>{name}</li>' for name in names) + '</ol>'
		prompt = bptools.applyReplacementRulesToText(prompt, rules)
		items, load_script = render_molecules(selected)
		prompt += load_script
	else:
		prompt = bptools.applyReplacementRulesToText(prompt, rules)
		items = bptools.applyReplacementRulesToList(selected, rules)
	if lead_out:
		lead_out = bptools.applyReplacementRulesToText(lead_out, rules)
	return prompt, items, lead_out


#============================================
def sequence_choices(correct: list[int]) -> tuple[list[str], str]:
	"""Create complete alternative sequences by swapping neighbors or reversing."""
	wrong_orders = []
	for index in range(len(correct) - 1):
		wrong = correct.copy()
		# Error: neighboring stages are performed in the wrong order.
		wrong[index], wrong[index + 1] = wrong[index + 1], wrong[index]
		wrong_orders.append(wrong)
	# Error: the ordering direction is reversed.
	wrong_orders.append(list(reversed(correct)))
	answer = ' &rarr; '.join(str(number) for number in correct)
	choices = [answer]
	for wrong in random.sample(wrong_orders, 3):
		choices.append(' &rarr; '.join(str(number) for number in wrong))
	random.shuffle(choices)
	return choices, answer


#============================================
def write_question(N: int, args: argparse.Namespace, bank: dict,
		steps: list[tuple[str, list]], mc: bool) -> object:
	"""Render the complete ordered set in the selected assessment format."""
	prompt, items, lead_out = question_content(bank, steps, mc)
	if not mc:
		question = bptools.formatBB_ORD_Question(N, prompt, items)
		return question
	display_order = random.sample(range(len(items)), len(items))
	labels = {step_index: label for label, step_index in enumerate(display_order, start=1)}
	correct = [labels[index] for index in range(len(items))]
	prompt += '<ol>'
	prompt += ''.join(f'<li>{items[index]}</li>' for index in display_order)
	prompt += f'</ol><p>{lead_out}</p>'
	choices, answer = sequence_choices(correct)
	question = bptools.formatBB_MC_Question(N, prompt, choices, answer)
	return question


#============================================
def parse_arguments() -> argparse.Namespace:
	"""Use the same file and shared generation options as the other YAML loaders."""
	parser = bptools.make_arg_parser(description=__doc__)
	parser.add_argument('-f', '-y', '--file', dest='input_yaml_file', required=True)
	args = parser.parse_args()
	return args


#============================================
def main(mc: bool) -> None:
	args = parse_arguments()
	bank = bptools.readYamlFile(args.input_yaml_file)
	steps = ordered_steps(bank)
	if mc and len(steps) < 3:
		raise ValueError('Four-choice MC ordering needs at least three steps.')
	if any(isinstance(value, dict) for _, alternatives in steps for value in alternatives):
		# Preserve the existing molecule generator's anti-cheat setting.
		bptools.allow_insert_hidden_terms = False
	bank_name = os.path.splitext(os.path.basename(args.input_yaml_file))[0]
	question_format = 'MCORDER' if mc else 'ORDER'
	outfile = f'bbq-{question_format}-{bank_name}-{len(steps)}_items-questions.txt'
	writer = functools.partial(write_question, bank=bank, steps=steps, mc=mc)
	bptools.collect_and_write_questions(writer, args, outfile)

