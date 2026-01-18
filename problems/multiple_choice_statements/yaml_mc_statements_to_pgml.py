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
def build_statement_text(pgml_question):
	"""
	Build the PGML statement text.
	"""
	text = ""
	text += "#==========================================================\n"
	text += "# PGML\n"
	text += "#==========================================================\n"
	text += "\n"
	text += "BEGIN_PGML\n"
	text += "\n"
	text += pgml_question + "\n"
	text += "\n"
	text += "[@ $rb->buttons() @]*\n"
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
	text += "ANS($rb->cmp());\n"
	text += "\n"
	text += "ENDDOCUMENT();\n"
	text += "\n"
	return text

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

	perl_true = webwork_lib.perl_array("true_groups", true_groups)
	perl_false = webwork_lib.perl_array("false_groups", false_groups)

	preamble_text = build_preamble_text(header_text)
	setup_text = build_setup_text(
		perl_true,
		perl_false,
		topic,
		question_setup,
	)
	statement_text = build_statement_text(pgml_question)
	solution_text = build_solution_text()
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
