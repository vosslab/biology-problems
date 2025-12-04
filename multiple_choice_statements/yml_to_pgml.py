#!/usr/bin/env python3
import sys
import yaml
import re
from pathlib import Path

def group_statements(block):
    """
    Groups truth1a, truth1b... into:
       { 1: ["statement A", "statement B"], 2: [...] }
    """
    grouped = {}

    for key, value in block.items():
        # Extract the digits from keys like truth3a → 3
        m = re.search(r'(\d+)', key)
        if not m:
            continue
        group_num = int(m.group(1))

        if group_num not in grouped:
            grouped[group_num] = []

        grouped[group_num].append(value)

    # Return list ordered by group index
    return [grouped[k] for k in sorted(grouped.keys())]


def perl_array(name, groups):
    """
    Convert Python list-of-lists into Perl array syntax.
    """
    out = f"@{name} = (\n"
    for g in groups:
        out += "    [\n"
        for stmt in g:
            safe = stmt.replace('"', '\\"')
            out += f'      "{safe}",\n'
        out += "    ],\n"
    out += ");\n\n"
    return out


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 yml_to_pgml.py input.yml")
        sys.exit(1)

    yml_path = Path(sys.argv[1])
    if not yml_path.exists():
        print("File not found:", yml_path)
        sys.exit(1)

    data = yaml.safe_load(yml_path.read_text())

    # Extract topic
    topic = data.get("topic", "this topic")

    # Handle naming variations: true_statements / false_statements
    true_block = data.get("true_statements", {})
    false_block = data.get("false_statements", {})

    # Convert dicts -> grouped lists
    true_groups = group_statements(true_block)
    false_groups = group_statements(false_block)

    # Convert to Perl arrays
    perl_true = perl_array("true_groups", true_groups)
    perl_false = perl_array("false_groups", false_groups)

    # Full PGML template with FIXED distractor selection
    pgml_template = f"""
DOCUMENT();

loadMacros(
  "PGstandard.pl",
  "PGML.pl",
  "PGchoicemacros.pl",
  "parserRadioButtons.pl",
);

TEXT(beginproblem());
$showPartialCorrectAnswers = 1;

########################################################
# AUTO-GENERATED GROUPS FROM YAML
########################################################

{perl_true}
{perl_false}

########################################################
# GLOBAL SETTINGS
########################################################

$topic = "{topic}";
$mode  = list_random("TRUE","FALSE");
$num_distractors = 4;

########################################################
# SELECT GROUP
########################################################

my (@selected_group, @opposite_groups);

if ($mode eq "TRUE") {{
    $group_index      = random(0, scalar(@true_groups)-1, 1);
    @selected_group   = @{{ $true_groups[$group_index] }};
    @opposite_groups  = @false_groups;
}} else {{
    $group_index      = random(0, scalar(@false_groups)-1, 1);
    @selected_group   = @{{ $false_groups[$group_index] }};
    @opposite_groups  = @true_groups;
}}

########################################################
# PICK CORRECT + DISTRACTORS (MAINTAINING GROUP STRUCTURE)
########################################################

$correct = list_random(@selected_group);

# Generate random group indices to pull distractors from
my @available_group_indices = (0 .. $#opposite_groups);
my @selected_distractor_indices = ();

# Randomly select which groups to pull from (need $num_distractors groups)
while (@selected_distractor_indices < $num_distractors && @available_group_indices > 0) {{
    my $random_index = random(0, scalar(@available_group_indices)-1, 1);
    push @selected_distractor_indices, splice(@available_group_indices, $random_index, 1);
}}

# Pull one random statement from each selected group
@distractors = ();
foreach my $group_idx (@selected_distractor_indices) {{
    my @group = @{{ $opposite_groups[$group_idx] }};
    my $distractor = list_random(@group);
    push @distractors, $distractor;
}}

@choices = ($correct, @distractors);

########################################################
# RADIO BUTTONS WITH A/B/C/D/E LABELS
########################################################

$rb = RadioButtons(
  [@choices],
  $correct,
  labels        => ['A','B','C','D','E'],
  displayLabels => 1,
  randomize     => 1,
  separator     => '<div style="margin-bottom: 0.7em;"></div>',
);

########################################################
# PGML
########################################################

BEGIN_PGML

Which one of the following statements is [@ "<span style='font-weight: bold;'>$mode</span>" @]* about [$topic]?

[@ $rb->buttons() @]*

END_PGML

ANS($rb->cmp());

ENDDOCUMENT();
"""

    # Write output file
    output_path = yml_path.with_suffix(".pg")
    output_path.write_text(pgml_template.strip() + "\n")

    print("Generated:", output_path)


if __name__ == "__main__":
    main()