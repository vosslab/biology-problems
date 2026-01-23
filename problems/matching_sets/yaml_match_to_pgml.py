#!/usr/bin/env python3

"""
Generate a PGML matching problem from a matching-set YAML file.

Uses modern PGML style with parserPopUp.pl and inline answer specifications.
Based on MatchingAlt.pg from WeBWorK PG tutorial (2023-05-23).
See docs/webwork/MATCHING_PROBLEMS.md for approach documentation.
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
	text += "    'parserPopUp.pl',\n"
	text += "    'PGgraders.pl',\n"
	text += "    'PGcourse.pl'\n"
	text += ");\n"
	text += "\n"
	return text

#============================================
def build_setup_text(match_data, exclude_pairs, num_choices):
	"""
	Build the PGML setup text using modern DropDown approach.
	Keys (short terms) go in dropdowns, values (long descriptions) are prompts.
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
	text += "# Select N random keys\n"
	text += "# -------------------------------\n"
	text += f"my $n = {num_choices};\n"
	text += "@all_keys = keys %match_data;\n"
	text += "\n"
	if len(exclude_pairs) > 0:
		text += "my @selected_keys = ();\n"
		text += "my $max_tries = 500;\n"
		text += "my $tries = 0;\n"
		text += "while (1) {\n"
		text += "  my @indices = NchooseK(scalar(@all_keys), $n);\n"
		text += "  @selected_keys = @all_keys[@indices[0..$n-1]];\n"
		text += "  my $excluded = 0;\n"
		text += "  foreach my $pair (@exclude_pairs) {\n"
		text += "    my ($left, $right) = @$pair;\n"
		text += "    my $has_left = 0;\n"
		text += "    my $has_right = 0;\n"
		text += "    foreach my $key (@selected_keys) {\n"
		text += "      if ($key eq $left) {\n"
		text += "        $has_left = 1;\n"
		text += "      }\n"
		text += "      if ($key eq $right) {\n"
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
		text += "    die 'Unable to find a non-conflicting set of keys';\n"
		text += "  }\n"
		text += "}\n"
	else:
		text += "my @indices = NchooseK(scalar(@all_keys), $n);\n"
		text += "my @selected_keys = @all_keys[@indices[0..$n-1]];\n"
	text += "\n"
	text += "# -------------------------------\n"
	text += "# Build question-answer pairs\n"
	text += "# -------------------------------\n"
	text += "# Keys (short terms) = dropdown choices (A, B, C...)\n"
	text += "# Values (long descriptions) = numbered prompts (1, 2, 3...)\n"
	text += "@prompts = ();  # Will be the numbered questions (from values)\n"
	text += "@choices = @selected_keys;  # Will be lettered dropdown options (A, B, C...)\n"
	text += "%correct_choice = ();  # Maps prompt index to choice index\n"
	text += "\n"
	text += "foreach my $key (@selected_keys) {\n"
	text += "  my $values_ref = $match_data{$key};\n"
	text += "  my $i = random(0, $#$values_ref, 1);\n"
	text += "  my $value = $values_ref->[$i];\n"
	text += "  push @prompts, $value;\n"
	text += "}\n"
	text += "\n"
	text += "# -------------------------------\n"
	text += "# Shuffle the choices (A, B, C...)\n"
	text += "# -------------------------------\n"
	text += "@choice_indices = (0 .. $#choices);\n"
	text += "@shuffle = ();\n"
	text += "foreach (0 .. $#choice_indices) {\n"
	text += "  push @shuffle, splice(@choice_indices, random(0, $#choice_indices), 1);\n"
	text += "}\n"
	text += "\n"
	text += "# -------------------------------\n"
	text += "# Create inverse mapping\n"
	text += "# -------------------------------\n"
	text += "my @inversion;\n"
	text += "@inversion[@shuffle] = (0 .. $#shuffle);\n"
	text += "\n"
	text += "# -------------------------------\n"
	text += "# Create DropDown objects\n"
	text += "# -------------------------------\n"
	text += "my @letters = ('A' .. 'Z');\n"
	text += "@answer_dropdowns = ();\n"
	text += "foreach my $i (0 .. $#prompts) {\n"
	text += "  my $correct_index = $inversion[$i];\n"
	text += "  push @answer_dropdowns, DropDown([ @letters[0 .. $#choices] ], $correct_index);\n"
	text += "}\n"
	text += "\n"
	return text

#============================================
def build_statement_text(question_text, note_text):
	"""
	Build the PGML statement text using modern inline answer specs.
	"""
	text = ""
	text += "# -------------------------------\n"
	text += "# Render the question\n"
	text += "# -------------------------------\n"
	text += "BEGIN_PGML\n"
	text += question_text + "\n"
	text += note_text + "\n"
	text += "\n"
	text += "## Prompts\n"
	text += "\n"
	text += "[@ join(\"\\n\\n\", map { \"[_]{$answer_dropdowns[\" . $_ . \"]} *\" . ($_ + 1) . \".* [$prompts[\" . $_ . \"]]\" } 0 .. $#prompts) @]**\n"
	text += "\n"
	text += "## Choices\n"
	text += "\n"
	text += "[@ join(\"\\n\\n\", map { \"*\" . $letters[($_)] . \".* [$choices[$shuffle[\" . $_ . \"]]]\" } 0 .. $#choices) @]**\n"
	text += "END_PGML\n"
	text += "\n"
	return text

#============================================
def build_solution_text():
	"""
	Build the PGML solution text (modern PGML - no ANS() calls needed).
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
	text += "# Solution\n"
	text += "# -------------------------------\n"
	text += "# Show the correct answer letters\n"
	text += "$answerstring = join(', ', map { $letters[($inversion[$_])] } 0 .. $#prompts);\n"
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
		output_pgml_file = f"{base_name}-matching.pgml"

	with open(output_pgml_file, 'w') as outfile:
		outfile.write(pgml_text)
	print(f"Wrote PGML to {output_pgml_file}")

#============================================
if __name__ == '__main__':
	main()
