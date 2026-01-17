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
def escape_perl_string(text_string):
	"""
	Escape a string for use in Perl double quotes.
	"""
	if text_string is None:
		return ""
	text_string = text_string.replace('\\', '\\\\')
	text_string = text_string.replace('"', '\\"')
	text_string = text_string.replace('$', '\\$')
	text_string = text_string.replace('@', '\\@')
	return text_string

#============================================
def perl_array(name, groups):
	"""
	Convert Python list-of-lists into Perl array syntax.
	"""
	text = ""
	text += f"@{name} = (\n"
	for group in groups:
		text += "    [\n"
		for statement in group:
			safe = escape_perl_string(statement)
			text += f'      "{safe}",\n'
		text += "    ],\n"
	text += ");\n"
	text += "\n"
	return text

#============================================
def build_question_text(override_true, override_false):
	"""
	Build the question setup block and PGML question line.
	"""
	question_setup_lines = []
	if override_true or override_false:
		if override_true and override_false:
			question_setup_lines.append("# Question text with overrides")
			question_setup_lines.append(
				f'$question_true = "{escape_perl_string(override_true)}";'
			)
			question_setup_lines.append(
				f'$question_false = "{escape_perl_string(override_false)}";'
			)
			pgml_question = (
				'[@ $mode eq "TRUE" ? $question_true : $question_false @]*'
			)
		elif override_true:
			question_setup_lines.append("# Question text with TRUE override")
			question_setup_lines.append(
				f'$question_true = "{escape_perl_string(override_true)}";'
			)
			pgml_question = (
				'[@ $mode eq "TRUE" ? $question_true : '
				'"Which one of the following statements is '
				'<strong>FALSE</strong> about $topic?" @]*'
			)
		else:
			question_setup_lines.append("# Question text with FALSE override")
			question_setup_lines.append(
				f'$question_false = "{escape_perl_string(override_false)}";'
			)
			pgml_question = (
				'[@ $mode eq "TRUE" ? '
				'"Which one of the following statements is '
				'<strong>TRUE</strong> about $topic?" : $question_false @]*'
			)
	else:
		pgml_question = (
			'[@ "Which one of the following statements is '
			'<strong>$mode</strong> about $topic?" @]*'
		)
	question_setup = "\n".join(question_setup_lines)
	return question_setup, pgml_question

