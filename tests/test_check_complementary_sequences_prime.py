import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SEQ_DIR = os.path.join(ROOT_DIR, 'problems', 'molecular_biology-problems')
if SEQ_DIR not in sys.path:
	sys.path.insert(0, SEQ_DIR)

import seqlib
import complementary_sequences


def run_checks():
	seq = 'ATGCCG'
	expected = seqlib.reverse_complement(seq)
	assert expected == 'CGGCAT'
	assert complementary_sequences.prime_answer_sequence(seq) == expected

	answers_list = complementary_sequences.prime_fib_answers(expected)
	assert expected in answers_list
	assert "5'-{0}-3'".format(expected) in answers_list
	assert "5&prime;-{0}-3&prime;".format(expected) in answers_list

	answer_table_five = seqlib.Single_Strand_Table(expected, True)
	assert "<!-- {0} -->".format(expected) in answer_table_five

	answer_table_three = seqlib.Single_Strand_Table(seqlib.flip(expected), False)
	assert "<!-- {0} -->".format(seqlib.flip(expected)) in answer_table_three


def test_mc_writers_use_choice_count(monkeypatch):
	sequence = 'ACGTCAGTA'
	monkeypatch.setattr(
		complementary_sequences.seqlib, 'makeSequence', lambda seqlen: sequence
	)

	def fake_format(N, question_text, choices_list, answer_text):
		assert answer_text in choices_list
		return len(choices_list)

	monkeypatch.setattr(
		complementary_sequences.bptools, 'formatBB_MC_Question', fake_format
	)

	for writer in (
		complementary_sequences.write_directionless_mc_question,
		complementary_sequences.write_prime_mc_question,
	):
		assert writer(1, len(sequence), 3) == 3
		assert writer(1, len(sequence)) == 5


def test_num_choices_cli_default_and_option(monkeypatch):
	monkeypatch.setattr(
		sys, 'argv', ['complementary_sequences.py', '--mc', '--num-choices', '3']
	)
	assert complementary_sequences.parse_arguments().num_choices == 3

	monkeypatch.setattr(sys, 'argv', ['complementary_sequences.py', '--mc'])
	assert complementary_sequences.parse_arguments().num_choices == 5


if __name__ == '__main__':
	run_checks()
	print('prime complement checks passed')
