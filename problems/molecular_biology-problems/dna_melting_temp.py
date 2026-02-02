#!/usr/bin/env python3

import random
import seqlib

"""
give the user four different primers and have them choose which one has the lowest/highest melting temp
"""
import bptools

SCENARIOS: list[str] = []

#=====================
#=====================
def makeSequence(sequence_len, num_at_bases):
	sequence = []
	for i in range(sequence_len - num_at_bases):
		sequence.append(random.choice(('G', 'C')))
	for i in range(num_at_bases):
		sequence.append(random.choice(('A', 'T')))
	seq_text = ''.join(sequence)
	loop_count = 0
	while 'CCC' in seq_text or 'GGG' in seq_text or 'AAA' in seq_text or 'TTT' in seq_text:
		loop_count += 1
		random.shuffle(sequence)
		seq_text = ''.join(sequence)
		if loop_count > 20:
			break
	seq_text = ''.join(sequence)
	return seq_text

#=====================
#=====================
def makeChoices(sequence_len, answer_num_at_bases):
	answer = makeSequence(sequence_len, answer_num_at_bases + random.randint(-1,1))
	wrong_num_at_bases = sequence_len - answer_num_at_bases
	wrong1 = makeSequence(sequence_len, wrong_num_at_bases)
	wrong2 = makeSequence(sequence_len, wrong_num_at_bases+1)
	wrong3 = makeSequence(sequence_len, wrong_num_at_bases-1)
	choices_list = [answer, wrong1, wrong2, wrong3]
	random.shuffle(choices_list)
	return choices_list, answer

#=====================
def make_question(question_num, question_type, sequence_len, num_off_bases):
	question = (
		"Which one of the following DNA sequences below will have the "
		+ "<strong>{0}</strong> melting point (T<sub>m</sub>).".format(
			question_type.upper()
		)
	)
	question += '<p><i>Hint: I tried to make this question pretty easy and it does not require a calculator.</i></p>'

	if question_type == 'highest':
		answer_num_at_bases = num_off_bases
	elif question_type == 'lowest':
		answer_num_at_bases = sequence_len - num_off_bases
	else:
		return None

	choices_list, answer = makeChoices(sequence_len, answer_num_at_bases)
	table_list = [seqlib.DNA_Table(choice_seq) for choice_seq in choices_list]
	answer_table = seqlib.DNA_Table(answer)
	bb_question = bptools.formatBB_MC_Question(question_num, question, table_list, answer_table)
	return bb_question


#=====================
def write_question_batch(start_num, args):
	if len(SCENARIOS) == 0:
		return []

	questions = []

	remaining = None
	if args.max_questions is not None:
		remaining = args.max_questions - (start_num - 1)
		if remaining <= 0:
			return questions
	batch_size = len(SCENARIOS) if remaining is None else min(len(SCENARIOS), remaining)

	for offset in range(batch_size):
		question_num = start_num + offset
		idx = (question_num - 1) % len(SCENARIOS)
		question_type = SCENARIOS[idx]

		question = make_question(
			question_num,
			question_type,
			args.sequence_len,
			args.num_off_bases
		)
		if question is None:
			continue
		questions.append(question)
	return questions


#=====================
#=====================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate DNA melting temperature questions.", batch=True)
	parser = bptools.add_scenario_args(parser)
	parser.add_argument(
		'-s', '--sequence-length', type=int, dest='sequence_len',
		default=12, help='Length of each DNA sequence.'
	)
	parser.add_argument(
		'-o', '--num-off-bases', type=int, dest='num_off_bases',
		default=3, help='Number of off bases to bias the correct answer.'
	)
	args = parser.parse_args()
	return args


#=====================
def main():
	global SCENARIOS

	args = parse_arguments()
	outfile = bptools.make_outfile(f"len_{args.sequence_len}")

	SCENARIOS = ['highest', 'lowest']
	if args.scenario_order == 'sorted':
		SCENARIOS.sort()
	else:
		random.shuffle(SCENARIOS)
	if args.max_questions is None or args.max_questions > len(SCENARIOS):
		args.max_questions = len(SCENARIOS)

	questions = bptools.collect_question_batches(write_question_batch, args)
	bptools.write_questions_to_file(questions, outfile)


#=====================
if __name__ == '__main__':
	main()
