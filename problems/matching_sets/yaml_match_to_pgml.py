#!/usr/bin/env python3

"""
Generate a PGML matching problem from a matching-set YAML file.

Note: This generator uses legacy PG style with ANS() calls because matching
problems do not have a modern PGML inline answer specification as of January 2026.
See docs/webwork/MATCHING_PROBLEMS_LEGACY_STYLE.md for detailed rationale.
"""

import argparse
import os
import random

import bptools
import webwork_lib

#============================================
def parse_args():
	"""
	Parse command-line arguments.
	"""
	parser = argparse.ArgumentParser(
		description="Generate a PGML matching problem from a YAML matching set."
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
		help='Number of matching pairs to include per question'
	)
	args = parser.parse_args()
	return args

#============================================
#============================================
def normalize_key(raw_key):
	"""
	Normalize keys to a single string.
	"""
	if isinstance(raw_key, list):
		if len(raw_key) == 0:
			raise ValueError("matching pair key list is empty")
		raw_key = random.choice(raw_key)
	if not isinstance(raw_key, str):
		raise TypeError(f"matching pair key is not string: {raw_key}")
	return raw_key

#============================================
def normalize_values(raw_values):
	"""
	Normalize values to a list of strings.
	"""
	if isinstance(raw_values, list):
		values_list = raw_values
	else:
		values_list = [raw_values]
	normalized = []
	for value in values_list:
		if isinstance(value, list):
			raise TypeError(f"matching pair value should be string, got list: {value}")
		if not isinstance(value, str):
			raise TypeError(f"matching pair value is not string: {value}")
		normalized.append(value)
	return normalized

#============================================
def normalize_replacement_rules(replacement_rules):
	"""
	Ensure replacement rules are a dict, so base rules apply without extra prints.
	"""
	if replacement_rules is None:
		return {}
	if not isinstance(replacement_rules, dict):
		raise TypeError("replacement_rules must be a dict when provided")
	return replacement_rules

#============================================
def apply_replacements_to_text(text_string, replacement_rules):
	"""
	Apply replacement rules to a single string.
	"""
	return bptools.applyReplacementRulesToText(text_string, replacement_rules)

#============================================
def apply_replacements_to_list(list_of_text_strings, replacement_rules):
	"""
	Apply replacement rules to a list of strings.
	"""
	return bptools.applyReplacementRulesToList(list_of_text_strings, replacement_rules)

#============================================
def build_match_data(yaml_data, replacement_rules):
	"""
	Build match data and exclude pairs from YAML.
	"""
	if 'matching pairs' not in yaml_data:
		raise KeyError("missing required key: matching pairs")
	raw_pairs = yaml_data['matching pairs']
	if not isinstance(raw_pairs, dict):
		raise TypeError("matching pairs must be a mapping")
	match_data = {}
	for raw_key, raw_values in raw_pairs.items():
		key = normalize_key(raw_key)
		values = normalize_values(raw_values)
		key = apply_replacements_to_text(key, replacement_rules)
		values = apply_replacements_to_list(values, replacement_rules)
		match_data[key] = values

	exclude_pairs = []
	raw_excludes = yaml_data.get('exclude pairs', [])
	if raw_excludes is None:
		raw_excludes = []
	if not isinstance(raw_excludes, list):
		raise TypeError("exclude pairs must be a list")
	for pair in raw_excludes:
		if not isinstance(pair, list) or len(pair) != 2:
			raise ValueError(f"exclude pair must be a 2-item list: {pair}")
		left = normalize_key(pair[0])
		right = normalize_key(pair[1])
		left = apply_replacements_to_text(left, replacement_rules)
		right = apply_replacements_to_text(right, replacement_rules)
		exclude_pairs.append([left, right])
	return match_data, exclude_pairs

