import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SEQ_DIR = os.path.join(ROOT_DIR, 'molecular_biology-problems')
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


if __name__ == '__main__':
	run_checks()
	print('prime complement checks passed')
