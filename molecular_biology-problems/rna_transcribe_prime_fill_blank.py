#!/usr/bin/env python3

import random
import seqlib
import bptools

def write_question(N, args):
	#============================
	seq = seqlib.makeSequence(args.sequence_len)
	
	#============================
	question = "<p>What is the transcribed RNA sequence to the "
	if random.random() < 0.5:
		table = seqlib.Single_Strand_Table(seq, fivetothree=True)
		dirseq = "5'-{0}-3'".format(seq)
		question += "DNA non-template/coding strand sequence {0} ?</p>".format(seqlib.html_monospace(dirseq))
		answer1 = seqlib.transcribe(seq)
	else:
		table = seqlib.Single_Strand_Table(seq, fivetothree=False)
		dirseq = "3'-{0}-5'".format(seq)
		question += "DNA template strand sequence {0} ?</p>".format(seqlib.html_monospace(dirseq))
		answer1 = seqlib.transcribe(seqlib.complement(seq))
	question = table + question

	question += "<p><i> you may include a comma every 3 letters, but "
	question += "do NOT include any extra commas or spaces in your answer. </i></p>"

	question += "<p>Write your nucleotide sequence only in the 5&prime; -> 3&prime; direction</p>"

	answer1c = seqlib.insertCommas(answer1)
	answer2 = "5'-{0}-3'".format(answer1)
	answer2c = "5'-{0}-3'".format(answer1c)
	answer3 = "5&prime;-{0}-3&prime;".format(answer1)
	answer3c = "5&prime;-{0}-3&prime;".format(answer1c)
	
	answers_list = [answer1, answer2, answer1c, answer2c]
	
	question = bptools.formatBB_FIB_Question(N, question, answers_list)
	return question


#============================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate RNA transcription fill-in-blank questions.")
	parser.add_argument(
		'-s', '--sequence-length', dest='sequence_len',
		type=int, default=9, help='Length of the DNA sequence.'
	)
	args = parser.parse_args()
	return args


#============================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile(__file__, f"len_{args.sequence_len}")
	bptools.collect_and_write_questions(write_question, args, outfile)


#============================
if __name__ == '__main__':
	main()
