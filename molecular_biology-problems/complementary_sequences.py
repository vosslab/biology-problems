#!/usr/bin/env python3

import os
import sys
import random
import argparse

#local
import seqlib
import bptools

#============================
#============================
#============================
def dna_complement_context():
	# Initialize an empty string to store the context information
	context_str = "<p>"

	# Add information about DNA being a double helix and the anti-parallel nature of the strands
	context_str += ("DNA is organized as a double helix where two strands "
					"run in opposite, or anti-parallel, directions. ")

	# Add information about the 5' and 3' ends of DNA strands
	context_str += ("The ends of these strands are referred to as 5&prime; "
					"(five prime) and 3&prime; (three prime) ends. ")

	# Add information about the base pairing rules and the type of bond formed
	context_str += ("The strands are held together by hydrogen bonds between "
					"complementary base pairs. ")

	# Add specific information about which bases pair with each other with color
	context_str += ('Specifically, <span style="color: darkgreen;"><strong>adenine (A)</strong>'
		'</span> forms a pair with <span style="color: darkred;"><strong>thymine (T)</strong>'
		'</span>, and <span style="color: dimgray;"><strong>guanine (G)</strong></span> '
		'pairs with <span style="color: darkblue;"><strong>cytosine (C)</strong></span>. ')

	# Add a note about the importance of the correct pairing for the stability of the DNA structure
	context_str += ("This base pairing is critical for the stability of the "
					"DNA molecule and is central to processes like DNA replication and transcription.")

	context_str += "</p><br/>"

	# Return the complete context string
	return context_str


#============================
#============================
#============================
def write_directionless_fib_question(N, seqlen):
	#============================
	question_seq = seqlib.makeSequence(seqlen)
	answer_seq = seqlib.complement(question_seq)
	question_table = seqlib.Single_Strand_Table_No_Primes(question_seq)
	#============================

	question_text = dna_complement_context()
	question_text += question_table
	question_text += "<h5>Find the complementary DNA sequence to the given direction-less DNA sequence above.</h5>"
	question_text += "<p><i>You can include a comma after every 3 letters. Do not add extra commas or spaces.</i></p>"

	answers_list = []
	answers_list.append(answer_seq)
	answers_list.append(seqlib.flip(answer_seq))
	answers_list.append(seqlib.insertCommas(answer_seq))
	answers_list.append(seqlib.insertCommas(seqlib.flip(answer_seq)))

	#============================
	bbformat = bptools.formatBB_FIB_Question(N, question_text, answers_list)
	return bbformat

