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
def build_match_data(yaml_data, replacement_rules, color_mode):
	"""
	Build match data and exclude pairs from YAML.
	"""
	if 'matching pairs' not in yaml_data:
		raise KeyError("missing required key: matching pairs")
	raw_pairs = yaml_data['matching pairs']
	if not isinstance(raw_pairs, dict):
		raise TypeError("matching pairs must be a mapping")
	match_data = {}
	answer_html_map = {}
	color_classes = {}
	needs_bold_class = False
	warnings = []
	for raw_key, raw_values in raw_pairs.items():
		key_raw = normalize_key(raw_key)
		values_raw = normalize_values(raw_values)
		key_replaced = webwork_lib.apply_replacements_to_text(
			key_raw,
			replacement_rules,
		)
		key_plain = webwork_lib.sanitize_replaced_text(key_replaced)
		key_html, is_bold = webwork_lib.format_label_html(
			key_replaced,
			color_mode,
			color_classes,
			warnings,
			label_name=key_raw,
		)
		if is_bold:
			needs_bold_class = True
		values = [
			webwork_lib.sanitize_replaced_text(value)
			for value in webwork_lib.apply_replacements_to_list(
				values_raw,
				replacement_rules,
			)
		]
		match_data[key_plain] = values
		answer_html_map[key_plain] = key_html

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
		left = webwork_lib.sanitize_replaced_text(
			webwork_lib.apply_replacements_to_text(left, replacement_rules)
		)
		right = webwork_lib.sanitize_replaced_text(
			webwork_lib.apply_replacements_to_text(right, replacement_rules)
		)
		exclude_pairs.append([left, right])
	return match_data, exclude_pairs, answer_html_map, color_classes, needs_bold_class, warnings

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
	question_text = webwork_lib.sanitize_replaced_text(
		webwork_lib.apply_replacements_to_text(question_text, replacement_rules)
	)
	note_text = "Note: Each choice will be used exactly once."
	note_text = webwork_lib.sanitize_replaced_text(
		webwork_lib.apply_replacements_to_text(note_text, replacement_rules)
	)
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
	text += "    'parserUtils.pl',\n"
	text += "    'PGgraders.pl',\n"
	text += "    'PGcourse.pl'\n"
	text += ");\n"
	text += "our @ALPHABET = ('A' .. 'Z');\n"
	text += "\n"
	return text

