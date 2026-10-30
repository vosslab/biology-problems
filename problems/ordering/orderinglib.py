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
import qti_package_maker.common.string_functions


COLOR_PALETTE = [
	'#D40000', '#B74300', '#935D00', '#6C6C00', '#3B7600', '#007A00', '#00775F',
	'#007576', '#076DAD', '#003FFF', '#0067CC', '#A719DB', '#C80085', '#CC0066',
]
LABEL_STYLES = ('bracketed', 'numbers', 'roman', 'roman-lower', 'circled', 'dice', 'greek', 'words')
COLOR_MODES = ('full', 'labels', 'none')


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
def validate_presentation(step_count: int, label_style: str, color_mode: str) -> None:
	"""Reject unknown presentation options and label styles beyond their symbol range."""
	if label_style not in LABEL_STYLES:
		raise ValueError(f'Unknown label style {label_style!r}; choose from {", ".join(LABEL_STYLES)}.')
	if color_mode not in COLOR_MODES:
		raise ValueError(f'Unknown color mode {color_mode!r}; choose from {", ".join(COLOR_MODES)}.')
	capacities = {'circled': 20, 'dice': 6, 'greek': 24}
	capacity = capacities.get(label_style)
	if capacity is not None and step_count > capacity:
		message = f'{label_style} labels support at most {capacity} steps; '
		message += f'this bank has {step_count}.'
		raise ValueError(message)


#============================================
def labels_for_count(step_count: int, label_style: str) -> list[str]:
	"""Return the requested visible label tokens for positions starting at one."""
	validate_presentation(step_count, label_style, 'none')
	greek = ['&alpha;', '&beta;', '&gamma;', '&delta;', '&epsilon;', '&zeta;', '&eta;',
		'&theta;', '&iota;', '&kappa;', '&lambda;', '&mu;', '&nu;', '&xi;', '&omicron;',
		'&pi;', '&rho;', '&sigma;', '&tau;', '&upsilon;', '&phi;', '&chi;', '&psi;', '&omega;']
	labels = []
	for number in range(1, step_count + 1):
		if label_style == 'bracketed':
			label = f'[{number}]'
		elif label_style == 'numbers':
			label = str(number)
		elif label_style == 'roman':
			label = qti_package_maker.common.string_functions.number_to_roman(number)
		elif label_style == 'roman-lower':
			label = qti_package_maker.common.string_functions.number_to_roman(number).lower()
		elif label_style == 'circled':
			label = f'&#{9311 + number};'
		elif label_style == 'dice':
			label = f'&#{9855 + number};'
		elif label_style == 'greek':
			label = greek[number - 1]
		else:
			label = bptools.number_to_cardinal(number)
		labels.append(label)
	return labels


#============================================
def colors_for_count(step_count: int) -> list[str]:
	"""Select the display-order colors from the documented fixed palette."""
	if step_count == 4:
		indices = [0, 5, 9, 11]
	elif step_count == 6:
		indices = [0, 1, 3, 5, 9, 11]
	elif step_count <= len(COLOR_PALETTE):
		indices = [round(index * (len(COLOR_PALETTE) - 1) / (step_count - 1))
			for index in range(step_count)]
	else:
		indices = [index % len(COLOR_PALETTE) for index in range(step_count)]
	colors = [COLOR_PALETTE[index] for index in indices]
	return colors


#============================================
def format_label(position: int, labels: list[str], colors: list[str], color_mode: str) -> str:
	"""Render a choice label using the same token and display-position color everywhere."""
	token = labels[position - 1]
	if color_mode == 'none':
		return token
	return f'<span style="color: {colors[position - 1]};">{token}</span>'


#============================================
def write_question(N: int, args: argparse.Namespace, bank: dict,
		steps: list[tuple[str, list]], mc: bool) -> object:
	"""Render the complete ordered set in the selected assessment format."""
	prompt, items, lead_out = question_content(bank, steps, mc)
	if not mc:
		question = bptools.formatBB_ORD_Question(N, prompt, items)
		return question
	label_style = getattr(args, 'label_style', 'bracketed')
	color_mode = getattr(args, 'color_mode', 'full')
	validate_presentation(len(items), label_style, color_mode)
	display_order = random.sample(range(len(items)), len(items))
	labels = {step_index: label for label, step_index in enumerate(display_order, start=1)}
	correct = [labels[index] for index in range(len(items))]
	label_tokens = labels_for_count(len(items), label_style)
	colors = colors_for_count(len(items))
	is_molecular = all(isinstance(value, dict)
		for _, alternatives in steps for value in alternatives)
	prompt += '<ol style="list-style: none; padding-left: 0;">'
	for position, index in enumerate(display_order, start=1):
		label_html = format_label(position, label_tokens, colors, color_mode)
		item_html = items[index]
		if color_mode == 'full' and not is_molecular:
			item_html = f'<span style="color: {colors[position - 1]};">{item_html}</span>'
		prompt += f'<li>{label_html} {item_html}</li>'
	prompt += f'</ol><p>{lead_out}</p>'
	choices, answer = sequence_choices(correct)
	choice_labels = []
	for choice in choices:
		positions = [int(value) for value in choice.split(' &rarr; ')]
		choice_labels.append(' &rarr; '.join(
			format_label(position, label_tokens, colors, color_mode) for position in positions))
	answer_positions = [int(value) for value in answer.split(' &rarr; ')]
	answer = ' &rarr; '.join(
		format_label(position, label_tokens, colors, color_mode) for position in answer_positions)
	choices = choice_labels
	question = bptools.formatBB_MC_Question(N, prompt, choices, answer)
	return question


#============================================
def parse_arguments(mc: bool) -> argparse.Namespace:
	"""Use the same file and shared generation options as the other YAML loaders."""
	parser = bptools.make_arg_parser(description=__doc__)
	parser.add_argument('-f', '-y', '--file', dest='input_yaml_file', required=True)
	if mc:
		parser.add_argument('-l', '--label-style', choices=LABEL_STYLES, default='bracketed')
		parser.add_argument('-C', '--color-mode', choices=COLOR_MODES, default='full')
	args = parser.parse_args()
	return args


#============================================
def main(mc: bool) -> None:
	args = parse_arguments(mc)
	bank = bptools.readYamlFile(args.input_yaml_file)
	steps = ordered_steps(bank)
	if mc and len(steps) < 3:
		raise ValueError('Four-choice MC ordering needs at least three steps.')
	if mc:
		validate_presentation(len(steps), args.label_style, args.color_mode)
	if any(isinstance(value, dict) for _, alternatives in steps for value in alternatives):
		# Preserve the existing molecule generator's anti-cheat setting.
		bptools.allow_insert_hidden_terms = False
	bank_name = os.path.splitext(os.path.basename(args.input_yaml_file))[0]
	question_format = 'SEQUENCEMC' if mc else 'ORDER'
	outfile = f'bbq-{question_format}-{bank_name}-{len(steps)}_items-questions.txt'
	writer = functools.partial(write_question, bank=bank, steps=steps, mc=mc)
	bptools.collect_and_write_questions(writer, args, outfile)

