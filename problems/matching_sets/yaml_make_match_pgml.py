#!/usr/bin/env python3

"""
Generate a PGML matching problem from a matching-set YAML file.
"""

import argparse
import os
import random
import re

import bptools

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
def escape_perl_single_quoted(text_string):
	"""
	Escape text for a Perl single-quoted string.
	"""
	if not isinstance(text_string, str):
		raise TypeError(f"value is not string: {text_string}")
	text_string = text_string.replace("\\", "\\\\")
	text_string = text_string.replace("'", "\\'")
	text_string = text_string.replace("\r", " ")
	text_string = text_string.replace("\n", " ")
	return text_string

#============================================
def sanitize_header_text(text_string):
	"""
	Sanitize header text to plain ASCII without HTML tags.
	"""
	if not isinstance(text_string, str):
		raise TypeError(f"value is not string: {text_string}")
	text_string = re.sub(r'<[^>]+>', '', text_string)
	text_string = text_string.replace("\r", " ")
	text_string = text_string.replace("\n", " ")
	text_string = " ".join(text_string.split())
	text_string = text_string.encode("ascii", "ignore").decode("ascii")
	return text_string

#============================================
def normalize_keywords(raw_keywords):
	"""
	Normalize keywords to a list of strings.
	"""
	if raw_keywords is None:
		return []
	if isinstance(raw_keywords, list):
		keywords = raw_keywords
	elif isinstance(raw_keywords, str):
		if "," in raw_keywords:
			keywords = [item.strip() for item in raw_keywords.split(",")]
		else:
			keywords = [raw_keywords.strip()]
	else:
		raise TypeError("keywords must be a list or string")
	normalized = []
	for keyword in keywords:
		if not keyword:
			continue
		if not isinstance(keyword, str):
			raise TypeError(f"keyword is not string: {keyword}")
		normalized.append(keyword)
	return normalized

#============================================
def build_header_lines(yaml_data):
	"""
	Build a complete OPL-style header block.
	"""
	description_text = yaml_data.get('description')
	if description_text is None:
		keys_description = yaml_data.get('keys description', '')
		values_description = yaml_data.get('values description', '')
		description_text = (
			f"Match each of the following {keys_description} "
			f"with their corresponding {values_description}."
		)
	description_text = sanitize_header_text(description_text)

	keywords = normalize_keywords(yaml_data.get('keywords'))
	if len(keywords) == 0:
		for candidate in [
			yaml_data.get('topic'),
			yaml_data.get('keys description'),
			yaml_data.get('values description'),
		]:
			if candidate:
				keywords.append(candidate)
	keywords = [sanitize_header_text(keyword) for keyword in keywords if keyword]

	dbsubject = sanitize_header_text(str(yaml_data.get('dbsubject', '')))
	dbchapter = sanitize_header_text(str(yaml_data.get('dbchapter', '')))
	dbsection = sanitize_header_text(str(yaml_data.get('dbsection', '')))
	date_text = sanitize_header_text(str(yaml_data.get('date', '')))
	author_text = sanitize_header_text(str(yaml_data.get('author', '')))
	institution_text = sanitize_header_text(str(yaml_data.get('institution', '')))
	title_text = sanitize_header_text(str(yaml_data.get('titletext1', '')))
	edition_text = sanitize_header_text(str(yaml_data.get('editiontext1', '')))
	author_text_1 = sanitize_header_text(str(yaml_data.get('authortext1', '')))
	section_text = sanitize_header_text(str(yaml_data.get('section1', '')))
	problem_text = sanitize_header_text(str(yaml_data.get('problem1', '')))

	header_lines = []
	header_lines.append("## DESCRIPTION")
	header_lines.append(f"## {description_text}")
	header_lines.append("## ENDDESCRIPTION")
	if len(keywords) == 0:
		header_lines.append("## KEYWORDS('')")
	else:
		escaped_keywords = []
		for keyword in keywords:
			escaped_keywords.append(escape_perl_single_quoted(keyword))
		keyword_blob = "','".join(escaped_keywords)
		header_lines.append(f"## KEYWORDS('{keyword_blob}')")
	header_lines.append(f"## DBsubject('{escape_perl_single_quoted(dbsubject)}')")
	header_lines.append(f"## DBchapter('{escape_perl_single_quoted(dbchapter)}')")
	header_lines.append(f"## DBsection('{escape_perl_single_quoted(dbsection)}')")
	header_lines.append(f"## Date('{escape_perl_single_quoted(date_text)}')")
	header_lines.append(f"## Author('{escape_perl_single_quoted(author_text)}')")
	header_lines.append(f"## Institution('{escape_perl_single_quoted(institution_text)}')")
	header_lines.append(f"## TitleText1('{escape_perl_single_quoted(title_text)}')")
	header_lines.append(f"## EditionText1('{escape_perl_single_quoted(edition_text)}')")
	header_lines.append(f"## AuthorText1('{escape_perl_single_quoted(author_text_1)}')")
	header_lines.append(f"## Section1('{escape_perl_single_quoted(section_text)}')")
	header_lines.append(f"## Problem1('{escape_perl_single_quoted(problem_text)}')")
	return header_lines

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
	lines = []
	lines.append("%match_data = (")
	for key, values in match_data.items():
		key_text = escape_perl_single_quoted(key)
		lines.append(f"  '{key_text}' => [")
		for value in values:
			value_text = escape_perl_single_quoted(value)
			lines.append(f"    '{value_text}',")
		lines.append("  ],")
	lines.append(");")
	return lines

