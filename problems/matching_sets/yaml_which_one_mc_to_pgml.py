#!/usr/bin/env python3

"""
Generate PGML "which one" multiple choice questions from matching set YAML files.

This is the PGML equivalent of yaml_make_which_one_multiple_choice.py.
"""

# Standard Library
import argparse
import itertools
import os
import random

# Local repo modules
import bptools
import webwork_lib

#============================================

def parse_args():
	"""
	Parse command-line arguments.
	"""
	parser = argparse.ArgumentParser(
		description="Generate PGML which-one MC questions from matching set YAML."
	)
	parser.add_argument(
		'-y', '--file', dest='input_yaml_file', required=True,
		help='YAML input file to process'
	)
	parser.add_argument(
		'-o', '--output', dest='output_pgml_file',
		help='Output PGML file path'
	)
	parser.add_argument(
		'-c', '--num-choices', dest='num_choices', type=int, default=None,
		help='Number of choices per question'
	)
	color_group = parser.add_mutually_exclusive_group()
	color_group.add_argument(
		'--use-colors', dest='use_colors', action='store_true',
		help='Enable inline color styling (default behavior).'
	)
	color_group.add_argument(
		'--use-color', dest='use_colors', action='store_true',
		help='Enable inline color styling (alias for --use-colors).'
	)
	color_group.add_argument(
		'--no-color', dest='no_color', action='store_true',
		help='Disable color styling.'
	)
	parser.add_argument(
		'--flip', action='store_true', dest='flip',
		help='Flip the keys and values from the YAML input'
	)
	args = parser.parse_args()
	return args

#============================================

def build_key_value_pairs(matching_pairs_dict):
	"""
	Build a list of all (key, value) pairs.
	"""
	key_value_pairs = []
	for key in matching_pairs_dict.keys():
		values = matching_pairs_dict[key]
		if not isinstance(values, list):
			values = [values]
		for value in values:
			pair = (key, value)
			key_value_pairs.append(pair)
	return key_value_pairs

#============================================

def generate_combinations(all_keys, num_choices, exclude_pairs_list):
	"""
	Generate filtered combinations of keys.
	"""
	all_combs = list(itertools.combinations(all_keys, num_choices))
	print(f'Created {len(all_combs)} combinations from {len(all_keys)} items')

	if len(exclude_pairs_list) > 0:
		filter_combs = []
		for comb in all_combs:
			excluded_comb = False
			for a, b in exclude_pairs_list:
				if a in comb and b in comb:
					excluded_comb = True
					break
			if not excluded_comb:
				filter_combs.append(comb)
		print(f'Filtered down to {len(filter_combs)} combinations')
		all_combs = filter_combs

	random.shuffle(all_combs)
	return all_combs

#============================================

