#!/usr/bin/env python3

"""
Generate a minimal PGML file with just SMILES arrays for macromolecule identification.
Creates a self-contained .pg file with only the essential data: SMILES strings organized by type.
"""

import os
import yaml

def load_yaml_file(filepath):
	"""Load and return YAML file contents."""
	with open(filepath, 'r') as f:
		return yaml.safe_load(f)

def get_molecule_type_map(macromolecules_data):
	"""
	Create a flat map of molecule_name -> macromolecule_type
	from the hierarchical macromolecules.yml structure.
	"""
	molecule_to_type = {}
	for macro_type, groups in macromolecules_data.items():
		for group_name, molecule_list in groups.items():
			for molecule_name in molecule_list:
				molecule_to_type[molecule_name.lower().strip()] = macro_type
	return molecule_to_type

def collect_smiles_by_type(pubchem_data, molecule_to_type):
	"""
	Collect SMILES strings organized by macromolecule type.
	Returns dict: {type: [smiles1, smiles2, ...]}
	"""
	smiles_by_type = {
		'proteins': [],
		'lipids': [],
		'carbohydrates': [],
		'nucleic acids': [],
	}

	cid_to_data = pubchem_data.get('cid_to_data', {})
	name_to_cid = pubchem_data.get('name_to_cid', {})

	for molecule_name, macro_type in molecule_to_type.items():
		# Look up CID
		cid = name_to_cid.get(molecule_name)
		if cid is None:
			continue

		# Get molecule data
		mol_data = cid_to_data.get(cid)
		if mol_data is None:
			continue

		# Extract SMILES
		smiles = mol_data.get('SMILES')
		if not smiles:
			continue

		smiles_by_type[macro_type].append(smiles)

	return smiles_by_type

def escape_perl_string(s):
	"""Escape special characters for Perl strings."""
	if s is None:
		return ''
	s = str(s)
	s = s.replace('\\', '\\\\')
	s = s.replace("'", "\\'")
	return s

def format_smiles_array(smiles_list):
	"""Format a list of SMILES as a Perl array."""
	escaped = [f"\t'{escape_perl_string(s)}'" for s in smiles_list]
	return ",\n".join(escaped)