#============================================
def render_exclude_pairs(exclude_pairs):
	"""
	Render exclude pairs into Perl array-of-arrays syntax.
	"""
	lines = []
	if len(exclude_pairs) == 0:
		return lines
	lines.append("@exclude_pairs = (")
	for left, right in exclude_pairs:
		left_text = escape_perl_single_quoted(left)
		right_text = escape_perl_single_quoted(right)
		lines.append(f"  ['{left_text}', '{right_text}'],")
	lines.append(");")
	return lines

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

	lines = []
	lines.extend(build_header_lines(yaml_data))
	lines.append("")
	lines.append("DOCUMENT();")
	lines.append("")
	lines.append("loadMacros(")
	lines.append("    'PGstandard.pl',")
	lines.append("    'PGML.pl',")
	lines.append("    'PGchoicemacros.pl',")
	lines.append("    'PGgraders.pl',")
	lines.append("    'unionTables.pl',")
	lines.append("    'PGcourse.pl'")
	lines.append(");")
	lines.append("")
	lines.append("# ================================")
	lines.append("# Full matching data")
	lines.append("# ================================")
	lines.extend(render_match_data(match_data))
	lines.append("")
	if len(exclude_pairs) > 0:
		lines.append("# -------------------------------")
		lines.append("# Exclude pairs")
		lines.append("# -------------------------------")
		lines.extend(render_exclude_pairs(exclude_pairs))
		lines.append("")
	lines.append("# -------------------------------")
	lines.append("# Select N random terms")
	lines.append("# -------------------------------")
	lines.append(f"my $n = {num_choices};")
	lines.append("@all_terms = keys %match_data;")
	lines.append("")
	if len(exclude_pairs) > 0:
		lines.append("my @selected_terms = ();")
		lines.append("my $max_tries = 500;")
		lines.append("my $tries = 0;")
		lines.append("while (1) {")
		lines.append("  my @indices = NchooseK(scalar(@all_terms), $n);")
		lines.append("  @selected_terms = @all_terms[@indices[0..$n-1]];")
		lines.append("  my $excluded = 0;")
		lines.append("  foreach my $pair (@exclude_pairs) {")
		lines.append("    my ($left, $right) = @$pair;")
		lines.append("    my $has_left = 0;")
		lines.append("    my $has_right = 0;")
		lines.append("    foreach my $term (@selected_terms) {")
		lines.append("      if ($term eq $left) {")
		lines.append("        $has_left = 1;")
		lines.append("      }")
		lines.append("      if ($term eq $right) {")
		lines.append("        $has_right = 1;")
		lines.append("      }")
		lines.append("    }")
		lines.append("    if ($has_left && $has_right) {")
		lines.append("      $excluded = 1;")
		lines.append("      last;")
		lines.append("    }")
		lines.append("  }")
		lines.append("  last if !$excluded;")
		lines.append("  $tries += 1;")
		lines.append("  if ($tries > $max_tries) {")
		lines.append("    die 'Unable to find a non-conflicting set of terms';")
		lines.append("  }")
		lines.append("}")
	else:
		lines.append("my @indices = NchooseK(scalar(@all_terms), $n);")
		lines.append("my @selected_terms = @all_terms[@indices[0..$n-1]];")
	lines.append("")
	lines.append("# -------------------------------")
	lines.append("# Build (Q, A, Q, A, ...) array")
	lines.append("# -------------------------------")
	lines.append("@qa_list = ();")
	lines.append("@indices = ();")
	lines.append("%answer_map = ();")
	lines.append("foreach my $term (@selected_terms) {")
	lines.append("  my $descriptions_ref = $match_data{$term};")
	lines.append("  my $i = random(0, $#$descriptions_ref, 1);")
	lines.append("  my $desc = $descriptions_ref->[$i];")
	lines.append("  push @qa_list, $term, $desc;")
	lines.append("  push @indices, $i;")
	lines.append("  $answer_map{$term} = $desc;")
	lines.append("}")
	lines.append("")
	lines.append("# -------------------------------")
	lines.append("# Create match list")
	lines.append("# -------------------------------")
	lines.append("$ml = new_match_list();")
	lines.append("")
	lines.append("# -------------------------------")
	lines.append("# Override question formatting")
	lines.append("# -------------------------------")
	lines.append("sub custom_pop_up_list_print_q {")
	lines.append("    my $self = shift;")
	lines.append("    my (@questions) = @_;")
	lines.append("    my @list = @{$self->{ra_pop_up_list}};")
	lines.append("    my $out = \"\";")
	lines.append("    if ($main::displayMode =~ /^HTML/) {")
	lines.append("        my $i = 1;")
	lines.append("        foreach my $quest (@questions) {")
	lines.append("            $out .= qq!<div style=\"margin-bottom: 0.75em; white-space: nowrap;\">!")
	lines.append("                  . qq!<strong>$i.</strong>&nbsp;$quest&nbsp;!")
	lines.append("                  . pop_up_list(@list)")
	lines.append("                  . qq!</div>!;")
	lines.append("            $i++;")
	lines.append("        }")
	lines.append("    } else {")
	lines.append("        return pop_up_list_print_q($self, @questions);")
	lines.append("    }")
	lines.append("    return $out;")
	lines.append("}")
	lines.append("")
	lines.append("$ml->rf_print_q(~~&custom_pop_up_list_print_q);")
	lines.append("")
	lines.append("# -------------------------------")
	lines.append("# Override answer formatting")
	lines.append("# -------------------------------")
	lines.append("sub my_print_a {")
	lines.append("  my $self = shift;")
	lines.append("  my(@array) = @_;")
	lines.append("  my @alpha = ('A'..'Z', 'AA'..'ZZ');")
	lines.append("  my $out = \"<BLOCKQUOTE>\";")
	lines.append("  for my $i (0..$#array) {")
	lines.append("    my $letter = $alpha[$i];")
	lines.append("    my $elem = $array[$i];")
	lines.append("    $out .= \"<div style='margin-bottom: 1em;'><b>$letter.</b> $elem</div>\";")
	lines.append("  }")
	lines.append("  $out .= \"</BLOCKQUOTE>\";")
	lines.append("  return $out;")
	lines.append("}")
	lines.append("")
	lines.append("$ml->rf_print_a(~~&my_print_a);")
	lines.append("")
	lines.append("# -------------------------------")
	lines.append("# Dynamically generate popup choices (A to N)")
	lines.append("# -------------------------------")
	lines.append("my @letters = ('A' .. 'Z');")
	lines.append("my @popup_list = ('No answer', '?');")
	lines.append("for my $i (0 .. $n - 1) {")
	lines.append("  push @popup_list, $letters[$i], $letters[$i];")
	lines.append("}")
	lines.append("$ml->ra_pop_up_list([@popup_list]);")
	lines.append("")
	lines.append("# -------------------------------")
	lines.append("# Insert generated Q/A pairs")
	lines.append("# -------------------------------")
	lines.append("$ml->qa(@qa_list);")
	lines.append("$ml->choose($n);")
	lines.append("")
	lines.append("# -------------------------------")
	lines.append("# Render the question")
	lines.append("# -------------------------------")
	lines.append("BEGIN_PGML")
	lines.append(question_text)
	lines.append(note_text)
	lines.append("")
	lines.append("[@ ColumnMatchTable($ml) @]***")
	lines.append("END_PGML")
	lines.append("")
	lines.append("# -------------------------------")
	lines.append("# Dynamic Partial Credit Based on $n")
	lines.append("# -------------------------------")
	lines.append("$showPartialCorrectAnswers = 0;")
	lines.append("my @thresholds;")
	lines.append("my @scores;")
	lines.append("for (my $i = 1; $i <= $n; $i++) {")
	lines.append("  push @thresholds, $i;")
	lines.append("  push @scores, sprintf(\"%.2f\", $i / $n);")
	lines.append("}")
	lines.append("")
	lines.append("install_problem_grader(~~&custom_problem_grader_fluid);")
	lines.append("$ENV{grader_numright} = [@thresholds];")
	lines.append("$ENV{grader_scores}   = [@scores];")
	lines.append("$ENV{grader_message} = 'You can earn partial credit.';")
	lines.append("")
	lines.append("# -------------------------------")
	lines.append("# Grading")
	lines.append("# -------------------------------")
	lines.append("ANS(str_cmp($ml->ra_correct_ans));")
	lines.append("")
	lines.append("@correct      = @{ $ml->ra_correct_ans() };")
	lines.append("$answerstring = join(', ', @correct);")
	lines.append("")
	lines.append("BEGIN_PGML_SOLUTION")
	lines.append("The correct answers are [$answerstring].")
	lines.append("END_PGML_SOLUTION")
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
