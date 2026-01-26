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
import re

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
	parser.add_argument(
		'-m', '--color-mode', dest='color_mode',
		choices=['inline', 'class', 'none'], default='inline',
		help='Replacement rule coloring mode (inline, class, or none).'
	)
	parser.add_argument(
		'--use-colors', dest='use_colors', action='store_true',
		help='Bake MathJax-colored choice labels into the generated PG (legacy).'
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
#============================================
def tex_escape(text_string):
	"""
	Escape a string for use inside TeX \\text{...}.
	"""
	repl = {
		"\\": r"\\",
		"{": r"\{",
		"}": r"\}",
		"#": r"\#",
		"$": r"\$",
		"%": r"\%",
		"&": r"\&",
		"_": r"\_",
		"^": r"\^{}",
		"~": r"\~{}",
	}
	return "".join(repl.get(ch, ch) for ch in text_string)

#============================================
def mj_color_label(label, hex_color):
	"""
	Create a MathJax-colored label string.
	"""
	safe = tex_escape(label)
	return f"[\\color{{{hex_color}}}{{\\text{{{safe}}}}}]"

#============================================
def make_color_palette(num_colors):
	"""
	Select colors from the qti_package_maker color wheel.
	"""
	if num_colors <= 0:
		return []
	color_wheel = bptools.dark_color_wheel
	color_keys = list(color_wheel.keys())
	if len(color_keys) == 0:
		return []
	indices = bptools.get_indices_for_color_wheel(num_colors, len(color_keys))
	return [f"#{color_wheel[color_keys[i]]}" for i in indices]

#============================================

#============================================
def apply_replacements_to_text(text_string, replacement_rules):
	"""
	Apply replacement rules to a single string.
	"""
	text_string = bptools.applyReplacementRulesToText(text_string, replacement_rules)
	return sanitize_replaced_text(text_string)

#============================================
def apply_replacements_to_list(list_of_text_strings, replacement_rules):
	"""
	Apply replacement rules to a list of strings.
	"""
	values_list = bptools.applyReplacementRulesToList(list_of_text_strings, replacement_rules)
	return [sanitize_replaced_text(value) for value in values_list]

#============================================
def sanitize_replaced_text(text_string):
	"""
	Sanitize replacement output into PGML-safe text.
	"""
	text_string = webwork_lib.convert_sub_sup(text_string)
	text_string = webwork_lib.strip_html_tags(text_string, preserve_pgml_wrappers=True)
	text_string = webwork_lib.unescape_html(text_string)
	text_string = webwork_lib.normalize_nbsp(text_string)
	return text_string

#============================================
def prepare_replacement_rules(replacement_rules, color_mode):
	"""
	Prepare replacement rules by converting strict color spans to PGML wrappers.
	"""
	prepared = {}
	color_classes = {}
	needs_bold_class = False
	warnings = []

	for token, value in replacement_rules.items():
		if not isinstance(value, str):
			prepared[token] = value
			continue
		if color_mode == "none":
			prepared[token] = value
			continue
		if webwork_lib.contains_html_table(value):
			warnings.append(f"table content skipped for replacement: {token}")
			prepared[token] = value
			continue
		parsed = webwork_lib.extract_strict_color_span(value)
		if parsed is None:
			if re.search(r'<span[^>]*color', value, flags=re.IGNORECASE):
				warnings.append(f"non-strict color span skipped for replacement: {token}")
			prepared[token] = value
			continue
		prefix, inner_text, suffix, color_value, is_bold = parsed
		if color_mode == "class":
			normalized_color, class_name = webwork_lib.normalize_color_value(color_value)
			class_names = class_name
			if is_bold:
				class_names = f"{class_names} pgml-bold"
				needs_bold_class = True
			wrapper = webwork_lib.build_pgml_tag_wrapper(
				inner_text,
				class_name=class_names,
			)
			color_classes[class_name] = normalized_color
		else:
			normalized_color, _ = webwork_lib.normalize_color_value(color_value)
			style = f"color: {normalized_color};"
			if is_bold:
				style += " font-weight:700;"
			wrapper = webwork_lib.build_pgml_tag_wrapper(
				inner_text,
				style=style,
			)
		prepared[token] = f"{prefix}{wrapper}{suffix}"

	return prepared, color_classes, needs_bold_class, warnings

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
def maybe_color_mapping(match_data, exclude_pairs, use_colors):
	"""
	Optionally colorize choice labels using MathJax \\color{...}.
	"""
	if not use_colors:
		return match_data, exclude_pairs
	labels = sorted(match_data.keys())
	palette = make_color_palette(len(labels))
	if len(palette) == 0:
		return match_data, exclude_pairs
	color_for = {label: palette[i] for i, label in enumerate(labels)}
	label_map = {
		label: mj_color_label(label, color_for[label])
		for label in labels
	}
	colored_match_data = {
		label_map[label]: values
		for label, values in match_data.items()
	}
	colored_exclude_pairs = []
	for left, right in exclude_pairs:
		colored_exclude_pairs.append([
			label_map.get(left, left),
			label_map.get(right, right),
		])
	return colored_match_data, colored_exclude_pairs

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
	text += "    'parserUtils.pl',\n"
	text += "    'PGgraders.pl',\n"
	text += "    'PGcourse.pl'\n"
	text += ");\n"
	text += "our @ALPHABET = ('A' .. 'Z');\n"
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
	text += "# Build question/answer pairs\n"
	text += "# -------------------------------\n"
	text += "# Each entry: [prompt, choice]\n"
	text += "@q_and_a = ();\n"
	text += "foreach my $key (@selected_keys) {\n"
	text += "  my $values_ref = $match_data{$key};\n"
	text += "  my $i = random(0, $#$values_ref, 1);\n"
	text += "  my $value = $values_ref->[$i];\n"
	text += "  push @q_and_a, [ $value, $key ];\n"
	text += "}\n"
	text += "\n"
	text += "# -------------------------------\n"
	text += "# Randomize the questions\n"
	text += "# -------------------------------\n"
	text += "@q_and_a = map { splice(@q_and_a, random(0, $#q_and_a)) } 0 .. $#q_and_a;\n"
	text += "\n"
	text += "# -------------------------------\n"
	text += "# Shuffle the choices\n"
	text += "# -------------------------------\n"
	text += "@answers = ();\n"
	text += "@indices = ();\n"
	text += "@shuffle = ();\n"
	text += "push(@answers, (map { $_->[1] } @q_and_a));\n"
	text += "@indices = (0 .. $#answers);\n"
	text += "@shuffle = map { splice(@indices, random(0, $#indices), 1) } 0 .. $#indices;\n"
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
	text += "@answer_dropdowns =\n"
	text += "  map { DropDown([ @ALPHABET[0 .. $#answers] ], $inversion[$_]) }\n"
	text += "  0 .. $#q_and_a;\n"
	text += "\n"
	return text

#============================================
def build_statement_text(question_text, note_text, use_colors, color_mode, color_classes,
	needs_bold_class):
	"""
	Build the PGML statement text using PGML tag wrappers and empty TeX slots.
	"""
	text = ""
	text += "# -------------------------------\n"
	text += "# Render the question\n"
	text += "# -------------------------------\n"
	text += "HEADER_TEXT(MODES(TeX => '', HTML => <<END_STYLE));\n"
	text += "<style>\n"
	if not use_colors:
		text += ".right-col > div:nth-child(1) { color: #00b3b3; font-weight: 700; }\n"
		text += ".right-col > div:nth-child(2) { color: #b3b300; font-weight: 700; }\n"
		text += ".right-col > div:nth-child(3) { color: #009900; font-weight: 700; }\n"
		text += ".right-col > div:nth-child(4) { color: #e60000; font-weight: 700; }\n"
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
	text += "[@ MODES(TeX => '',\n"
	text += "\tHTML => '<div class=\"two-column\"><div>') @]*\n"
	text += "[@ join(\n"
	text += "    \"\\n\\n\",\n"
	text += "    map {\n"
	text += "        '[_]{$answer_dropdowns[' . $_ . ']} '\n"
	text += "            . '*' . ($_ + 1) . '.* '\n"
	text += "            . '[$q_and_a[' . $_ . '][0]]'\n"
	text += "    } 0 .. $#q_and_a\n"
	text += ") @]**\n"
	text += "[@ MODES(TeX => '',\n"
	text += "\tHTML => '</div><div class=\"right-col\">') @]*\n"
	text += "[@ join(\n"
	text += "    \"\\n\\n\",\n"
	text += "    map {\n"
	text += "        chr(65 + $_) . '. ' . '[$answers[$shuffle[' . $_ . ']]]' \n"
	text += "    } 0 .. $#answers\n"
	text += ") @]**\n"
	text += "[@ MODES(TeX => '', HTML => '</div></div>') @]*\n"
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
	text += "[@ join(', ', map { $ALPHABET[($inversion[($_)])] } 0 .. $#q_and_a) @]*.\n"
	text += "END_PGML_SOLUTION\n"
	text += "\n"
	text += "ENDDOCUMENT();\n"
	text += "\n"
	return text

#============================================
def build_pgml_text(yaml_data, num_choices, use_colors, color_mode):
	"""
	Create the PGML file content as a string.
	"""
	replacement_rules = normalize_replacement_rules(
		yaml_data.get('replacement_rules')
	)
	replacement_rules, color_classes, needs_bold_class, warnings = prepare_replacement_rules(
		replacement_rules,
		color_mode,
	)
	match_data, exclude_pairs = build_match_data(
		yaml_data,
		replacement_rules
	)
	match_data, exclude_pairs = maybe_color_mapping(
		match_data,
		exclude_pairs,
		use_colors,
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
	setup_text = build_setup_text(match_data, exclude_pairs, num_choices)
	statement_text = build_statement_text(
		question_text,
		note_text,
		use_colors,
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
	pgml_text, warnings = build_pgml_text(
		yaml_data,
		args.num_choices,
		args.use_colors,
		args.color_mode,
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