#============================================
def build_question_text(yaml_data, replacement_rules):
	"""
	Build question text from YAML fields.
	"""
	question_override = yaml_data.get('question override')
	if question_override is None:
		keys_description = yaml_data.get('keys description')
		values_description = yaml_data.get('values description')
		if keys_description is None or values_description is None:
			raise KeyError("missing keys description or values description")
		question_text = (
			f"Match each of the following {keys_description} "
			f"with their corresponding {values_description}."
		)
	else:
		question_text = question_override
	question_text = apply_replacements_to_text(question_text, replacement_rules)
	note_text = "Note: Each choice will be used exactly once."
	note_text = apply_replacements_to_text(note_text, replacement_rules)
	return question_text, note_text

#============================================
def render_match_data(match_data):
	"""
	Render match data into Perl hash syntax.
	"""
	text = ""
	text += "%match_data = (\n"
	for key, values in match_data.items():
		key_text = webwork_lib.escape_perl_string(key)
		text += f"  '{key_text}' => [\n"
		for value in values:
			value_text = webwork_lib.escape_perl_string(value)
			text += f"    '{value_text}',\n"
		text += "  ],\n"
	text += ");\n"
	return text

#============================================
def render_exclude_pairs(exclude_pairs):
	"""
	Render exclude pairs into Perl array-of-arrays syntax.
	"""
	if len(exclude_pairs) == 0:
		return ""
	text = ""
	text += "@exclude_pairs = (\n"
	for left, right in exclude_pairs:
		left_text = webwork_lib.escape_perl_string(left)
		right_text = webwork_lib.escape_perl_string(right)
		text += f"  ['{left_text}', '{right_text}'],\n"
	text += ");\n"
	return text

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
	text += "    'PGgraders.pl',\n"
	text += "    'unionTables.pl',\n"
	text += "    'PGcourse.pl'\n"
	text += ");\n"
	text += "\n"
	return text

