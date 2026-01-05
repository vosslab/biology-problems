#!/usr/bin/env python3

import random

import bptools
import seqlib

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
def prime_answer_sequence(question_seq):
	return seqlib.reverse_complement(question_seq)

#============================
#============================
def prime_fib_answers(answer_seq):
	answer1 = answer_seq
	answer1c = seqlib.insertCommas(answer1)
	answer2 = "5'-{0}-3'".format(answer1)
	answer2c = "5'-{0}-3'".format(answer1c)
	answer3 = "5&prime;-{0}-3&prime;".format(answer1)
	answer3c = "5&prime;-{0}-3&prime;".format(answer1c)
	answers_list = [answer1, answer2, answer1c, answer2c, answer3, answer3c]
	return answers_list

#============================
#============================
def write_prime_fib_question(N, seqlen):
	#============================
	question_seq = seqlib.makeSequence(seqlen)
	answer_seq = prime_answer_sequence(question_seq)
	if random.randint(1,2) == 1:
		question_table = seqlib.Single_Strand_Table(question_seq, fivetothree=True)
	else:
		question_table = seqlib.Single_Strand_Table(seqlib.flip(question_seq), fivetothree=False)

	question_text = dna_complement_context()
	question_text += question_table
	question_text += "<h5>Determine the complementary DNA sequence for the DNA strand above.</h5>"
	question_text += "<p>Hint: pay close attention to the 5&prime; and 3&prime; directions of the strand.</p>"
	question_text += "<p><i>Include a comma after every 3 letters, but avoid extra commas or spaces.</i></p>"
	question_text += "<p>Write your answer in the 5&prime; -> 3&prime; direction only.</p>"

	#============================
	answers_list = prime_fib_answers(answer_seq)

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

	answer_seq = prime_answer_sequence(question_seq)
	if choice_fivetothree is True:
		answer_table = seqlib.Single_Strand_Table(answer_seq, True)
	else:
		answer_table = seqlib.Single_Strand_Table(seqlib.flip(answer_seq), False)

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
		if choice_fivetothree is True:
			display_choice = choice
		else:
			display_choice = seqlib.flip(choice)
		choice_table = seqlib.Single_Strand_Table(display_choice, choice_fivetothree)
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
def write_question(N, args):
	return choose_question(N, args.seqlen, args.question_type, args.direction_mode)

#============================
#============================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate complementary sequence questions.")
	parser = bptools.add_question_format_args(
		parser,
		types_list=['mc', 'fib'],
		required=False,
		default='mc'
	)

	direction_group = parser.add_mutually_exclusive_group(required=False)
	direction_group.add_argument('--direction', dest='direction_mode', type=str,
		choices=('directionless', 'prime'),
		help="Set the sequence direction: 'directionless' or 'prime' for 5' and 3' ends.")
	direction_group.add_argument('--directionless', dest='direction_mode',
		action='store_const', const='directionless',
		help="Set the sequence direction to 'directionless'.")
	direction_group.add_argument('--prime', dest='direction_mode', action='store_const',
		const='prime', help="Set the sequence direction to 'prime' for 5' and 3' ends.")
	parser.set_defaults(direction_mode='directionless')

	parser.add_argument('-s', '--seqlen', dest='seqlen', type=int, default=9,
		help='Set the length of the sequence. Default is 9.')

	args = parser.parse_args()
	return args

#============================
#============================
def main():
	args = parse_arguments()

	if args.seqlen > 18:
		raise ValueError(f"Sequence length too long: {args.seqlen}")

	outfile = bptools.make_outfile(args.question_type, args.direction_mode)
	bptools.collect_and_write_questions(write_question, args, outfile)

#============================
#============================
if __name__ == '__main__':
	main()
