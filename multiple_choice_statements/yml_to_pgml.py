#!/usr/bin/env python3
# Standard Library
import re
import pathlib
import argparse

# PIP3 modules
import yaml


#============================================
def group_statements(block: dict) -> list:
	"""
	Group truth or false statement keys into ordered groups.

	Args:
		block (dict): Mapping of statement keys to text values.

	Returns:
		list: Ordered list of grouped statement lists.
	"""
	# Build grouped statements by numeric suffix.
	grouped = {}
	for key, value in block.items():
		# Extract the digits from keys like truth3a.
		match = re.search(r"(\d+)", key)
		if match:
			group_number = int(match.group(1))
			if group_number not in grouped:
				grouped[group_number] = []
			grouped[group_number].append(value)
	# Return list ordered by group index.
	return [grouped[index] for index in sorted(grouped.keys())]


# Simple assertion test for the function: 'group_statements'
assert group_statements({"truth1a": "A", "truth1b": "B", "truth2a": "C"}) == [
	["A", "B"],
	["C"],
]


#============================================
def perl_array(name: str, groups: list) -> str:
	"""
	Convert grouped statements into Perl array syntax.

	Args:
		name (str): Target Perl array name.
		groups (list): List of grouped statement lists.

	Returns:
		str: Perl array definition string.
	"""
	# Build Perl array text.
	perl_text = f"@{name} = (\n"
	for group in groups:
		perl_text += "    [\n"
		for statement in group:
			safe = statement.replace('"', '\\"')
			perl_text += f'      "{safe}",\n'
		perl_text += "    ],\n"
	perl_text += ");\n\n"
	return perl_text


# Simple assertion test for the function: 'perl_array'
assert '@demo = (\n    [\n      "one",\n    ],\n);\n\n' in perl_array("demo", [["one"]])


#============================================
def build_pgml(topic: str, perl_true: str, perl_false: str) -> str:
	"""
	Assemble the PGML output content.

	Args:
		topic (str): Topic description for the problem.
		perl_true (str): Perl array text for true groups.
		perl_false (str): Perl array text for false groups.

	Returns:
		str: Complete PGML content.
	"""
	# Assemble PGML content with concatenation.
	pgml_content = ""
	pgml_content += "DOCUMENT();\n\n"
	pgml_content += "loadMacros(\n"
	pgml_content += '  "PGstandard.pl",\n'
	pgml_content += '  "PGML.pl",\n'
	pgml_content += '  "PGchoicemacros.pl",\n'
	pgml_content += '  "parserRadioButtons.pl",\n'
	pgml_content += ");\n\n"
	pgml_content += "TEXT(beginproblem());\n"
	pgml_content += "$showPartialCorrectAnswers = 1;\n\n"
	pgml_content += "########################################################\n"
	pgml_content += "# AUTO-GENERATED GROUPS FROM YAML\n"
	pgml_content += "########################################################\n\n"
	pgml_content += perl_true
	pgml_content += perl_false
	pgml_content += "########################################################\n"
	pgml_content += "# GLOBAL SETTINGS\n"
	pgml_content += "########################################################\n\n"
	pgml_content += f'$topic = "{topic}";\n'
	pgml_content += '$mode  = list_random("TRUE","FALSE");\n'
	pgml_content += "$num_distractors = 4;\n\n"
	pgml_content += "########################################################\n"
	pgml_content += "# SELECT GROUP\n"
	pgml_content += "########################################################\n\n"
	pgml_content += "my (@selected_group, @opposite_groups);\n\n"
	pgml_content += 'if ($mode eq "TRUE") {\n'
	pgml_content += "    $group_index      = random(0, scalar(@true_groups)-1, 1);\n"
	pgml_content += "    @selected_group   = @{ $true_groups[$group_index] };\n"
	pgml_content += "    @opposite_groups  = @false_groups;\n"
	pgml_content += "} else {\n"
	pgml_content += "    $group_index      = random(0, scalar(@false_groups)-1, 1);\n"
	pgml_content += "    @selected_group   = @{ $false_groups[$group_index] };\n"
	pgml_content += "    @opposite_groups  = @true_groups;\n"
	pgml_content += "}\n\n"
	pgml_content += "########################################################\n"
	pgml_content += "# PICK CORRECT + DISTRACTORS (MAINTAINING GROUP STRUCTURE)\n"
	pgml_content += "########################################################\n\n"
	pgml_content += "$correct = list_random(@selected_group);\n\n"
	pgml_content += "# Generate random group indices to pull distractors from\n"
	pgml_content += "my @available_group_indices = (0 .. $#opposite_groups);\n"
	pgml_content += "my @selected_distractor_indices = ();\n\n"
	pgml_content += "# Randomly select which groups to pull from (need $num_distractors groups)\n"
	pgml_content += "while (@selected_distractor_indices < $num_distractors && "
	pgml_content += "@available_group_indices > 0) {\n"
	pgml_content += "    my $random_index = random(0, scalar(@available_group_indices)-1, 1);\n"
	pgml_content += (
		"    push @selected_distractor_indices, splice(@available_group_indices, "
		"$random_index, 1);\n"
	)
	pgml_content += "}\n\n"
	pgml_content += "# Pull one random statement from each selected group\n"
	pgml_content += "@distractors = ();\n"
	pgml_content += "foreach my $group_idx (@selected_distractor_indices) {\n"
	pgml_content += "    my @group = @{ $opposite_groups[$group_idx] };\n"
	pgml_content += "    my $distractor = list_random(@group);\n"
	pgml_content += "    push @distractors, $distractor;\n"
	pgml_content += "}\n\n"
	pgml_content += "@choices = ($correct, @distractors);\n\n"
	pgml_content += "########################################################\n"
	pgml_content += "# RADIO BUTTONS WITH A/B/C/D/E LABELS\n"
	pgml_content += "########################################################\n\n"
	pgml_content += "$rb = RadioButtons(\n"
	pgml_content += "  [@choices],\n"
	pgml_content += "  $correct,\n"
	pgml_content += "  labels        => ['A','B','C','D','E'],\n"
	pgml_content += "  displayLabels => 1,\n"
	pgml_content += "  randomize     => 1,\n"
	pgml_content += "  separator     => '<div style=\"margin-bottom: 0.7em;\"></div>',\n"
	pgml_content += ");\n\n"
	pgml_content += "########################################################\n"
	pgml_content += "# PGML\n"
	pgml_content += "########################################################\n\n"
	pgml_content += "BEGIN_PGML\n\n"
	pgml_content += "Which one of the following statements is "
	pgml_content += "[@ \"<span style='font-weight: bold;'>$mode</span>\" @]* "
	pgml_content += "about [$topic]?\n\n"
	pgml_content += "[@ $rb->buttons() @]*\n\n"
	pgml_content += "END_PGML\n\n"
	pgml_content += "ANS($rb->cmp());\n\n"
	pgml_content += "ENDDOCUMENT();\n"
	return pgml_content


