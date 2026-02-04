#!/usr/bin/env python3

import os
import sys
import yaml

import bptools

def get_pubchem_dir():
	git_root = bptools._get_git_root(os.path.dirname(__file__))
	if git_root is None:
		raise RuntimeError("Unable to locate git root for PubChem imports.")
	return os.path.join(git_root, 'problems', 'biochemistry-problems', 'PUBCHEM')


_PUBCHEM_DIR = get_pubchem_dir()
if _PUBCHEM_DIR not in sys.path:
	sys.path.insert(0, _PUBCHEM_DIR)

import pubchemlib

DEFAULT_CHOICES_FILE = "amino_acid_distractors.yml"
OUTPUT_FILE = "alpha_amino_acid_identification.pg"


#======================================
#======================================
def escape_pg_string(value: str) -> str:
	"""Escape backslashes and single quotes for PG single-quoted strings."""
	return value.replace("\\", "\\\\").replace("'", "\\'")


#======================================
#======================================
def load_choices(input_yaml_file: str) -> dict[str, dict]:
	"""Load alpha/distractor sets from YAML."""
	with open(input_yaml_file, "r") as file:
		data = yaml.safe_load(file)
	sets = data.get("amino_acid_sets", {})
	if not isinstance(sets, dict) or len(sets) == 0:
		raise ValueError("No amino_acid_sets found in the choice YAML.")
	for name, entry in sets.items():
		alpha_name = entry.get("alpha")
		distractors = entry.get("distractors", [])
		if not alpha_name:
			raise ValueError(f"Missing alpha entry for {name}.")
		if not isinstance(distractors, list) or len(distractors) < 3:
			raise ValueError(f"Need at least three distractors for {name}.")
	return sets


#======================================
#======================================
def build_pg_entries(names: list[str], pcl: pubchemlib.PubChemLib) -> list[str]:
	entries = []
	for name in names:
		molecule_data = pcl.get_molecule_data_dict(name)
		if molecule_data is None:
			raise ValueError(f"PubChem lookup failed for {name}")
		smiles = molecule_data.get("SMILES")
		if smiles is None:
			raise ValueError(f"Missing SMILES for {name}")
		entry = (
			"\t{ "
			f"name => '{escape_pg_string(name)}', "
			f"smiles => '{escape_pg_string(smiles)}' "
			"},"
		)
		entries.append(entry)
	return entries