#============================================
def build_setup_text(match_data, exclude_pairs, num_choices):
	"""
	Build the PGML setup text.
	"""
	text = ""
	text += "# ================================\n"
	text += "# Full matching data\n"
	text += "# ================================\n"
	text += render_match_data(match_data)
	text += "\n"
	if len(exclude_pairs) > 0:
		text += "# -------------------------------\n"
		text += "# Exclude pairs\n"
		text += "# -------------------------------\n"
		text += render_exclude_pairs(exclude_pairs)
		text += "\n"
	text += "# -------------------------------\n"
	text += "# Select N random terms\n"
	text += "# -------------------------------\n"
	text += f"my $n = {num_choices};\n"
	text += "@all_terms = keys %match_data;\n"
	text += "\n"
	if len(exclude_pairs) > 0:
		text += "my @selected_terms = ();\n"
		text += "my $max_tries = 500;\n"
		text += "my $tries = 0;\n"
		text += "while (1) {\n"
		text += "  my @indices = NchooseK(scalar(@all_terms), $n);\n"
		text += "  @selected_terms = @all_terms[@indices[0..$n-1]];\n"
		text += "  my $excluded = 0;\n"
		text += "  foreach my $pair (@exclude_pairs) {\n"
		text += "    my ($left, $right) = @$pair;\n"
		text += "    my $has_left = 0;\n"
		text += "    my $has_right = 0;\n"
		text += "    foreach my $term (@selected_terms) {\n"
		text += "      if ($term eq $left) {\n"
		text += "        $has_left = 1;\n"
		text += "      }\n"
		text += "      if ($term eq $right) {\n"
		text += "        $has_right = 1;\n"
		text += "      }\n"
		text += "    }\n"
		text += "    if ($has_left && $has_right) {\n"
		text += "      $excluded = 1;\n"
		text += "      last;\n"
		text += "    }\n"
		text += "  }\n"
		text += "  last if !$excluded;\n"
		text += "  $tries += 1;\n"
		text += "  if ($tries > $max_tries) {\n"
		text += "    die 'Unable to find a non-conflicting set of terms';\n"
		text += "  }\n"
		text += "}\n"
	else:
		text += "my @indices = NchooseK(scalar(@all_terms), $n);\n"
		text += "my @selected_terms = @all_terms[@indices[0..$n-1]];\n"
	text += "\n"
	text += "# -------------------------------\n"
	text += "# Build (Q, A, Q, A, ...) array\n"
	text += "# -------------------------------\n"
	text += "@qa_list = ();\n"
	text += "@indices = ();\n"
	text += "%answer_map = ();\n"
	text += "foreach my $term (@selected_terms) {\n"
	text += "  my $descriptions_ref = $match_data{$term};\n"
	text += "  my $i = random(0, $#$descriptions_ref, 1);\n"
	text += "  my $desc = $descriptions_ref->[$i];\n"
	text += "  push @qa_list, $term, $desc;\n"
	text += "  push @indices, $i;\n"
	text += "  $answer_map{$term} = $desc;\n"
	text += "}\n"
	text += "\n"
	text += "# -------------------------------\n"
	text += "# Create match list\n"
	text += "# -------------------------------\n"
	text += "$ml = new_match_list();\n"
	text += "\n"
	text += "# -------------------------------\n"
	text += "# Override question formatting\n"
	text += "# -------------------------------\n"
	text += "sub custom_pop_up_list_print_q {\n"
	text += "    my $self = shift;\n"
	text += "    my (@questions) = @_;\n"
	text += "    my @list = @{$self->{ra_pop_up_list}};\n"
	text += "    my $out = \"\";\n"
	text += "    if ($main::displayMode =~ /^HTML/) {\n"
	text += "        my $i = 1;\n"
	text += "        foreach my $quest (@questions) {\n"
	text += "            $out .= qq!<div style=\"margin-bottom: 0.75em; white-space: nowrap;\">!\n"
	text += "                  . qq!<strong>$i.</strong>&nbsp;$quest&nbsp;!\n"
	text += "                  . pop_up_list(@list)\n"
	text += "                  . qq!</div>!;\n"
	text += "            $i++;\n"
	text += "        }\n"
	text += "    } else {\n"
	text += "        return pop_up_list_print_q($self, @questions);\n"
	text += "    }\n"
	text += "    return $out;\n"
	text += "}\n"
	text += "\n"
	text += "$ml->rf_print_q(~~&custom_pop_up_list_print_q);\n"
	text += "\n"
	text += "# -------------------------------\n"
	text += "# Override answer formatting\n"
	text += "# -------------------------------\n"
	text += "sub my_print_a {\n"
	text += "  my $self = shift;\n"
	text += "  my(@array) = @_;\n"
	text += "  my @alpha = ('A'..'Z', 'AA'..'ZZ');\n"
	text += "  my $out = \"<BLOCKQUOTE>\";\n"
	text += "  for my $i (0..$#array) {\n"
	text += "    my $letter = $alpha[$i];\n"
	text += "    my $elem = $array[$i];\n"
	text += "    $out .= \"<div style='margin-bottom: 1em;'><b>$letter.</b> $elem</div>\";\n"
	text += "  }\n"
	text += "  $out .= \"</BLOCKQUOTE>\";\n"
	text += "  return $out;\n"
	text += "}\n"
	text += "\n"
	text += "$ml->rf_print_a(~~&my_print_a);\n"
	text += "\n"
	text += "# -------------------------------\n"
	text += "# Dynamically generate popup choices (A to N)\n"
	text += "# -------------------------------\n"
	text += "my @letters = ('A' .. 'Z');\n"
	text += "my @popup_list = ('No answer', '?');\n"
	text += "for my $i (0 .. $n - 1) {\n"
	text += "  push @popup_list, $letters[$i], $letters[$i];\n"
	text += "}\n"
	text += "$ml->ra_pop_up_list([@popup_list]);\n"
	text += "\n"
	text += "# -------------------------------\n"
	text += "# Insert generated Q/A pairs\n"
	text += "# -------------------------------\n"
	text += "$ml->qa(@qa_list);\n"
	text += "$ml->choose($n);\n"
	text += "\n"
	return text

