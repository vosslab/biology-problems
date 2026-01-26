#!/usr/bin/env python3

"""
Generate a PGML multiple-choice statements problem from YAML.
"""

# Standard Library
import argparse
import pathlib
import re

# PIP3 modules
import yaml

# local repo modules
import webwork_lib

#============================================
def parse_args():
	"""
	Parse command-line arguments.
	"""
	parser = argparse.ArgumentParser(
		description="Generate a PGML MC statements problem from YAML."
	)
	parser.add_argument(
		'-y', '--yaml', dest='input_yaml_file', required=True,
		help='YAML input file to process'
	)
	parser.add_argument(
		'-o', '--output', dest='output_pg_file',
		help='Output PG file path'
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
	args = parser.parse_args()
	return args

#============================================
def group_statements(block):
	"""
	Groups truth1a, truth1b... into a list of statement groups.
	"""
	grouped = {}
	for key, value in block.items():
		match = re.search(r'(\d+)', key)
		if not match:
			continue
		group_num = int(match.group(1))
		if group_num not in grouped:
			grouped[group_num] = []
		grouped[group_num].append(value)
	grouped_list = []
	for group_num in sorted(grouped.keys()):
		grouped_list.append(grouped[group_num])
	return grouped_list

#============================================
def convert_groups_to_html(groups, replacement_rules, color_mode, color_classes, warnings):
	"""
	Convert grouped statements into HTML-safe strings.
	"""
	converted = []
	needs_bold_class = False
	for group in groups:
		new_group = []
		for statement in group:
			replaced = webwork_lib.apply_replacements_to_text(
				statement,
				replacement_rules,
			)
			html_text, is_bold = webwork_lib.format_label_html(
				replaced,
				color_mode,
				color_classes,
				warnings,
				label_name=statement,
			)
			if is_bold:
				needs_bold_class = True
			new_group.append(html_text)
		converted.append(new_group)
	return converted, needs_bold_class

#============================================
def build_question_text(override_true, override_false):
	"""
	Build the question setup block and PGML question line.
	"""
	has_true_override = override_true is not None
	has_false_override = override_false is not None

	default_true = (
		"Which one of the following statements is "
		"<strong>TRUE</strong> about $topic?"
	)
	default_false = (
		"Which one of the following statements is "
		"<strong>FALSE</strong> about $topic?"
	)

	question_setup_lines = []
	if has_true_override:
		question_setup_lines.append("# Question text with TRUE override")
		escaped_true = webwork_lib.escape_perl_string(override_true)
		question_setup_lines.append(f"$question_true = '{escaped_true}';")

	if has_false_override:
		question_setup_lines.append("# Question text with FALSE override")
		escaped_false = webwork_lib.escape_perl_string(override_false)
		question_setup_lines.append(f"$question_false = '{escaped_false}';")

	true_expr = "$question_true" if has_true_override else f'"{default_true}"'
	false_expr = "$question_false" if has_false_override else f'"{default_false}"'
	pgml_question = f'[@ $mode eq "TRUE" ? {true_expr} : {false_expr} @]*'
	question_setup = "\n".join(question_setup_lines)
	return question_setup, pgml_question

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
	text += '  "PGstandard.pl",\n'
	text += '  "PGML.pl",\n'
	text += '  "PGchoicemacros.pl",\n'
	text += '  "parserRadioButtons.pl",\n'
	text += '  "PGcourse.pl",\n'
	text += ");\n"
	text += "\n"
	text += "TEXT(beginproblem());\n"
	text += "$showPartialCorrectAnswers = 1;\n"
	text += "\n"
	return text

#============================================
def build_setup_text(perl_true, perl_false, topic, question_setup):
	"""
	Build the PGML setup text.
	"""
	text = ""
	text += "#==========================================================\n"
	text += "# AUTO-GENERATED GROUPS FROM YAML\n"
	text += "#==========================================================\n"
	text += "\n"
	text += perl_true.rstrip() + "\n"
	text += perl_false.rstrip() + "\n"
	text += "\n"
	text += "#==========================================================\n"
	text += "# GLOBAL SETTINGS\n"
	text += "#==========================================================\n"
	text += "\n"
	text += f"$topic = '{webwork_lib.escape_perl_string(topic)}';\n"
	text += '$mode  = list_random("TRUE","FALSE");\n'
	text += "$num_distractors = 4;\n"
	if question_setup:
		text += question_setup + "\n"
	text += "#==========================================================\n"
	text += "# SELECT GROUP\n"
	text += "#==========================================================\n"
	text += "\n"
	text += "my (@selected_group, @opposite_groups);\n"
	text += "\n"
	text += 'if ($mode eq "TRUE") {\n'
	text += "  $group_index      = random(0, scalar(@true_groups)-1, 1);\n"
	text += "  @selected_group   = @{ $true_groups[$group_index] };\n"
	text += "  @opposite_groups  = @false_groups;\n"
	text += "} else {\n"
	text += "  $group_index      = random(0, scalar(@false_groups)-1, 1);\n"
	text += "  @selected_group   = @{ $false_groups[$group_index] };\n"
	text += "  @opposite_groups  = @true_groups;\n"
	text += "}\n"
	text += "\n"
	text += "#==========================================================\n"
	text += "# PICK CORRECT + DISTRACTORS\n"
	text += "#==========================================================\n"
	text += "\n"
	text += "$correct = list_random(@selected_group);\n"
	text += "\n"
	text += "my @available_group_indices = (0 .. $#opposite_groups);\n"
	text += "my @selected_distractor_indices = ();\n"
	text += "\n"
	text += (
		"while (@selected_distractor_indices < $num_distractors "
		"&& @available_group_indices > 0) {\n"
	)
	text += "  my $random_index = random(0, scalar(@available_group_indices)-1, 1);\n"
	text += (
		"  push @selected_distractor_indices, "
		"splice(@available_group_indices, $random_index, 1);\n"
	)
	text += "}\n"
	text += "\n"
	text += "@distractors = ();\n"
	text += "foreach my $group_idx (@selected_distractor_indices) {\n"
	text += "  my @group = @{ $opposite_groups[$group_idx] };\n"
	text += "  my $distractor = list_random(@group);\n"
	text += "  push @distractors, $distractor;\n"
	text += "}\n"
	text += "\n"
	text += "@choices = ($correct, @distractors);\n"
	text += "\n"
	text += "#==========================================================\n"
	text += "# RADIO BUTTONS WITH A/B/C/D/E LABELS\n"
	text += "#==========================================================\n"
	text += "\n"
	text += "$rb = RadioButtons(\n"
	text += "  [@choices],\n"
	text += "  $correct,\n"
	text += "  labels        => ['A','B','C','D','E'],\n"
	text += "  displayLabels => 1,\n"
	text += "  randomize     => 1,\n"
	text += "  separator     => '<div style=\"margin-bottom: 0.7em;\"></div>',\n"
	text += ");\n"
	text += "\n"
	return text

#============================================
def build_statement_text(pgml_question, color_mode, color_classes, needs_bold_class):
	"""
	Build the PGML statement text.
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
	text += pgml_question + "\n"
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
	text += "ENDDOCUMENT();\n"
	text += "\n"
	return text

#============================================
def build_pgml_text(yaml_data, color_mode):
	"""
	Create the PGML file content as a string.
	"""
	replacement_rules = webwork_lib.normalize_replacement_rules(
		yaml_data.get("replacement_rules")
	)
	color_classes = {}
	needs_bold_class = False
	warnings = []

	topic_raw = yaml_data.get("topic", "this topic")
	topic_replaced = webwork_lib.apply_replacements_to_text(
		topic_raw,
		replacement_rules,
	)
	topic, topic_bold = webwork_lib.format_label_html(
		topic_replaced,
		color_mode,
		color_classes,
		warnings,
		label_name=topic_raw,
	)
	if topic_bold:
		needs_bold_class = True
	default_description = (
		f"Select the statement that is TRUE or FALSE about {topic_raw}."
	)
	fallback_keywords = [topic_raw, "true/false", "multiple choice"]
	header_text = webwork_lib.build_opl_header(
		yaml_data,
		default_description=default_description,
		fallback_keywords=fallback_keywords,
	)

	override_true_raw = yaml_data.get("override_question_true")
	override_false_raw = yaml_data.get("override_question_false")
	override_true = None
	override_false = None
	if override_true_raw is not None:
		override_true_replaced = webwork_lib.apply_replacements_to_text(
			override_true_raw,
			replacement_rules,
		)
		override_true, is_bold = webwork_lib.format_label_html(
			override_true_replaced,
			color_mode,
			color_classes,
			warnings,
			label_name="override_question_true",
		)
		if is_bold:
			needs_bold_class = True
	if override_false_raw is not None:
		override_false_replaced = webwork_lib.apply_replacements_to_text(
			override_false_raw,
			replacement_rules,
		)
		override_false, is_bold = webwork_lib.format_label_html(
			override_false_replaced,
			color_mode,
			color_classes,
			warnings,
			label_name="override_question_false",
		)
		if is_bold:
			needs_bold_class = True
	question_setup, pgml_question = build_question_text(
		override_true,
		override_false,
	)

	true_block = yaml_data.get("true_statements", {})
	false_block = yaml_data.get("false_statements", {})

	true_groups = group_statements(true_block)
	false_groups = group_statements(false_block)
	true_groups, true_bold = convert_groups_to_html(
		true_groups,
		replacement_rules,
		color_mode,
		color_classes,
		warnings,
	)
	if true_bold:
		needs_bold_class = True
	false_groups, false_bold = convert_groups_to_html(
		false_groups,
		replacement_rules,
		color_mode,
		color_classes,
		warnings,
	)
	if false_bold:
		needs_bold_class = True

	perl_true = webwork_lib.perl_array("true_groups", true_groups)
	perl_false = webwork_lib.perl_array("false_groups", false_groups)

	preamble_text = build_preamble_text(header_text)
	setup_text = build_setup_text(
		perl_true,
		perl_false,
		topic,
		question_setup,
	)
	statement_text = build_statement_text(
		pgml_question,
		color_mode,
		color_classes,
		needs_bold_class,
	)
	solution_text = build_solution_text()
	return preamble_text + setup_text + statement_text + solution_text, warnings

#============================================
def main():
	"""
	Script entrypoint.
	"""
	args = parse_args()
	yml_path = pathlib.Path(args.input_yaml_file)
	if not yml_path.exists():
		raise FileNotFoundError(f"File not found: {yml_path}")
	yaml_data = yaml.safe_load(yml_path.read_text())
	color_mode = "none" if args.no_color else "inline"
	pgml_text, warnings = build_pgml_text(yaml_data, color_mode)

	output_path = args.output_pg_file
	if output_path is None:
		output_path = str(yml_path.with_suffix(".pg"))
	with open(output_path, 'w') as handle:
		handle.write(pgml_text)
	print(f"Generated: {output_path}")
	for warning in warnings:
		print(f"WARNING: {warning}")

#============================================
if __name__ == "__main__":
	main()
