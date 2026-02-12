
import random
from types import SimpleNamespace

from lib_test_utils import import_from_repo_path


def test_match_amino_acid_structures_question_text_contains_prompt():
	mod = import_from_repo_path(
		"problems/biochemistry-problems/PUBCHEM/AMINO_ACIDS/match_amino_acid_structures.py"
	)
	text = mod.get_question_text()
	assert "Match the amino acid structures" in text
	assert "Each choice will be used exactly once" in text


def test_wordle_read_wordle_filters_to_valid_words():
	mod = import_from_repo_path("problems/biochemistry-problems/PUBCHEM/PEPTIDES/wordle_peptides.py")
	words = mod.read_wordle()
	assert len(words) > 0
	valid_letters = set(mod.VALID_AMINO_ACID_LETTERS)
	assert all(len(word) == 5 and set(word) <= valid_letters for word in words)


def test_wordle_generate_question_text_mentions_wordle():
	mod = import_from_repo_path("problems/biochemistry-problems/PUBCHEM/PEPTIDES/wordle_peptides.py")
	text = mod.generate_question_text()
	assert "Wordle" in text


def test_polypeptide_sequence_is_unique_and_valid():
	mod = import_from_repo_path(
		"problems/biochemistry-problems/PUBCHEM/PEPTIDES/polypeptide_fib_sequence.py"
	)
	random.seed(0)
	seq = mod.get_peptide_sequence(5)
	assert len(seq) == 5
	assert "P" not in seq
	assert len(set(seq)) == 5


def test_polypeptide_question_text_includes_length():
	mod = import_from_repo_path(
		"problems/biochemistry-problems/PUBCHEM/PEPTIDES/polypeptide_fib_sequence.py"
	)
	text = mod.generate_question_text(3)
	assert "tripeptide" in text
	assert "three (3)" in text


def test_glycolysis_load_molecules_has_required_fields():
	mod = import_from_repo_path(
		"problems/biochemistry-problems/PUBCHEM/GLYCOLYSIS/order_glycolysis_molecules.py"
	)
	data = mod.load_molecules()
	assert isinstance(data, list)
	assert data
	for key in ("SMILES", "name", "abbreviation"):
		assert key in data[0]


def test_glycolysis_write_question_contains_prompt():
	mod = import_from_repo_path(
		"problems/biochemistry-problems/PUBCHEM/GLYCOLYSIS/order_glycolysis_molecules.py"
	)
	mod.GLOBAL_MOLECULE_DATA = mod.load_molecules()
	args = SimpleNamespace(num_choices=4)
	item = mod.write_question(1, args)
	question_text = getattr(item, "question_text", "")
	assert "Glycolysis" in question_text
	assert "metabolic pathway" in question_text


def test_macromolecule_guide_text_mentions_phosphate_groups():
	mod = import_from_repo_path(
		"problems/biochemistry-problems/PUBCHEM/MACROMOLECULE_CATEGORIZE/which_macromolecule.py"
	)
	text = mod.get_guide_text()
	assert "Phosphate groups" in text


def test_macromolecule_load_molecules_has_expected_group():
	mod = import_from_repo_path(
		"problems/biochemistry-problems/PUBCHEM/MACROMOLECULE_CATEGORIZE/which_macromolecule.py"
	)
	data = mod.load_molecules()
	assert "carbohydrates" in data