#============================================
def build_pgml_text(yaml_data):
	"""
	Create the PGML file content as a string.
	"""
	topic = yaml_data.get("topic", "this topic")
	default_description = (
		f"Select the statement that is TRUE or FALSE about {topic}."
	)
	fallback_keywords = [topic, "true/false", "multiple choice"]
	header_text = webwork_lib.build_opl_header(
		yaml_data,
		default_description=default_description,
		fallback_keywords=fallback_keywords,
	)

	override_true = yaml_data.get("override_question_true")
	override_false = yaml_data.get("override_question_false")
	question_setup, pgml_question = build_question_text(
		override_true,
		override_false,
	)

	true_block = yaml_data.get("true_statements", {})
	false_block = yaml_data.get("false_statements", {})

	true_groups = group_statements(true_block)
	false_groups = group_statements(false_block)

	perl_true = perl_array("true_groups", true_groups)
	perl_false = perl_array("false_groups", false_groups)

	preamble_text = ""
	preamble_text += header_text.rstrip() + "\n"
	preamble_text += "\n"
	preamble_text += "DOCUMENT();\n"
	preamble_text += "\n"
	preamble_text += "loadMacros(\n"
	preamble_text += '  "PGstandard.pl",\n'
	preamble_text += '  "PGML.pl",\n'
	preamble_text += '  "PGchoicemacros.pl",\n'
	preamble_text += '  "parserRadioButtons.pl",\n'
	preamble_text += '  "PGcourse.pl",\n'
	preamble_text += ");\n"
	preamble_text += "\n"
	preamble_text += "TEXT(beginproblem());\n"
	preamble_text += "$showPartialCorrectAnswers = 1;\n"
	preamble_text += "\n"

	setup_text = ""
	setup_text += "#==========================================================\n"
	setup_text += "# AUTO-GENERATED GROUPS FROM YAML\n"
	setup_text += "#==========================================================\n"
	setup_text += "\n"
	setup_text += perl_true.rstrip() + "\n"
	setup_text += perl_false.rstrip() + "\n"
	setup_text += "\n"
	setup_text += "#==========================================================\n"
	setup_text += "# GLOBAL SETTINGS\n"
	setup_text += "#==========================================================\n"
	setup_text += "\n"
	setup_text += f'$topic = "{escape_perl_string(topic)}";\n'
	setup_text += '$mode  = list_random("TRUE","FALSE");\n'
	setup_text += "$num_distractors = 4;\n"
	if question_setup:
		setup_text += question_setup + "\n"
	setup_text += "#==========================================================\n"
	setup_text += "# SELECT GROUP\n"
	setup_text += "#==========================================================\n"
	setup_text += "\n"
	setup_text += "my (@selected_group, @opposite_groups);\n"
	setup_text += "\n"
	setup_text += 'if ($mode eq "TRUE") {\n'
	setup_text += "  $group_index      = random(0, scalar(@true_groups)-1, 1);\n"
	setup_text += "  @selected_group   = @{ $true_groups[$group_index] };\n"
	setup_text += "  @opposite_groups  = @false_groups;\n"
	setup_text += "} else {\n"
	setup_text += "  $group_index      = random(0, scalar(@false_groups)-1, 1);\n"
	setup_text += "  @selected_group   = @{ $false_groups[$group_index] };\n"
	setup_text += "  @opposite_groups  = @true_groups;\n"
	setup_text += "}\n"
	setup_text += "\n"
	setup_text += "#==========================================================\n"
	setup_text += "# PICK CORRECT + DISTRACTORS\n"
	setup_text += "#==========================================================\n"
	setup_text += "\n"
	setup_text += "$correct = list_random(@selected_group);\n"
	setup_text += "\n"
	setup_text += "my @available_group_indices = (0 .. $#opposite_groups);\n"
	setup_text += "my @selected_distractor_indices = ();\n"
	setup_text += "\n"
	setup_text += (
		"while (@selected_distractor_indices < $num_distractors "
		"&& @available_group_indices > 0) {\n"
	)
	setup_text += "  my $random_index = random(0, scalar(@available_group_indices)-1, 1);\n"
	setup_text += (
		"  push @selected_distractor_indices, "
		"splice(@available_group_indices, $random_index, 1);\n"
	)
	setup_text += "}\n"
	setup_text += "\n"
	setup_text += "@distractors = ();\n"
	setup_text += "foreach my $group_idx (@selected_distractor_indices) {\n"
	setup_text += "  my @group = @{ $opposite_groups[$group_idx] };\n"
	setup_text += "  my $distractor = list_random(@group);\n"
	setup_text += "  push @distractors, $distractor;\n"
	setup_text += "}\n"
	setup_text += "\n"
	setup_text += "@choices = ($correct, @distractors);\n"
	setup_text += "\n"
	setup_text += "#==========================================================\n"
	setup_text += "# RADIO BUTTONS WITH A/B/C/D/E LABELS\n"
	setup_text += "#==========================================================\n"
	setup_text += "\n"
	setup_text += "$rb = RadioButtons(\n"
	setup_text += "  [@choices],\n"
	setup_text += "  $correct,\n"
	setup_text += "  labels        => ['A','B','C','D','E'],\n"
	setup_text += "  displayLabels => 1,\n"
	setup_text += "  randomize     => 1,\n"
	setup_text += "  separator     => '<div style=\"margin-bottom: 0.7em;\"></div>',\n"
	setup_text += ");\n"
	setup_text += "\n"

	statement_text = ""
	statement_text += "#==========================================================\n"
	statement_text += "# PGML\n"
	statement_text += "#==========================================================\n"
	statement_text += "\n"
	statement_text += "BEGIN_PGML\n"
	statement_text += "\n"
	statement_text += pgml_question + "\n"
	statement_text += "\n"
	statement_text += "[@ $rb->buttons() @]*\n"
	statement_text += "\n"
	statement_text += "END_PGML\n"
	statement_text += "\n"

	solution_text = ""
	solution_text += "ANS($rb->cmp());\n"
	solution_text += "\n"
	solution_text += "ENDDOCUMENT();\n"
	solution_text += "\n"
	return preamble_text + setup_text + statement_text + solution_text

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
	pgml_text = build_pgml_text(yaml_data)

	output_path = args.output_pg_file
	if output_path is None:
		output_path = str(yml_path.with_suffix(".pg"))
	with open(output_path, 'w') as handle:
		handle.write(pgml_text)
	print(f"Generated: {output_path}")

#============================================
if __name__ == "__main__":
	main()