#======================================
#======================================
def build_pg_file(sets_blob: str) -> str:
	return f"""## TITLE('Biochemistry: Identify an Alpha Amino Acid')
## DESCRIPTION
## Identify which structure is an alpha-amino acid based on PubChem-derived structures.
## ENDDESCRIPTION
## KEYWORDS('amino acids','alpha amino acid','pubchem','structure')
## DBsubject('Biochemistry')
## DBchapter('Macromolecules')
## DBsection('Amino Acids')
## Level(3)
## Date('2026-02-03')
## Author('Dr. Neil R. Voss')
## Institution('Roosevelt University')
## Language(en)
# https://github.com/vosslab
# This work is licensed under CC BY 4.0 (Creative Commons Attribution 4.0
# International License).
# https://creativecommons.org/licenses/by/4.0/
# Source code portions are licensed under LGPLv3.
#
# Generated from {DEFAULT_CHOICES_FILE} by generate_alpha_amino_acid_identification_pg.py

DOCUMENT();

# ----------------------------
# 1) Preamble
# ----------------------------
loadMacros(
	"PGstandard.pl",
	"PGML.pl",
	"PGcourse.pl",
);

$showPartialCorrectAnswers = 0;

# ----------------------------
# 2) Setup
# ----------------------------

@amino_acid_sets = (
{sets_blob}
);

@numerals = ("I", "II", "III", "IV");

my $set_index = random(0, $#amino_acid_sets, 1);
my $set_ref = $amino_acid_sets[$set_index];
my $alpha_ref = $set_ref->{{alpha}};
my @distractors = @{{ $set_ref->{{distractors}} }};
my %seen = ();
my @non_indices = ();
while (scalar(@non_indices) < 3) {{
	my $index = random(0, $#distractors, 1);
	next if $seen{{$index}};
	$seen{{$index}} = 1;
	push @non_indices, $index;
}}

@selected = (
	{{ %{{ $alpha_ref }}, is_alpha => 1 }},
	{{ %{{ $distractors[$non_indices[0]] }}, is_alpha => 0 }},
	{{ %{{ $distractors[$non_indices[1]] }}, is_alpha => 0 }},
	{{ %{{ $distractors[$non_indices[2]] }}, is_alpha => 0 }},
);

# Shuffle selected options.
@shuffled = ();
@temp_opts = @selected;
while (@temp_opts) {{
	my $index = random(0, $#temp_opts, 1);
	push @shuffled, splice(@temp_opts, $index, 1);
}}

@cards = ();
$correct_label = '';
for my $idx (0 .. $#shuffled) {{
	my $opt = $shuffled[$idx];
	my $numeral = $numerals[$idx];
	my $canvas_id = "canvas_alpha_" . ($idx + 1);
	my $canvas_html = '<canvas id="' . $canvas_id . '" width="260" height="200" data-smiles="' . $opt->{{smiles}} . '"></canvas>';
	my $card_html = '<div style="border: 1px solid #ddd; border-radius: 8px; padding: 0.9em; margin-bottom: 1em;">'
		. '<div style="display: flex; align-items: center; gap: 1em;">'
		. '<div style="font-weight: 700; font-size: 1.1em; width: 2.2em;">' . $numeral . '</div>'
		. '<div style="flex-shrink: 0;">' . $canvas_html . '</div>'
		. '<div style="flex-grow: 1;">'
		. '<label style="display: flex; align-items: center; gap: 0.5em; font-size: 1.05em; cursor: pointer;">'
		. '<input type="radio" name="alpha_choice" value="' . $numeral . '" style="width: 20px; height: 20px; cursor: pointer;">'
		. '<span><strong>Select this structure</strong></span></label>'
		. '</div></div></div>';
	push @cards, $card_html;
	if ($opt->{{is_alpha}}) {{
		$correct_label = $numeral;
	}}
}}

# ----------------------------
# 2b) Header (RDKit)
# ----------------------------

HEADER_TEXT(<<'END_HEADER');
<script src="https://unpkg.com/@rdkit/rdkit/dist/RDKit_minimal.js"></script>
<script>
let RDKitReady = null;
function getRDKit() {{
	if (!RDKitReady) {{
		RDKitReady = initRDKitModule();
	}}
	return RDKitReady;
}}
function initMoleculeCanvases() {{
	getRDKit().then(function(RDKit) {{
		const canvases = document.querySelectorAll('canvas[data-smiles]');
		canvases.forEach((canvas) => {{
			const smiles = canvas.dataset.smiles;
			if (!smiles) {{
				return;
			}}
			const mol = RDKit.get_mol(smiles);
			const mdetails = {{
				"legend": "",
				"explicitMethyl": true,
				"addAtomIndices": false,
				"addBondIndices": false
			}};
			if (canvas && mol) {{
				mol.draw_to_canvas_with_highlights(canvas, JSON.stringify(mdetails));
				mol.delete();
			}}
		}});
	}}).catch(error => {{
		console.error('Error initializing RDKit:', error);
	}});
}}
if (document.readyState === 'loading') {{
	document.addEventListener('DOMContentLoaded', initMoleculeCanvases);
}} else {{
	initMoleculeCanvases();
}}
</script>
END_HEADER

# ----------------------------
# 3) Statement (PGML)
# ----------------------------

$alpha_emph = "<span style='color:#0066cc;font-weight:700;'>&alpha;-amino acid</span>";

BEGIN_PGML
Which of the following (I, II, III, IV) is an [$alpha_emph]*?

Select one answer.
END_PGML

BEGIN_TEXT
$PAR
\\{{ MODES(HTML => $cards[0], TeX => '') }}
$PAR
\\{{ MODES(HTML => $cards[1], TeX => '') }}
$PAR
\\{{ MODES(HTML => $cards[2], TeX => '') }}
$PAR
\\{{ MODES(HTML => $cards[3], TeX => '') }}
$PAR
$BR
\\{{ MODES(HTML => '<div style="display:none;">' . ans_rule(20) . '</div>', TeX => '') }}
END_TEXT

HEADER_TEXT(<<'END_SYNC');
<script>
document.addEventListener('DOMContentLoaded', function() {{
	const answerInput = document.querySelector('input[name="AnSwEr0001"]');
	if (!answerInput) return;

	const customRadios = document.querySelectorAll('input[name="alpha_choice"]');
	customRadios.forEach(function(radio) {{
		radio.addEventListener('change', function() {{
			if (this.checked) {{
				answerInput.value = this.value;
			}}
		}});

		if (answerInput.value === radio.value) {{
			radio.checked = true;
		}}
	}});
}});
</script>
END_SYNC

ANS(str_cmp($correct_label));

# ----------------------------
# 4) Solution
# ----------------------------

BEGIN_PGML_SOLUTION
**Solution:**

The correct choice is **[$correct_label]**.

An alpha-amino acid has the amino group on the alpha carbon adjacent to the
carboxyl group. The other choices place the amine farther away or omit the
carboxyl group, so they are not alpha-amino acids.
END_PGML_SOLUTION

ENDDOCUMENT();
"""


#======================================
#======================================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate the alpha amino acid PG file.")
	parser.add_argument(
		'-f', '-y', '--file', metavar='<file>', type=str, dest='input_yaml_file',
		help='YAML file with alpha and distractor lists'
	)
	args = parser.parse_args()
	return args


#======================================
#======================================
def main():
	args = parse_arguments()
	if args.input_yaml_file is None:
		args.input_yaml_file = os.path.join(os.path.dirname(__file__), DEFAULT_CHOICES_FILE)
	sets = load_choices(args.input_yaml_file)

	pcl = pubchemlib.PubChemLib()
	set_entries = []
	for set_name in sorted(sets.keys()):
		entry = sets[set_name]
		alpha_name = entry.get("alpha")
		distractors = list(entry.get("distractors", []))
		alpha_entries = build_pg_entries([alpha_name], pcl)
		distractor_entries = build_pg_entries(distractors, pcl)
		set_entry = (
			"\t{ "
			f"name => '{escape_pg_string(set_name)}', "
			f"alpha => {alpha_entries[0].strip().rstrip(',')}, "
			f"distractors => [\n{chr(10).join(distractor_entries)}\n\t] "
			"},"
		)
		set_entries.append(set_entry)
	pcl.close()

	sets_blob = "\n".join(set_entries)
	pg_text = build_pg_file(sets_blob)
	output_path = os.path.join(os.path.dirname(__file__), OUTPUT_FILE)
	with open(output_path, "w") as file:
		file.write(pg_text)
	print(f"Wrote {output_path}")


#======================================
#======================================
if __name__ == "__main__":
	main()