#============================================
def build_setup_text(match_data, exclude_pairs, num_choices, answer_html_map):
	"""
	Build the PGML setup text using modern PopUp approach.
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
	text += "@all_keys = PGsort(sub { $_[0] lt $_[1] }, keys %match_data);\n"
	text += "my $local_seed = (defined($problemSeed) && $problemSeed ne '') ? $problemSeed : 1;\n"
	text += "my $local_random = new PGrandom($local_seed);\n"
	text += "\n"
	if len(exclude_pairs) > 0:
		text += "my @selected_keys = ();\n"
		text += "my $max_tries = 500;\n"
		text += "my $tries = 0;\n"
		text += "while (1) {\n"
		text += "  my @indices = (0 .. $#all_keys);\n"
		text += "  my @shuffled = ();\n"
		text += "  while (@indices) {\n"
		text += "    my $pick = $local_random->random(0, $#indices, 1);\n"
		text += "    push @shuffled, splice(@indices, $pick, 1);\n"
		text += "  }\n"
		text += "  @selected_keys = @all_keys[@shuffled[0..$n-1]];\n"
		text += "  my %selected = map { $_ => 1 } @selected_keys;\n"
		text += "  my $excluded = 0;\n"
		text += "  foreach my $pair (@exclude_pairs) {\n"
		text += "    my ($left, $right) = @$pair;\n"
		text += "    if ($selected{$left} && $selected{$right}) {\n"
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
		text += "my @indices = (0 .. $#all_keys);\n"
		text += "my @shuffled = ();\n"
		text += "while (@indices) {\n"
		text += "  my $pick = $local_random->random(0, $#indices, 1);\n"
		text += "  push @shuffled, splice(@indices, $pick, 1);\n"
		text += "}\n"
		text += "my @selected_keys = @all_keys[@shuffled[0..$n-1]];\n"
	text += "\n"
	text += "# -------------------------------\n"
	text += "# Build question/answer pairs\n"
	text += "# -------------------------------\n"
	text += "# Each entry: [prompt, choice]\n"
	text += "@q_and_a = ();\n"
	text += "foreach my $key (@selected_keys) {\n"
	text += "  my $values_ref = $match_data{$key};\n"
	text += "  my $i = $local_random->random(0, $#$values_ref, 1);\n"
	text += "  my $value = $values_ref->[$i];\n"
	text += "  push @q_and_a, [ $value, $key ];\n"
	text += "}\n"
	text += "\n"
	text += "# -------------------------------\n"
	text += "# Randomize the questions\n"
	text += "# -------------------------------\n"
	text += "my @q_indices = (0 .. $#q_and_a);\n"
	text += "my @q_shuffled = ();\n"
	text += "while (@q_indices) {\n"
	text += "  my $pick = $local_random->random(0, $#q_indices, 1);\n"
	text += "  push @q_shuffled, $q_and_a[splice(@q_indices, $pick, 1)];\n"
	text += "}\n"
	text += "@q_and_a = @q_shuffled;\n"
	text += "\n"
	text += "# -------------------------------\n"
	text += "# Sort the choices alphabetically\n"
	text += "# -------------------------------\n"
	text += "@answers = ();\n"
	text += "push(@answers, (map { $_->[1] } @q_and_a));\n"
	text += "@answers_sorted = PGsort(sub { $_[0] lt $_[1] }, @answers);\n"
	text += "\n"
	if answer_html_map:
		text += "# -------------------------------\n"
		text += "# HTML-safe answer labels\n"
		text += "# -------------------------------\n"
		text += webwork_lib.perl_hash("answer_html", answer_html_map)
		text += "@answers_sorted_html = map { $answer_html{$_} || $_ } @answers_sorted;\n"
		text += "\n"
	text += "# -------------------------------\n"
	text += "# Create answer index lookup\n"
	text += "# -------------------------------\n"
	text += "my %answer_index;\n"
	text += "for (my $i = 0; $i <= $#answers_sorted; $i++) {\n"
	text += "  $answer_index{$answers_sorted[$i]} = $i;\n"
	text += "}\n"
	text += "\n"
	text += "# -------------------------------\n"
	text += "# PopUp/DropDown compatibility\n"
	text += "# -------------------------------\n"
	text += "sub make_popup {\n"
	text += "  return defined &DropDown ? DropDown(@_) : PopUp(@_);\n"
	text += "}\n"
	text += "\n"
	text += "# -------------------------------\n"
	text += "# Create popup objects (blank default)\n"
	text += "# -------------------------------\n"
	text += "my @answer_letters = @ALPHABET[0 .. $#answers_sorted];\n"
	text += "my @answer_letters_with_blank = ('', @answer_letters);\n"
	text += "@answer_dropdowns =\n"
	text += "  map { make_popup([ @answer_letters_with_blank ], $answer_index{$q_and_a[$_][1]} + 1 ) }\n"
	text += "  0 .. $#q_and_a;\n"
	text += "\n"
	return text

#============================================
def build_statement_text(question_text, note_text, use_answer_html, color_mode,
	color_classes, needs_bold_class):
	"""
	Build the PGML statement text using PGML tag wrappers and empty TeX slots.
	"""
	text = ""
	text += "# -------------------------------\n"
	text += "# Render the question\n"
	text += "# -------------------------------\n"
	text += "HEADER_TEXT(MODES(TeX => '', HTML => <<END_STYLE));\n"
	text += "<style>\n"
	if color_mode == "class" and len(color_classes) > 0:
		for class_name in sorted(color_classes.keys()):
			color_value = color_classes[class_name]
			text += f".{class_name} {{ color: {color_value}; }}\n"
		if needs_bold_class:
			text += ".pgml-bold { font-weight: 700; }\n"
	text += ".two-column {\n"
	text += "    display: flex;\n"
	text += "\tflex-wrap: wrap;\n"
	text += "\tgap: 2rem;\n"
	text += "\talign-items: center;\n"
	text += "\tjustify-content: space-evenly;\n"
	text += "}\n"
	text += "</style>\n"
	text += "END_STYLE\n"
	text += "\n"
	text += "BEGIN_PGML\n"
	text += question_text + "\n"
	text += note_text + "\n"
	text += "\n"
	text += "[<\n"
	text += "  [<\n"
	text += "    [@ join(\n"
	text += "        \"\\n\\n\",\n"
	text += "        map {\n"
	text += "            '[_]{$answer_dropdowns[' . $_ . ']} '\n"
	text += "                . '*' . ($_ + 1) . '.* '\n"
	text += "                . '[$q_and_a[' . $_ . '][0]]'\n"
	text += "        } 0 .. $#q_and_a\n"
	text += "    ) @]**\n"
	text += "  >]{ [ 'div' ] }{ [ '\\\\parbox{0.55\\\\linewidth}{', '}' ] }\n"
	text += "  [<\n"
	text += "    [@ join(\n"
	text += "        \"\\n\\n\",\n"
	text += "        map {\n"
	text += "            chr(65 + $_) . '\\\\.' . ' ' . "
	if use_answer_html:
		text += "'[$answers_sorted_html[' . $_ . ']]*'\n"
	else:
		text += "'[$answers_sorted[' . $_ . ']]'\n"
	text += "        } 0 .. $#answers_sorted\n"
	text += "    ) @]**\n"
	text += "  >]{ [ 'div' ] }{ [ '\\\\parbox{0.25\\\\linewidth}{', '}' ] }\n"
	text += "]{ [ 'div', class => 'two-column' ] }\n"
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
	text += "BEGIN_PGML_SOLUTION\n"
	text += "The correct answers are\n"
	text += "[@ join(', ', map { $ALPHABET[$answer_index{$q_and_a[$_][1]}] } 0 .. $#q_and_a) @]*.\n"
	text += "END_PGML_SOLUTION\n"
	text += "\n"
	text += "ENDDOCUMENT();\n"
	text += "\n"
	return text

#============================================
def build_pgml_text(yaml_data, num_choices, color_mode):
	"""
	Create the PGML file content as a string.
	"""
	replacement_rules = webwork_lib.normalize_replacement_rules(
		yaml_data.get('replacement_rules')
	)
	match_data, exclude_pairs, answer_html_map, color_classes, needs_bold_class, warnings = (
		build_match_data(
			yaml_data,
			replacement_rules,
			color_mode,
		)
	)
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
	use_answer_html = (color_mode != "none") and bool(answer_html_map)
	setup_text = build_setup_text(match_data, exclude_pairs, num_choices, answer_html_map)
	statement_text = build_statement_text(
		question_text,
		note_text,
		use_answer_html,
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
	if not os.path.isfile(args.input_yaml_file):
		raise FileNotFoundError(
			f"input yaml file not found: {args.input_yaml_file}"
		)
	yaml_data = bptools.readYamlFile(args.input_yaml_file)
	color_mode = "none" if args.no_color else "inline"
	pgml_text, warnings = build_pgml_text(
		yaml_data,
		args.num_choices,
		color_mode,
	)

	output_pgml_file = args.output_pgml_file
	if output_pgml_file is None:
		base_name = os.path.splitext(os.path.basename(args.input_yaml_file))[0]
		output_pgml_file = f"{base_name}-matching.pgml"

	with open(output_pgml_file, 'w') as outfile:
		outfile.write(pgml_text)
	print(f"Wrote PGML to {output_pgml_file}")
	for warning in warnings:
		print(f"WARNING: {warning}")

#============================================
if __name__ == '__main__':
	main()
