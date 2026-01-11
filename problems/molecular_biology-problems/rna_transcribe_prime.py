#!/usr/bin/env python3

import random

#local
import seqlib
import bptools

def write_question(N, args):
	#============================
	#sequence is 5' -> 3'
	question_seq = seqlib.makeSequence(args.sequence_len)

	if random.randint(1,2) == 1:
		question_table = seqlib.Single_Strand_Table(question_seq, fivetothree=True)
	else:
		question_table = seqlib.Single_Strand_Table(seqlib.flip(question_seq), fivetothree=False)

	#sequence is 3' -> 5'
	answer_seq = seqlib.complement(question_seq)
	answer_mRNA = seqlib.transcribe(answer_seq)

	if random.randint(1,2) == 1:
		choice_fivetothree = True
		answer_table = seqlib.Single_Strand_Table(seqlib.flip(answer_mRNA), fivetothree=True)
	else:
		choice_fivetothree = False
		answer_table = seqlib.Single_Strand_Table(answer_mRNA, fivetothree=False)

	question_text = ''
	question_text += question_table
	question_text += '<p>Which one of the following sequences below would be the mRNA product '
	question_text += 'produced from transcription of the DNA template strand above?</p>'
	question_text += '<p>Hint: pay close attention to the 5&prime; and 3&prime; directions!</p>'

	#============================
	choice_list = []
	half = int(args.sequence_len//2)

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
		mRNA = seqlib.transcribe(choice)
		if choice_fivetothree is True:
			choice_table = seqlib.Single_Strand_Table(seqlib.flip(mRNA), fivetothree=True)
		elif choice_fivetothree is False:
			choice_table = seqlib.Single_Strand_Table(mRNA, fivetothree=False)
		choice_table_list.append(choice_table)

	#============================
	choice_table_list.append(answer_table)
	random.shuffle(choice_table_list)
	choice_table_list = list(set(choice_table_list))
	#this next line should be okay
	#since the only way to have more than 5 is if the answer is duplicated
	choice_table_list = choice_table_list[:5]
	bbformat = bptools.formatBB_MC_Question(N, question_text, choice_table_list, answer_table)
	return bbformat

#============================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate RNA transcription multiple choice questions.")
	parser.add_argument(
		'-s', '--sequence-length', dest='sequence_len',
		type=int, default=9, help='Length of the DNA sequence.'
	)
	args = parser.parse_args()
	return args


#============================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile(f"len_{args.sequence_len}")
	bptools.collect_and_write_questions(write_question, args, outfile)


#============================
if __name__ == '__main__':
	main()