def build_perl_question_data(yaml_data, num_choices, flip, replacement_rules, color_mode):
	"""
	Build Perl code for question data arrays.
	"""
	matching_pairs_dict = yaml_data['matching pairs']
	exclude_pairs_list = yaml_data.get('exclude pairs', [])

	if num_choices is None:
		num_choices = yaml_data.get('items to match per question', 5)

	all_keys = list(matching_pairs_dict.keys())
	key_value_pairs = build_key_value_pairs(matching_pairs_dict)
	all_combs = generate_combinations(all_keys, num_choices, exclude_pairs_list)

	# Build questions data
	questions_data = []
	color_classes = {}
	needs_bold_class = False
	warnings = []

	for key, value in key_value_pairs:
		# Find a combination that includes this key
		comb = random.choice(all_combs)
		count = 0
		while key not in comb:
			comb = random.choice(all_combs)
			count += 1
			if count > 200:
				raise RuntimeError("Could not find suitable combination")

		if not flip:
			# Normal: show value, ask for key
			item_name = value
			plural_choice_description = yaml_data['keys description']
			singular_item_description = yaml_data['value description']
			choices_list = list(comb)
			correct_answer = key
		else:
			# Flipped: show key, ask for value
			item_name = key
			plural_choice_description = yaml_data['values description']
			singular_item_description = yaml_data['key description']
			choices_list = [value]
			for comb_key in comb:
				if comb_key == key:
					continue
				other_values = matching_pairs_dict[comb_key]
				if not isinstance(other_values, list):
					other_values = [other_values]
				choice = random.choice(other_values)
				choices_list.append(choice)
			correct_answer = value

		# Apply replacements
		item_name = webwork_lib.apply_replacements_to_text(item_name, replacement_rules)
		choices_list = webwork_lib.apply_replacements_to_list(
			choices_list,
			replacement_rules,
		)
		correct_answer = webwork_lib.apply_replacements_to_text(
			correct_answer,
			replacement_rules,
		)
		plural_choice_description = webwork_lib.apply_replacements_to_text(
			plural_choice_description,
			replacement_rules,
		)
		singular_item_description = webwork_lib.apply_replacements_to_text(
			singular_item_description,
			replacement_rules,
		)

		item_name_html, item_bold = webwork_lib.format_label_html(
			item_name,
			color_mode,
			color_classes,
			warnings,
			label_name=item_name,
		)
		if item_bold:
			needs_bold_class = True
		item_name_html = f"<strong>{item_name_html}</strong>"

		plural_choice_html, plural_bold = webwork_lib.format_label_html(
			plural_choice_description,
			color_mode,
			color_classes,
			warnings,
			label_name=plural_choice_description,
		)
		if plural_bold:
			needs_bold_class = True

		singular_item_html, singular_bold = webwork_lib.format_label_html(
			singular_item_description,
			color_mode,
			color_classes,
			warnings,
			label_name=singular_item_description,
		)
		if singular_bold:
			needs_bold_class = True

		choices_html = []
		for choice in choices_list:
			choice_html, choice_bold = webwork_lib.format_label_html(
				choice,
				color_mode,
				color_classes,
				warnings,
				label_name=choice,
			)
			if choice_bold:
				needs_bold_class = True
			choices_html.append(choice_html)

		correct_html, correct_bold = webwork_lib.format_label_html(
			correct_answer,
			color_mode,
			color_classes,
			warnings,
			label_name=correct_answer,
		)
		if correct_bold:
			needs_bold_class = True

		question_data = {
			'item_name': item_name_html,
			'plural_choice_description': plural_choice_html,
			'singular_item_description': singular_item_html,
			'choices': choices_html,
			'correct': correct_html,
		}
		questions_data.append(question_data)

	return questions_data, color_classes, needs_bold_class, warnings

#============================================

def build_preamble_text(header_text):
	"""
	Build the PGML preamble text.
	"""
	text = ""
	text += header_text.rstrip() + "\n"
	text += "\n"
	text += "DOCUMENT();\n"
	text += "\n"
	text += "loadMacros(\n"
	text += "    'PGstandard.pl',\n"
	text += "    'PGML.pl',\n"
	text += "    'PGchoicemacros.pl',\n"
	text += "    'parserRadioButtons.pl',\n"
	text += "    'PGcourse.pl',\n"
	text += ");\n"
	text += "\n"
	text += "TEXT(beginproblem());\n"
	text += "$showPartialCorrectAnswers = 0;\n"
	text += "\n"
	return text

#============================================

def build_setup_text(questions_data):
	"""
	Build the Perl setup code for all questions.
	"""
	text = ""
	text += "#==========================================================\n"
	text += "# QUESTION DATA\n"
	text += "#==========================================================\n"
	text += "\n"
	text += "# All questions data\n"
	text += "@questions_data = (\n"

	for q_data in questions_data:
		text += "  {\n"
		text += f"    'item_name' => '{webwork_lib.escape_perl_string(q_data['item_name'])}',\n"
		text += f"    'plural_choice' => '{webwork_lib.escape_perl_string(q_data['plural_choice_description'])}',\n"
		text += f"    'singular_item' => '{webwork_lib.escape_perl_string(q_data['singular_item_description'])}',\n"
		text += "    'choices' => [\n"
		for choice in q_data['choices']:
			text += f"      '{webwork_lib.escape_perl_string(choice)}',\n"
		text += "    ],\n"
		text += f"    'correct' => '{webwork_lib.escape_perl_string(q_data['correct'])}',\n"
		text += "  },\n"

	text += ");\n"
	text += "\n"
	text += "#==========================================================\n"
	text += "# SELECT RANDOM QUESTION\n"
	text += "#==========================================================\n"
	text += "\n"
	text += "$question_idx = random(0, scalar(@questions_data) - 1, 1);\n"
	text += "$q = $questions_data[$question_idx];\n"
	text += "\n"
	text += "$item_name = $q->{'item_name'};\n"
	text += "$plural_choice = $q->{'plural_choice'};\n"
	text += "$singular_item = $q->{'singular_item'};\n"
	text += "@choices = @{ $q->{'choices'} };\n"
	text += "$correct = $q->{'correct'};\n"
	text += "\n"
	text += "#==========================================================\n"
	text += "# BUILD RADIO BUTTONS\n"
	text += "#==========================================================\n"
	text += "\n"
	text += "$rb = RadioButtons(\n"
	text += "  [@choices],\n"
	text += "  $correct,\n"
	text += "  labels        => ['A','B','C','D','E','F','G','H'],\n"
	text += "  displayLabels => 1,\n"
	text += "  randomize     => 1,\n"
	text += "  separator     => '<div style=\"margin-bottom: 0.7em;\"></div>',\n"
	text += ");\n"
	text += "\n"
	return text

