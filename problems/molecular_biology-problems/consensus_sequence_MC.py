#!/usr/bin/env python3

import copy
import random
import seqlib
import bptools

dna_letters = ['A', 'C', 'G', 'T']

#============================
#============================
def make_sequence(length=9):
	sequence = ""
	for i in range(length):
		sequence += random.choice(dna_letters)
	return sequence

#============================
#============================
def compare_sequence(seq1, seq2):
	list1 = list(seq1)
	list2 = list(seq2)
	matches = 0
	for i in range(len(list1)):
		if list1[i] == list2[i]:
			matches += 1
	return matches

#============================
#============================
def mutate_sequences(consensus_sequence, sequence_list):
	length = len(consensus_sequence)
	num_sequences = len(sequence_list)
	for i in range(1, length):
		current_letter = consensus_sequence[i]
		other_letters = copy.copy(dna_letters)

		other_letters.remove(current_letter)
		letter1 = random.choice(other_letters)
		seq_num = random.randint(1,num_sequences) - 1
		seq = list(sequence_list[seq_num])
		seq[i] = letter1
		sequence_list[seq_num] = ''.join(seq)
	
		other_letters.remove(letter1)
		letter2 = random.choice(other_letters)
		seq_num = random.randint(1,num_sequences) - 1
		seq = list(sequence_list[seq_num])
		seq[i] = letter2
		sequence_list[seq_num] = ''.join(seq)
		#print(other_letters)
	return sequence_list

#============================
#============================
def make_choices(consensus_sequence, sequence_list):
	length = len(consensus_sequence)
	num_sequences = len(sequence_list)
	scores = {}
	max_score = 0
	wrong_choices = []
	for i in range(num_sequences):
		seq = sequence_list[i]
		score = compare_sequence(consensus_sequence, seq)
		if score > max_score and score != length:
			max_score = score
		scores[seq] = score

	for i in range(num_sequences):
		seq = sequence_list[i]
		score = scores[seq]
		if score == max_score:
			wrong_choices.append(seq)

	wrong_choices = list(set(wrong_choices))

	if len(wrong_choices) >= 3:
		random.shuffle(wrong_choices)
		wrong_choices = wrong_choices[:2]

	for i in range(5):
		new_choice = ""
		num_bits = length // 3 + 1
		for bit in range(num_bits):
			seq_num = random.randint(1,num_sequences) - 1
			new_choice += sequence_list[seq_num][3*bit:3*bit + 3]
		#print(new_choice)
		wrong_choices.append(new_choice)

	choices = wrong_choices
	choices.insert(0, consensus_sequence)
	#print(choices)

	choices = list(set(choices))
	choices = sorted(choices, key=lambda k: -compare_sequence(k, consensus_sequence))
	choices = choices[:5]

	random.shuffle(choices)
	return choices

#============================
#============================
def sequence_to_table_row(seq):
	#length = len(seq)
	#bits = length // 3 + 1
	row = "<tr> "
	row += seqlib.makeHtmlTDRow(seq)
	row += "</tr> "
	return row

#============================
#============================
def make_question(sequence_list):
	question_text = "<p>What would be the consensus sequence for the following aligned sequences?</p> "
	question_text += "<table><tbody> "
	for seq in sequence_list:
		question_text += sequence_to_table_row(seq)
	question_text += "</tbody></table> "
	return question_text

#============================
#============================
def make_alignment_sequences(consensus_sequence, num_sequences):
	sequence_list = []
	for i in range(num_sequences):
		sequence_list.append(consensus_sequence)
	#print(sequence_list)
	sequence_list = mutate_sequences(consensus_sequence, sequence_list)
	return sequence_list

#============================
#============================
def write_question(N, args):
	consensus_sequence = make_sequence(args.length)
	sequence_list = make_alignment_sequences(consensus_sequence, args.num_sequences)
	while consensus_sequence in sequence_list:
		sequence_list = make_alignment_sequences(consensus_sequence, args.num_sequences)
	choices = make_choices(consensus_sequence, sequence_list)
	question = make_question(sequence_list)

	choices_list = []
	for choice in choices:
		formed_choice = "<table>{0}</table> ".format(sequence_to_table_row(choice))
		choices_list.append(formed_choice)

	answer_text = "<table>{0}</table> ".format(sequence_to_table_row(consensus_sequence))
	bbtext = bptools.formatBB_MC_Question(N, question, choices_list, answer_text)
	return bbtext

#============================
#============================
#============================
#============================
def parse_arguments():
	parser = bptools.make_arg_parser(description='Generate consensus sequence questions.')
	parser.add_argument('-l', '--length', type=int, dest='length', default=9,
		help='Length of the aligned sequences.')
	parser.add_argument('-n', '--num-sequences', type=int, dest='num_sequences', default=4,
		help='Number of aligned sequences to show.')
	args = parser.parse_args()
	return args

#============================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)

#============================
if __name__ == '__main__':
	main()
		
	