#============================================
def build_statement_text(question_text, note_text):
	"""
	Build the PGML statement text.
	"""
	text = ""
	text += "# -------------------------------\n"
	text += "# Render the question\n"
	text += "# -------------------------------\n"
	text += "BEGIN_PGML\n"
	text += question_text + "\n"
	text += note_text + "\n"
	text += "\n"
	# Legacy pattern: no PGML inline equivalent exists for matching problems
	text += "[@ ColumnMatchTable($ml) @]***\n"
	text += "END_PGML\n"
	text += "\n"
	return text

#============================================
def build_solution_text():
	"""
	Build the PGML solution text.
	"""
	text = ""
	text += "# -------------------------------\n"
	text += "# Dynamic Partial Credit Based on $n\n"
	text += "# -------------------------------\n"
	text += "$showPartialCorrectAnswers = 0;\n"
	text += "my @thresholds;\n"
	text += "my @scores;\n"
	text += "for (my $i = 1; $i <= $n; $i++) {\n"
	text += "  push @thresholds, $i;\n"
	text += "  push @scores, sprintf(\"%.2f\", $i / $n);\n"
	text += "}\n"
	text += "\n"
	text += "install_problem_grader(~~&custom_problem_grader_fluid);\n"
	text += "$ENV{grader_numright} = [@thresholds];\n"
	text += "$ENV{grader_scores}   = [@scores];\n"
	text += "$ENV{grader_message} = 'You can earn partial credit.';\n"
	text += "\n"
	text += "# -------------------------------\n"
	text += "# Grading\n"
	text += "# -------------------------------\n"
	# Legacy ANS() call required: matching problems have no PGML inline spec
	text += "ANS(str_cmp($ml->ra_correct_ans));\n"
	text += "\n"
	text += "@correct      = @{ $ml->ra_correct_ans() };\n"
	text += "$answerstring = join(', ', @correct);\n"
	text += "\n"
	text += "BEGIN_PGML_SOLUTION\n"
	text += "The correct answers are [$answerstring].\n"
	text += "END_PGML_SOLUTION\n"
	text += "\n"
	text += "ENDDOCUMENT();\n"
	text += "\n"
	return text

#============================================
def build_pgml_text(yaml_data, num_choices):
	"""
	Create the PGML file content as a string.
	"""
	replacement_rules = normalize_replacement_rules(
		yaml_data.get('replacement_rules')
	)
	match_data, exclude_pairs = build_match_data(yaml_data, replacement_rules)

	if num_choices is None:
		num_choices = yaml_data.get('items to match per question', 5)
	if not isinstance(num_choices, int):
		raise TypeError("num_choices must be an integer")
	if num_choices < 1:
		raise ValueError("num_choices must be at least 1")
	if num_choices > len(match_data):
		raise ValueError("num_choices cannot exceed number of matching pairs")

	question_text, note_text = build_question_text(yaml_data, replacement_rules)

	default_description = None
	if yaml_data.get('description') is None:
		keys_description = yaml_data.get('keys description', '')
		values_description = yaml_data.get('values description', '')
		default_description = (
			f"Match each of the following {keys_description} "
			f"with their corresponding {values_description}."
		)
	fallback_keywords = [
		yaml_data.get('topic'),
		yaml_data.get('keys description'),
		yaml_data.get('values description'),
	]
	header_text = webwork_lib.build_opl_header(
		yaml_data,
		default_description=default_description,
		fallback_keywords=fallback_keywords,
	)
	preamble_text = build_preamble_text(header_text)
	setup_text = build_setup_text(match_data, exclude_pairs, num_choices)
	statement_text = build_statement_text(question_text, note_text)
	solution_text = build_solution_text()
	return preamble_text + setup_text + statement_text + solution_text

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
	pgml_text = build_pgml_text(yaml_data, args.num_choices)

	output_pgml_file = args.output_pgml_file
	if output_pgml_file is None:
		base_name = os.path.splitext(os.path.basename(args.input_yaml_file))[0]
		output_pgml_file = f"matching-{base_name}.pgml"

	with open(output_pgml_file, 'w') as outfile:
		outfile.write(pgml_text)
	print(f"Wrote PGML to {output_pgml_file}")

#============================================
if __name__ == '__main__':
	main()
