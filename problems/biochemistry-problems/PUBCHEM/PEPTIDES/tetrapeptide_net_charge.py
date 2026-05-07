#!/usr/bin/env python3

# Tetrapeptide net-charge question generator (bptools / Blackboard).
# The peptide is rendered with RDKit-in-the-browser using fully NEUTRAL SMILES
# (-COOH, -NH2, neutral guanidine, neutral imidazole, etc.) so the structure
# does not give away the charge state. Students must compute the net charge
# from the printed pKa table and the labeled three-letter sequence.

# general built-in/pip libraries
import os
import sys
import random

# local libraries
import bptools


#=================================================
def get_pubchem_dir():
	git_root = bptools._get_git_root(os.path.dirname(__file__))
	if git_root is None:
		raise RuntimeError("Unable to locate git root for PubChem imports.")
	return os.path.join(git_root, 'problems', 'biochemistry-problems', 'PUBCHEM')


# Add the PUBCHEM dir to sys.path so the sibling aminoacidlib (used for
# RDKit canvas + peptide-bond highlight HTML) can be imported.
_PUBCHEM_DIR = get_pubchem_dir()
if _PUBCHEM_DIR not in sys.path:
	sys.path.insert(0, _PUBCHEM_DIR)

import aminoacidlib

# Blackboard render tweaks: HTML must reach Blackboard untouched so the
# RDKit canvas + SMILES survive. The PUBCHEM generators in this repo set
# these flags to disable bptools' anti-cheat HTML wrappers.
bptools.allow_insert_hidden_terms = False
bptools.allow_no_click_div = False
bptools.use_nocopy_script = False

# 19 standard amino acids; proline excluded because the imino N breaks the
# generic peptide-bond template.
AMINO_ACID_LETTERS = list('ACDEFGHIKLMNQRSTVWY')

# Letters whose side chains have a pKa within the 1-13 range we sweep over.
IONIZABLE_LETTERS = ('K', 'R', 'H', 'D', 'E', 'C', 'Y')

# pKa table: alpha-amino, alpha-carboxyl, and the seven ionizable side chains.
PKA_TABLE = {
	'Nterm': 9.0,
	'Cterm': 2.0,
	'K': 10.5,
	'R': 12.5,
	'H': 6.0,
	'D': 3.7,
	'E': 4.1,
	'C': 8.3,
	'Y': 10.1,
}

# 'basic' = +1 when pH < pKa (protonated). 'acidic' = -1 when pH > pKa.
GROUP_KIND = {
	'Nterm': 'basic',
	'Cterm': 'acidic',
	'K': 'basic',
	'R': 'basic',
	'H': 'basic',
	'D': 'acidic',
	'E': 'acidic',
	'C': 'acidic',
	'Y': 'acidic',
}

# Side chains in fully NEUTRAL form. No bracketed charges; no charged
# guanidine, imidazolium, alkylammonium, carboxylate, thiolate, or phenolate.
NEUTRAL_SIDE_CHAINS = {
	'Gly': '([H])',
	'Ala': '(C)',
	'Ser': '(CO)',
	'Thr': '([C@H](O)C)',
	'Asn': '(CC(=O)N)',
	'Gln': '(CCC(=O)N)',
	'Asp': '(CC(=O)O)',
	'Glu': '(CCC(=O)O)',
	'Lys': '(CCCCN)',
	'Arg': '(CCCNC(=N)N)',
	'His': '(CC1=C[NH]C=N1)',
	'Val': '(C(C)C)',
	'Leu': '(CC(C)C)',
	'Ile': '([C@H](CC)C)',
	'Met': '(CCSC)',
	'Phe': '(Cc1ccccc1)',
	'Tyr': '(Cc1ccc(O)cc1)',
	'Trp': '(CC1=CC=C2C(=C1)C(=CN2))',
	'Cys': '(CS)',
}


#=================================================
def make_neutral_generic_polypeptide(length):
	"""Build a generic polypeptide SMILES with a free amine and free COOH."""
	# Free amine N-terminus and free COOH C-terminus (no charges).
	amino_terminal_end = 'N[C@@H]'
	carboxyl_terminal_end = '(C(=O)O)'
	peptide_bond = '(C(=O)N[C@@H]'
	peptide_chain = amino_terminal_end
	for i in range(length):
		peptide_chain += f'R{i+1}'
		if i + 1 < length:
			peptide_chain += peptide_bond
	peptide_chain += carboxyl_terminal_end
	# Close one parenthesis per peptide bond.
	for _ in range(length - 1):
		peptide_chain += ')'
	return peptide_chain