#============================
#============================
#============================
def write_directionless_mc_question(N, seqlen):
	#============================
	question_seq = seqlib.makeSequence(seqlen)
	answer_seq = seqlib.complement(question_seq)
	question_table = seqlib.Single_Strand_Table_No_Primes(question_seq)
	#============================

	question_text = dna_complement_context()
	question_text += question_table
	question_text += "<h5>Which one of the following DNA sequences is complementary to the direction-less DNA sequence shown above?</h5>"

	#============================
	choice_list = []
	half = int(seqlen//2)

	#choice 1
	choice_list.append(answer_seq)
	answer_table = seqlib.Single_Strand_Table_No_Primes(answer_seq)
	#choice 2
	choice_list.append(seqlib.flip(question_seq))

	extra_choices = []
	extra_choices.append(answer_seq[:half] + question_seq[half:])
	extra_choices.append(question_seq[:half] + answer_seq[half:])
	extra_choices.append(seqlib.flip(question_seq[:half]) + question_seq[half:])
	extra_choices.append(question_seq[:half] + seqlib.flip(question_seq[half:]))
	extra_choices.append(seqlib.flip(answer_seq[:half]) + answer_seq[half:])
	extra_choices.append(answer_seq[:half] + seqlib.flip(answer_seq[half:]))
	extra_choices.append(answer_seq[:half] + seqlib.flip(question_seq[half:]))
	random.shuffle(extra_choices)
	extra_choices = list(set(extra_choices))
	random.shuffle(extra_choices)

	while(len(choice_list) < 5 and len(extra_choices) > 0):
		random.shuffle(extra_choices)
		test_seq = extra_choices.pop()
		if not test_seq in choice_list:
			choice_list.append(test_seq)

	choice_table_list = []
	for choice in choice_list:
		choice_table = seqlib.Single_Strand_Table_No_Primes(choice)
		choice_table_list.append(choice_table)

	#============================
	random.shuffle(choice_table_list)
	bbformat = bptools.formatBB_MC_Question(N, question_text, choice_table_list, answer_table)
	return bbformat

#============================
#============================
#============================
def write_prime_fib_question(N, seqlen):
	#============================
	question_seq = seqlib.makeSequence(seqlen)
	answer_seq = seqlib.complement(question_seq)
	if random.randint(1,2) == 1:
		question_table = seqlib.Single_Strand_Table(question_seq, fivetothree=False)
	else:
		question_table = seqlib.Single_Strand_Table(seqlib.flip(question_seq), fivetothree=True)

	question_text = dna_complement_context()
	question_text += question_table
	question_text += "<h5>Determine the complementary DNA sequence for the DNA strand above.</h5>"
	question_text += "<p>Hint: pay close attention to the 5&prime; and 3&prime; directions of the strand.</p>"
	question_text += "<p><i>Include a comma after every 3 letters, but avoid extra commas or spaces.</i></p>"
	question_text += "<p>Write your answer in the 5&prime; -> 3&prime; direction only.</p>"

	#============================
	answer1 = answer_seq
	answer1c = seqlib.insertCommas(answer1)
	answer2 = "5'-{0}-3'".format(answer1)
	answer2c = "5'-{0}-3'".format(answer1c)
	answer3 = "5&prime;-{0}-3&prime;".format(answer1)
	answer3c = "5&prime;-{0}-3&prime;".format(answer1c)

	answers_list = [answer1, answer2, answer1c, answer2c, answer3, answer3c]

	bbformat = bptools.formatBB_FIB_Question(N, question_text, answers_list)
	return bbformat

#============================
#============================
#============================
def write_prime_mc_question(N, seqlen):
	#============================
	question_seq = seqlib.makeSequence(seqlen)
	#sequence will be 5' -> 3'
	if random.randint(1,2) == 1:
		question_table = seqlib.Single_Strand_Table(question_seq)
	else:
		question_table = seqlib.Single_Strand_Table(seqlib.flip(question_seq), fivetothree=False)

	#sequence will be 5' -> 3'
	#answer_seq = seqlib.complement(question_seq)

	if random.randint(1,2) == 1:
		choice_fivetothree = True
	else:
		choice_fivetothree = False

	answer_seq = seqlib.complement(question_seq)
	answer_table = seqlib.Single_Strand_Table(answer_seq, choice_fivetothree)

	question_text = dna_complement_context()
	question_text += question_table
	question_text += '<h5>Which one of the following sequences below is complementary to '
	question_text += 'the DNA sequence shown above?</h5>'
	question_text += "<p>Hint: pay close attention to the 5&prime; and 3&prime; directions of the strand.</p>"

	#============================
	choice_list = []
	half = int(seqlen//2)

	#choice 1
	choice_list.append(question_seq)
	#choice 2
	choice_list.append(seqlib.flip(question_seq))
	#choice 3
	choice_list.append(answer_seq)
	#choice 4
	choice_list.append(seqlib.flip(answer_seq))
	#choice 5
	nube = question_seq[:half] + answer_seq[half:]
	choice_list.append(nube)

	choice_table_list = []
	for choice in choice_list:
		choice_table = seqlib.Single_Strand_Table(choice, choice_fivetothree)
		choice_table_list.append(choice_table)

	#============================
	random.shuffle(choice_table_list)
	bbformat = bptools.formatBB_MC_Question(N, question_text, choice_table_list, answer_table)
	return bbformat

#============================
#============================
#============================
def choose_question(N, seqlen, question_type, direction_mode):
	if direction_mode == "directionless":
		if question_type == 'fib':
			return write_directionless_fib_question(N, seqlen)
		elif question_type == 'mc':
			return write_directionless_mc_question(N, seqlen)
	elif direction_mode == "prime":
		if question_type == 'fib':
			return write_prime_fib_question(N, seqlen)
		elif question_type == 'mc':
			return write_prime_mc_question(N, seqlen)
	print(f"question_type={question_type}")
	print(f"direction_mode={direction_mode}")
	raise ValueError("Invalid direction_mode or question_type.")

#============================
#============================
#============================
if __name__ == '__main__':
	# Initialize the argparse object with a description
	parser = argparse.ArgumentParser(
		description="A script to set sequence length and number of sequences.")

	# Create a mutually exclusive group for question types
	question_group = parser.add_mutually_exclusive_group(required=True)
	# Add question type argument with choices
	question_group.add_argument('-q', '--question-type', dest='question_type', type=str,
		choices=('mc', 'fib'),
		help='Set the question type: multiple choice (mc) or fill-in-the-blank (fib).')
	# Add flags for multiple-choice and fill-in-the-blank question types
	question_group.add_argument('--mc', dest='question_type', action='store_const', const='mc',
		help='Set question type to multiple choice.')
	question_group.add_argument('--fib', dest='question_type', action='store_const', const='fib',
		help='Set question type to fill-in-the-blank.')

	# Create a mutually exclusive group for direction modes
	direction_group = parser.add_mutually_exclusive_group(required=True)
	# Add direction argument with choices
	direction_group.add_argument('-d', '--direction', dest='direction_mode', type=str,
		choices=('directionless', 'prime'),
		help="Set the sequence direction: 'directionless' or 'prime' for 5' and 3' ends.")
	# Quick flags for direction mode
	direction_group.add_argument('--none', '--directionless', dest='direction_mode',
		action='store_const', const='directionless',
		help="Set the sequence direction to 'directionless'.")
	direction_group.add_argument('--prime', dest='direction_mode', action='store_const',
		const='prime', help="Set the sequence direction to 'prime' for 5' and 3' ends.")

	# Add other individual arguments here
	parser.add_argument('-s', '--seqlen', dest='seqlen', type=int, default=9,
		help='Set the length of the sequence. Default is 9.')
	parser.add_argument('-n', '--num-sequences', dest='num_sequences', type=int, default=24,
		help='Set the number of sequences. Default is 24.')

	# Parse the command-line arguments
	args = parser.parse_args()

	#===========================
	# Check for Invalid Inputs
	#===========================
	# Check if the sequence length is too long
	if args.seqlen > 18:
		print('sequence length too long', args.seqlen)
		sys.exit(1)

	#=====================
	# Main Processing
	#=====================
	# Generate output file name
	outfile = ('bbq-'
		+ os.path.splitext(os.path.basename(__file__))[0]
		+ "-" + args.question_type
		+ "-" + args.direction_mode
		+ '-questions.txt')
	print('writing to file: ' + outfile)

	# Open output file for writing using 'with' statement
	with open(outfile, 'w') as f:
		# Loop to write questions based on parsed arguments
		for i in range(args.num_sequences):
			N = i + 1
			bbformat = choose_question(N, args.seqlen, args.question_type, args.direction_mode)
			f.write(bbformat)

	# Print histogram (assumed to be a function in bptools)
	bptools.print_histogram()
