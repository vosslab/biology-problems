
import random

from lib_test_utils import import_from_repo_path


def test_wordle_read_wordle_filters_to_valid_words():
	mod = import_from_repo_path("problems/biochemistry-problems/PUBCHEM/PEPTIDES/wordle_peptides.py")
	words = mod.read_wordle()
	assert len(words) > 0
	valid_letters = set(mod.VALID_AMINO_ACID_LETTERS)
	assert all(len(word) == 5 and set(word) <= valid_letters for word in words)


def test_polypeptide_sequence_is_unique_and_valid():
	mod = import_from_repo_path(
		"problems/biochemistry-problems/PUBCHEM/PEPTIDES/polypeptide_fib_sequence.py"
	)
	random.seed(0)
	seq = mod.get_peptide_sequence(5)
	assert len(seq) == 5
	assert "P" not in seq
	assert len(set(seq)) == 5
