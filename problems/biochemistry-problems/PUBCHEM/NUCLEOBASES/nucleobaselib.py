"""Helper library for nucleobase matching problems (purines and pyrimidines).

Provides the canonical and non-canonical base lists used by the
match_purine_structures and match_pyrimidine_structures problems.
Names are lowercase PubChem lookup keys (pubchemlib.get_cid lowercases
internally), and each has an entry in data/pubchem_molecules_data.yml.
"""

# Standard Library
import random

# ==== canonical bases (matched answers) ====
canonical_purines = [
	'adenine',
	'guanine',
]

canonical_pyrimidines = [
	'cytosine',
	'thymine',
	'uracil',
]

# ==== non-canonical bases (distractor pool) ====
# isoguanine is an alternative base; 7-methylguanine is a modified base.
noncanonical_purines = [
	'isoguanine',
	'7-methylguanine',
]

# 5-methylcytosine and 5-hydroxymethylcytosine are epigenetic modifications;
# dihydrouracil is a reduction product seen in tRNA and uracil catabolism.
noncanonical_pyrimidines = [
	'5-methylcytosine',
	'5-hydroxymethylcytosine',
	'dihydrouracil',
]

# Inline SMILES from data/pubchem_molecules_data.yml. Kept here so the
# PGML generator Python counterparts (BBQ scripts) can look up SMILES
# without going through PubChemLib when a quick reference is needed.
nucleobase_smiles = {
	'adenine':                 'C1=NC2=NC=NC(=C2N1)N',
	'guanine':                 'C1=NC2=C(N1)C(=O)NC(=N2)N',
	'isoguanine':              'C1=NC2=NC(=O)NC(=C2N1)N',
	'7-methylguanine':         'CN1C=NC2=C1C(=O)NC(=N2)N',
	'cytosine':                'C1=C(NC(=O)N=C1)N',
	'thymine':                 'CC1=CNC(=O)NC1=O',
	'uracil':                  'C1=CNC(=O)NC1=O',
	'5-methylcytosine':        'CC1=C(NC(=O)N=C1)N',
	'5-hydroxymethylcytosine': 'C1=NC(=O)NC(=C1CO)N',
	'dihydrouracil':           'C1CNC(=O)NC1=O',
}


#======================================
#======================================
def pick_distractor(base_class: str, rng: random.Random) -> str:
	"""Return one non-canonical base name from the given class.

	Args:
		base_class: 'purine' or 'pyrimidine'.
		rng: a seeded random.Random instance for deterministic selection.

	Returns:
		A single non-canonical base name.
	"""
	if base_class == 'purine':
		pool = sorted(noncanonical_purines)
	elif base_class == 'pyrimidine':
		pool = sorted(noncanonical_pyrimidines)
	else:
		raise ValueError(f"Unknown base_class '{base_class}'; expected 'purine' or 'pyrimidine'.")
	return rng.choice(pool)


#======================================
#======================================
def build_question_names(base_class: str, distractor_name: str) -> list:
	"""Return the full name list for a question: canonicals + one distractor.

	Args:
		base_class: 'purine' or 'pyrimidine'.
		distractor_name: the non-canonical base name to add.

	Returns:
		A new list containing the canonical names followed by the distractor.
	"""
	if base_class == 'purine':
		names = list(canonical_purines)
	elif base_class == 'pyrimidine':
		names = list(canonical_pyrimidines)
	else:
		raise ValueError(f"Unknown base_class '{base_class}'; expected 'purine' or 'pyrimidine'.")
	names.append(distractor_name)
	return names