#=================================================
def make_neutral_polypeptide_smiles_from_sequence(seq):
	"""Build the full neutral SMILES for a single-letter peptide sequence."""
	smiles = make_neutral_generic_polypeptide(len(seq))
	# Replace from highest index down so R10 is replaced before R1 (future
	# proofing; harmless at length 4).
	letters = list(seq.upper())
	for i in range(len(letters) - 1, -1, -1):
		three_letter = aminoacidlib.amino_acid_mapping[letters[i]]
		side_chain = NEUTRAL_SIDE_CHAINS[three_letter]
		smiles = smiles.replace(f'R{i+1}', side_chain)
	return smiles


#=================================================
def count_ionizable(seq):
	"""Count residues whose single-letter code is ionizable in pH 1-13."""
	ion = set(IONIZABLE_LETTERS)
	return sum(1 for letter in seq.upper() if letter in ion)


#=================================================
def pick_tetrapeptide_with_two_ionizable():
	"""Random tetrapeptide with at least two ionizable residues."""
	# Try random unique-letter draws first.
	for _ in range(50):
		seq = ''.join(random.sample(AMINO_ACID_LETTERS, 4))
		if count_ionizable(seq) >= 2:
			return seq
	# Fallback: inject ionizable letters at fresh positions until count >= 2.
	letters = list(seq)
	present = set(letters)
	while count_ionizable(''.join(letters)) < 2:
		pos = random.randint(0, 3)
		candidates = [L for L in IONIZABLE_LETTERS if L not in present]
		if not candidates:
			candidates = list(IONIZABLE_LETTERS)
		new_letter = random.choice(candidates)
		# Update the present set as we mutate the sequence.
		present.discard(letters[pos])
		letters[pos] = new_letter
		present.add(new_letter)
	return ''.join(letters)


#=================================================
def compute_net_charge(seq, pH):
	"""Net integer charge using the simple "fully (de)protonated" rule."""
	charge = 0
	# Termini are always present.
	if pH < PKA_TABLE['Nterm']:
		charge += 1
	if pH > PKA_TABLE['Cterm']:
		charge -= 1
	for letter in seq.upper():
		if letter not in PKA_TABLE:
			continue
		kind = GROUP_KIND[letter]
		pKa = PKA_TABLE[letter]
		if kind == 'basic' and pH < pKa:
			charge += 1
		elif kind == 'acidic' and pH > pKa:
			charge -= 1
	return charge


#=================================================
def format_signed_charge(n):
	"""Format an integer charge as +N, -N, or 0."""
	if n == 0:
		return '0'
	return f'{n:+d}'


#=================================================
def sequence_to_three_letter(seq):
	"""Convert a single-letter peptide string into "Lys-Glu-His-Ala" form."""
	parts = [aminoacidlib.amino_acid_mapping[L] for L in seq.upper()]
	return '-'.join(parts)


#=================================================
def random_pH():
	"""Pick a pH uniformly in 1.0..13.0 with one decimal place."""
	# Drawing as integer tenths makes the displayed value exact.
	pH_int = random.randint(10, 130)
	return pH_int / 10.0


#=================================================
def build_choice_pool(correct_charge):
	"""Build the 5-choice charge pool with a uniform correct-position.

	Picks a target sorted index uniformly in 0..4, then fills consecutive
	integer offsets: target_idx values strictly below correct and
	(4 - target_idx) values strictly above. Pool is always exactly 5
	choices (correct + 4 distractors). Display order is then shuffled,
	so the correct answer's sorted position is uniform across the five
	buttons and "pick the middle/edge" heuristics do not beat random.
	"""
	# Sorted-position target index in 0..4 (5 choices = A..E).
	target_idx = random.randint(0, 4)
	offsets = []
	# Distractors strictly below correct: -target_idx..-1.
	for i in range(target_idx, 0, -1):
		offsets.append(-i)
	# Distractors strictly above correct: +1..+(4 - target_idx).
	for i in range(1, 4 - target_idx + 1):
		offsets.append(i)
	pool = [correct_charge] + [correct_charge + off for off in offsets]
	random.shuffle(pool)
	return pool


