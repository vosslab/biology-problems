#!/usr/bin/env python

import time
import math
import copy
import random

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
	print('========')
	for i in range(num_sequences):
		seq = sequence_list[i]
		score = compare_sequence(consensus_sequence, seq)
		print(seq, score)
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
	print('========')
	for seq in choices:
		score = compare_sequence(consensus_sequence, seq)
		print(seq, score)
	choices = choices[:5]

	random.shuffle(choices)
	return choices

#============================
#============================
def sequence_to_table_row(seq):
	length = len(seq)
	bits = length // 3 + 1
	row = "<tr> "
	for bit in range(bits):
		row += '<td>{0}</td> '.format(seq[3*bit:3*bit + 3])
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
def make_alignment_sequences(consensus_sequence):
	sequence_list = []
	for i in range(num_sequences):
		sequence_list.append(consensus_sequence)
	#print(sequence_list)
	sequence_list = mutate_sequences(consensus_sequence, sequence_list)
	return sequence_list

#============================
#============================
def write_question(length, num_sequences):
	consensus_sequence = make_sequence(length)
	print("consensus_sequence", consensus_sequence)


	sequence_list = make_alignment_sequences(consensus_sequence)
	while consensus_sequence in sequence_list:
		print("WOAH")
		time.sleep(1)
		sequence_list = make_alignment_sequences(consensus_sequence)
	
	choices = make_choices(consensus_sequence, sequence_list)	
	print('========')
		
	question = make_question(sequence_list)
	bbtext = "MC\t{0}".format(question)
	for choice in choices:
		status = "Incorrect"
		if choice == consensus_sequence:
			status = "Correct"
		formed_choice = "<table>{0}</table> ".format(sequence_to_table_row(choice))
		bbtext += "\t{0}\t{1}".format(formed_choice, status)
	bbtext += "\n"
	return bbtext

#============================
#============================
#============================
#============================
if __name__ == '__main__':
	length = 9
	num_sequences = 4

	f = open('bbq-consensus_sequences.txt', 'w')
	for i in range(90):
		bbtext = write_question(length, num_sequences)
		f.write(bbtext)
	f.close()


		
		
		
		
		
	