def generate_pg_file(smiles_by_type, output_path):
	"""Generate the minimal .pg file with just SMILES arrays."""

	# Calculate total and type counts
	total = sum(len(v) for v in smiles_by_type.values())
	type_counts = {k: len(v) for k, v in smiles_by_type.items()}

	# Format the arrays
	proteins_array = format_smiles_array(smiles_by_type['proteins'])
	lipids_array = format_smiles_array(smiles_by_type['lipids'])
	carbohydrates_array = format_smiles_array(smiles_by_type['carbohydrates'])
	nucleic_acids_array = format_smiles_array(smiles_by_type['nucleic acids'])

	# Generate the PG file
	pg_content = f'''## DESCRIPTION
## Identify the macromolecule type from a rendered chemical structure.
## ENDDESCRIPTION
## KEYWORDS('macromolecules','structure identification','pubchem','rdkit')
## DBsubject('Biochemistry')
## DBchapter('Macromolecules')
## DBsection('Identification')
## Date('')
## Author('')
## Institution('')
## TitleText1('')
## EditionText1('')
## AuthorText1('')
## Section1('')
## Problem1('')

DOCUMENT();
loadMacros(
	"PGstandard.pl",
	"PGML.pl",
	"parserRadioButtons.pl",
);

TEXT(beginproblem());

# =============================================================================
# MOLECULE DATA - SMILES ONLY
# =============================================================================
# Total: {total} molecules
# Proteins: {type_counts['proteins']}, Lipids: {type_counts['lipids']},
# Carbohydrates: {type_counts['carbohydrates']}, Nucleic acids: {type_counts['nucleic acids']}
# =============================================================================

@proteins = (
{proteins_array}
);

@lipids = (
{lipids_array}
);

@carbohydrates = (
{carbohydrates_array}
);

@nucleic_acids = (
{nucleic_acids_array}
);

# =============================================================================
# PROBLEM SETUP
# =============================================================================

# Randomly select a macromolecule type (seed-stable)
@types = ('proteins', 'lipids', 'carbohydrates', 'nucleic acids');
my $local_random = PGrandom->new();
$local_random->srand($problemSeed);
$type_index = $local_random->random(0, 3, 1);
$selected_type = $types[$type_index];

# Get the corresponding array and select a random SMILES
if ($selected_type eq 'proteins') {{
	$mol_smiles = $proteins[$local_random->random(0, $#proteins, 1)];
	$correct_answer_plain = "Proteins (amino acids and dipeptides)";
}} elsif ($selected_type eq 'lipids') {{
	$mol_smiles = $lipids[$local_random->random(0, $#lipids, 1)];
	$correct_answer_plain = "Lipids (fatty acids)";
}} elsif ($selected_type eq 'carbohydrates') {{
	$mol_smiles = $carbohydrates[$local_random->random(0, $#carbohydrates, 1)];
	$correct_answer_plain = "Carbohydrates (monosaccharides)";
}} elsif ($selected_type eq 'nucleic acids') {{
	$mol_smiles = $nucleic_acids[$local_random->random(0, $#nucleic_acids, 1)];
	$correct_answer_plain = "Nucleic acids (nucleobases)";
}}

# Escape SMILES for HTML attribute
$mol_smiles_attr = $mol_smiles;
$mol_smiles_attr =~ s/&/&amp;/g;
$mol_smiles_attr =~ s/"/&quot;/g;
$mol_smiles_attr =~ s/</&lt;/g;
$mol_smiles_attr =~ s/>/&gt;/g;

	# Create colorized choices (HTML) with plain TeX fallbacks
	$choice_carbohydrates = MODES(
		TeX => '',
		HTML => '<strong><span style="color: #0a9bf5;">Carbohydrates</span></strong> (monosaccharides)',
	);
	$choice_lipids = MODES(
		TeX => '',
		HTML => '<strong><span style="color: #e69100;">Lipids</span></strong> (fatty acids)',
	);
	$choice_proteins = MODES(
		TeX => '',
		HTML => '<strong><span style="color: #009900;">Proteins</span></strong> (amino acids and dipeptides)',
	);
	$choice_nucleic_acids = MODES(
		TeX => '',
		HTML => '<strong><span style="color: #e60000;">Nucleic acids</span></strong> (nucleobases)',
	);

	# Map the correct answer to its colored choice
	if ($selected_type eq 'proteins') {{
		$correct_answer = $choice_proteins;
	}} elsif ($selected_type eq 'lipids') {{
		$correct_answer = $choice_lipids;
	}} elsif ($selected_type eq 'carbohydrates') {{
		$correct_answer = $choice_carbohydrates;
	}} elsif ($selected_type eq 'nucleic acids') {{
		$correct_answer = $choice_nucleic_acids;
	}}

	# Create radio buttons
	$mc = RadioButtons(
	[
		$choice_carbohydrates,
		$choice_lipids,
		$choice_proteins,
		$choice_nucleic_acids,
	],
	$correct_answer,
	randomize => 1,
	);

# Generate unique canvas ID
$canvas_id = "canvas_" . $local_random->random(10000, 99999, 1);

# =============================================================================
# HEADER: Load RDKit.js
# =============================================================================
HEADER_TEXT(<<'EOF');
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
			const mdetails = {{"explicitMethyl": true}};
			if (canvas && mol) {{
				mol.draw_to_canvas_with_highlights(canvas, JSON.stringify(mdetails));
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
EOF

# Canvas HTML (HTML-only)
$canvas_html = MODES(
	TeX => '',
	HTML => '<canvas id="' . $canvas_id . '" width="480" height="270" data-smiles="' . $mol_smiles_attr . '"></canvas>',
);

# =============================================================================
# PROBLEM TEXT
# =============================================================================

BEGIN_PGML

## Identify the Macromolecule Type

Study the chemical structure below and identify which of the four main types of macromolecules it represents.

---

[$canvas_html]*

---

Which one of the four main types of macromolecules is represented by the chemical structure shown above?

[_]{{$mc}}

END_PGML

# =============================================================================
# HINT
# =============================================================================
# Note: In ADAPT, this hint section can be replaced with ADAPT's hint system.
# For standard WeBWorK, this hint is available via the "Hint" button.
# =============================================================================

BEGIN_PGML_HINT

### Guide to Identifying Chemical Structures of Macromolecules

**Carbohydrates (monosaccharides)**
* Should have about the same number of oxygens as carbons
* Look for hydroxyl groups (–OH) attached to carbon atoms
* Carbonyl groups (C=O) are often present
* Look for the base unit of CH₂O
* Larger carbohydrates form hexagon or pentagon ring structures

**Lipids (fatty acids)**
* Contain mostly carbon and hydrogen
* Very few oxygens and often no nitrogens
* Fats and oils have carboxyl groups (–COOH) and ester bonds
* Look for long chains or ring structures of only carbon and hydrogen
* Steroids have four interconnected carbon rings

**Proteins (amino acids and dipeptides)**
* Always have a nitrogen/amino group (–NH₂ or –NH₃⁺)
* Always have a carboxyl group (–COOH or –COO⁻)
* Identify the central Cα (alpha-carbon) attached to amino and carboxyl groups
* Larger proteins have characteristic peptide bonds (C–N)
* Try to identify common side chains (R groups)

**Nucleic acids (nucleobases)**
* Must have a nucleobase: rings containing carbon and nitrogen
* Larger nucleic acids have a sugar backbone and phosphate groups

**Note:** Phosphate groups (–PO₄²⁻) can be found in all macromolecule types, so they may be confusing markers.

END_PGML_HINT

# =============================================================================
# SOLUTION
# =============================================================================

BEGIN_PGML_SOLUTION

The correct answer is [$correct_answer_plain].

END_PGML_SOLUTION

ENDDOCUMENT();
'''

	# Write to file
	with open(output_path, 'w') as f:
		f.write(pg_content)

	print(f"Generated PG file: {output_path}")
	print(f"Total molecules: {total}")
	print(f"Breakdown: {type_counts}")
	file_size = len(pg_content)
	print(f"File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")

def main():
	# Define paths
	script_dir = os.path.dirname(__file__)
	macromolecules_file = os.path.join(script_dir, 'macromolecules.yml')
	pubchem_file = os.path.join(script_dir, '../../../data/pubchem_molecules_data.yml')
	output_file = os.path.join(script_dir, 'macromolecule_identification.pg')

	print("Loading data files...")
	macromolecules_data = load_yaml_file(macromolecules_file)
	pubchem_data = load_yaml_file(pubchem_file)

	print("Building molecule type map...")
	molecule_to_type = get_molecule_type_map(macromolecules_data)
	print(f"Found {len(molecule_to_type)} molecules across 4 macromolecule types")

	print("Collecting SMILES by type...")
	smiles_by_type = collect_smiles_by_type(pubchem_data, molecule_to_type)

	print("Generating PG file...")
	generate_pg_file(smiles_by_type, output_file)

	print("\nDone!")

if __name__ == '__main__':
	main()