#============================================

def build_statement_text(color_mode, color_classes, needs_bold_class):
	"""
	Build the PGML question text.
	"""
	text = ""
	text += "#==========================================================\n"
	text += "# PGML\n"
	text += "#==========================================================\n"
	text += "\n"
	if color_mode == "class" and (len(color_classes) > 0 or needs_bold_class):
		text += "HEADER_TEXT(MODES(TeX => '', HTML => <<END_STYLE));\n"
		text += "<style>\n"
		for class_name in sorted(color_classes.keys()):
			color_value = color_classes[class_name]
			text += f".{class_name} {{ color: {color_value}; }}\n"
		if needs_bold_class:
			text += ".pgml-bold { font-weight: 700; }\n"
		text += "</style>\n"
		text += "END_STYLE\n"
		text += "\n"
	text += "BEGIN_PGML\n"
	text += "\n"
	text += "Which one of the following [$plural_choice]* corresponds to the [$singular_item]* [$item_name]*?\n"
	text += "\n"
	text += "[_]{$rb}\n"
	text += "\n"
	text += "END_PGML\n"
	text += "\n"
	return text

#============================================

def build_solution_text():
	"""
	Build the PGML solution text.
	"""
	text = ""
	text += "BEGIN_PGML_SOLUTION\n"
	text += "\n"
	text += "The correct answer is: [$correct]*\n"
	text += "\n"
	text += "END_PGML_SOLUTION\n"
	text += "\n"
	text += "ENDDOCUMENT();\n"
	text += "\n"
	return text

#============================================

def build_pgml_text(yaml_data, num_choices, flip, color_mode):
	"""
	Create the PGML file content as a string.
	"""
	replacement_rules = webwork_lib.normalize_replacement_rules(
		yaml_data.get('replacement_rules')
	)

	# Determine default description
	if not flip:
		default_description = (
			f"Select the {yaml_data.get('key description', 'item')} "
			f"that corresponds to the given {yaml_data.get('value description', 'description')}."
		)
	else:
		default_description = (
			f"Select the {yaml_data.get('value description', 'description')} "
			f"that corresponds to the given {yaml_data.get('key description', 'item')}."
		)

	fallback_keywords = [
		yaml_data.get('topic'),
		yaml_data.get('keys description'),
		yaml_data.get('values description'),
		'which one',
		'multiple choice',
	]

	header_text = webwork_lib.build_opl_header(
		yaml_data,
		default_description=default_description,
		fallback_keywords=fallback_keywords,
	)

	questions_data, color_classes, needs_bold_class, warnings = build_perl_question_data(
		yaml_data,
		num_choices,
		flip,
		replacement_rules,
		color_mode,
	)

	preamble_text = build_preamble_text(header_text)
	setup_text = build_setup_text(questions_data)
	statement_text = build_statement_text(color_mode, color_classes, needs_bold_class)
	solution_text = build_solution_text()

	return preamble_text + setup_text + statement_text + solution_text, warnings

#============================================

def main():
	"""
	Script entrypoint.
	"""
	args = parse_args()
	if not os.path.isfile(args.input_yaml_file):
		raise FileNotFoundError(
			f"input yaml file not found: {args.input_yaml_file}"
		)

	yaml_data = bptools.readYamlFile(args.input_yaml_file)
	color_mode = "none" if args.no_color else "inline"
	pgml_text, warnings = build_pgml_text(
		yaml_data,
		args.num_choices,
		args.flip,
		color_mode,
	)

	output_pgml_file = args.output_pgml_file
	if output_pgml_file is None:
		base_name = os.path.splitext(os.path.basename(args.input_yaml_file))[0]
		flip_suffix = "-flipped" if args.flip else ""
		output_pgml_file = f"{base_name}-which_one{flip_suffix}.pgml"

	with open(output_pgml_file, 'w') as outfile:
		outfile.write(pgml_text)
	print(f"Wrote PGML to {output_pgml_file}")
	for warning in warnings:
		print(f"WARNING: {warning}")

#============================================

if __name__ == '__main__':
	main()