#=================================================
def generate_html_content(peptide_sequence):
	"""Generate the RDKit canvas HTML using a NEUTRAL SMILES."""
	# Inject the RDKit loader (CDN script). The peptide-bond highlight JS
	# uses split-comment tokens (function/* */name) so Blackboard's HTML/JS
	# sanitizer cannot rewrite the keywords.
	html_content = aminoacidlib.generate_load_script()
	smiles = make_neutral_polypeptide_smiles_from_sequence(peptide_sequence)
	# Stable canvas id keyed off the sequence so duplicate questions get
	# distinct canvases inside one Blackboard upload.
	crc16 = bptools.getCrc16_FromString(peptide_sequence)
	molecule_name = f'tetrapeptide_{crc16}'
	html_content += aminoacidlib.generate_html_for_molecule(
		smiles, molecule_name, width=540, height=320,
	)
	return html_content


#=================================================
def build_pKa_html(sequence):
	"""Build a <ul> of pKa lines for the groups present in this peptide.

	Termini always appear. Side chains only appear when their letter is in
	the drawn sequence, so the list never reveals which ionizable residues
	the student should be looking for.
	"""
	# Termini are always present.
	lines = [
		'<li>alpha-amino group (N-terminus): 9.0</li>',
		'<li>alpha-carboxyl group (C-terminus): 2.0</li>',
	]
	seen = set(sequence.upper())
	# Stable display order for ionizable side chains.
	side_chain_order = ('K', 'R', 'H', 'D', 'E', 'C', 'Y')
	for L in side_chain_order:
		if L not in seen:
			continue
		if L not in PKA_TABLE:
			continue
		three = aminoacidlib.amino_acid_mapping[L]
		lines.append(f'<li>{three} side chain: {PKA_TABLE[L]}</li>')
	pKa_html = '<ul>' + ''.join(lines) + '</ul>'
	return pKa_html


#=================================================
def generate_question_text(sequence, three_letter_seq, pH_str):
	"""Build the question prompt HTML."""
	pKa_html = build_pKa_html(sequence)
	question_text = ''
	question_text += '<p>The tetrapeptide above is shown in its fully neutral '
	question_text += '(uncharged) drawing form. Using the approximate pKa values '
	question_text += 'below, estimate the <b>net charge</b> of this peptide at '
	question_text += f'pH <b>{pH_str}</b>.</p>'
	question_text += '<p>Sequence (N to C): '
	question_text += '<span style="font-family: monospace; font-weight: bold;">'
	question_text += f'{three_letter_seq}</span></p>'
	question_text += '<p>Approximate pKa values for the groups in this peptide:</p>'
	question_text += pKa_html
	question_text += f'<p>Select the net charge at pH {pH_str}:</p>'
	return question_text


#=================================================
def generate_complete_question(N):
	"""Generate one complete tetrapeptide net-charge question."""
	# Pick the sequence and pH.
	sequence = pick_tetrapeptide_with_two_ionizable()
	three_letter_seq = sequence_to_three_letter(sequence)
	pH = random_pH()
	pH_str = f'{pH:.1f}'

	# Compute the correct net charge and the 5-choice pool.
	correct_charge = compute_net_charge(sequence, pH)
	answer_text = format_signed_charge(correct_charge)
	charge_pool = build_choice_pool(correct_charge)
	choices_list = [format_signed_charge(c) for c in charge_pool]

	# Build the rendered structure HTML and the prompt HTML.
	html_content = generate_html_content(sequence)
	question_text = generate_question_text(sequence, three_letter_seq, pH_str)

	# Combine the rendered structure with the prompt text.
	complete_question = html_content + question_text

	bbformat = bptools.formatBB_MC_Question(
		N, complete_question, choices_list, answer_text,
	)
	return bbformat


#=================================================
def write_question(N, args):
	return generate_complete_question(N)


#=================================================
def parse_arguments():
	parser = bptools.make_arg_parser(
		description='Generate tetrapeptide net-charge questions.',
	)
	args = parser.parse_args()
	return args


#=================================================
def main():
	args = parse_arguments()
	# Hardcoded: tetrapeptide (4 residues), 5 MC choices (scantron-friendly).
	outfile = bptools.make_outfile('tetrapeptide_net_charge', '5_choices')
	bptools.collect_and_write_questions(write_question, args, outfile)


#=================================================
if __name__ == '__main__':
	main()
