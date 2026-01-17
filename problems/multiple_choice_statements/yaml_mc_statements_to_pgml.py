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
	lines = []
	lines.append(f"@{name} = (")
	for group in groups:
		lines.append("    [")
		for statement in group:
			safe = escape_perl_string(statement)
			lines.append(f'      "{safe}",')
		lines.append("    ],")
	lines.append(");")
	lines.append("")
	perl_text = "\n".join(lines)
	return perl_text

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

	lines = []
	lines.append(header_text.rstrip())
	lines.append("")
	lines.append("DOCUMENT();")
	lines.append("")
	lines.append("loadMacros(")
	lines.append('  "PGstandard.pl",')
	lines.append('  "PGML.pl",')
	lines.append('  "PGchoicemacros.pl",')
	lines.append('  "parserRadioButtons.pl",')
	lines.append('  "PGcourse.pl",')
	lines.append(");")
	lines.append("")
	lines.append("TEXT(beginproblem());")
	lines.append("$showPartialCorrectAnswers = 1;")
	lines.append("")
	lines.append("#==========================================================")
	lines.append("# AUTO-GENERATED GROUPS FROM YAML")
	lines.append("#==========================================================")
	lines.append("")
	lines.append(perl_true.rstrip())
	lines.append(perl_false.rstrip())
	lines.append("")
	lines.append("#==========================================================")
	lines.append("# GLOBAL SETTINGS")
	lines.append("#==========================================================")
	lines.append("")
	lines.append(f'$topic = "{escape_perl_string(topic)}";')
	lines.append('$mode  = list_random("TRUE","FALSE");')
	lines.append("$num_distractors = 4;")
	if question_setup:
		lines.append(question_setup)
	lines.append("#==========================================================")
	lines.append("# SELECT GROUP")
	lines.append("#==========================================================")
	lines.append("")
	lines.append("my (@selected_group, @opposite_groups);")
	lines.append("")
	lines.append('if ($mode eq "TRUE") {')
	lines.append("  $group_index      = random(0, scalar(@true_groups)-1, 1);")
	lines.append("  @selected_group   = @{ $true_groups[$group_index] };")
	lines.append("  @opposite_groups  = @false_groups;")
	lines.append("} else {")
	lines.append("  $group_index      = random(0, scalar(@false_groups)-1, 1);")
	lines.append("  @selected_group   = @{ $false_groups[$group_index] };")
	lines.append("  @opposite_groups  = @true_groups;")
	lines.append("}")
	lines.append("")
	lines.append("#==========================================================")
	lines.append("# PICK CORRECT + DISTRACTORS")
	lines.append("#==========================================================")
	lines.append("")
	lines.append("$correct = list_random(@selected_group);")
	lines.append("")
	lines.append("my @available_group_indices = (0 .. $#opposite_groups);")
	lines.append("my @selected_distractor_indices = ();")
	lines.append("")
	lines.append(
		"while (@selected_distractor_indices < $num_distractors "
		"&& @available_group_indices > 0) {"
	)
	lines.append("  my $random_index = random(0, scalar(@available_group_indices)-1, 1);")
	lines.append(
		"  push @selected_distractor_indices, "
		"splice(@available_group_indices, $random_index, 1);"
	)
	lines.append("}")
	lines.append("")
	lines.append("@distractors = ();")
	lines.append("foreach my $group_idx (@selected_distractor_indices) {")
	lines.append("  my @group = @{ $opposite_groups[$group_idx] };")
	lines.append("  my $distractor = list_random(@group);")
	lines.append("  push @distractors, $distractor;")
	lines.append("}")
	lines.append("")
	lines.append("@choices = ($correct, @distractors);")
	lines.append("")
	lines.append("#==========================================================")
	lines.append("# RADIO BUTTONS WITH A/B/C/D/E LABELS")
	lines.append("#==========================================================")
	lines.append("")
	lines.append("$rb = RadioButtons(")
	lines.append("  [@choices],")
	lines.append("  $correct,")
	lines.append("  labels        => ['A','B','C','D','E'],")
	lines.append("  displayLabels => 1,")
	lines.append("  randomize     => 1,")
	lines.append("  separator     => '<div style=\"margin-bottom: 0.7em;\"></div>',")
	lines.append(");")
	lines.append("")
	lines.append("#==========================================================")
	lines.append("# PGML")
	lines.append("#==========================================================")
	lines.append("")
	lines.append("BEGIN_PGML")
	lines.append("")
	lines.append(pgml_question)
	lines.append("")
	lines.append("[@ $rb->buttons() @]*")
	lines.append("")
	lines.append("END_PGML")
	lines.append("")
	lines.append("ANS($rb->cmp());")
	lines.append("")
	lines.append("ENDDOCUMENT();")
	lines.append("")
	return "\n".join(lines)

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