#============================================
def parse_args() -> argparse.Namespace:
	"""
	Parse command-line arguments.

	Returns:
		argparse.Namespace: Parsed arguments.
	"""
	# Configure CLI arguments.
	parser = argparse.ArgumentParser(
		description="Convert YAML multiple-choice statements into a PGML file."
	)
	parser.add_argument(
		"-i",
		"--input",
		dest="input_path",
		required=True,
		help="Path to the input YAML file",
	)
	parser.add_argument(
		"-o",
		"--output",
		dest="output_path",
		required=False,
		help="Path for the generated PG file",
	)
	return parser.parse_args()


#============================================
def main() -> None:
	"""
	Load YAML statements and write PGML output.
	"""
	# Parse CLI options.
	args = parse_args()
	# Resolve input path.
	yml_path = pathlib.Path(args.input_path)
	# Validate that the input exists.
	if not yml_path.exists():
		raise FileNotFoundError(f"File not found: {yml_path}")
	# Read YAML content.
	yml_text = yml_path.read_text(encoding="utf-8")
	# Parse YAML data.
	data = yaml.safe_load(yml_text)
	# Extract topic with fallback.
	topic = data.get("topic", "this topic")
	# Handle naming variations.
	true_block = data.get("true_statements", {})
	false_block = data.get("false_statements", {})
	# Convert dicts to grouped lists.
	true_groups = group_statements(true_block)
	false_groups = group_statements(false_block)
	# Convert to Perl arrays.
	perl_true = perl_array("true_groups", true_groups)
	perl_false = perl_array("false_groups", false_groups)
	# Assemble PGML content.
	pgml_template = build_pgml(topic, perl_true, perl_false)
	# Determine output path.
	output_path = (
		pathlib.Path(args.output_path)
		if args.output_path
		else yml_path.with_suffix(".pg")
	)
	# Write output file.
	output_path.write_text(pgml_template, encoding="utf-8")
	# Report generation path.
	print(f"Generated: {output_path}")


if __name__ == "__main__":
	main()
