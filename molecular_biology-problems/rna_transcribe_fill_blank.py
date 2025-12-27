#!/usr/bin/env python3

import bptools
import seqlib


def addTextPrimes(my_str):
	return "5'-" + my_str + "-3'"


def write_question(N, args):
	question_base = ''
	question_base += '<p>Enter the sequence for the mRNA product in the 5&prime; to 3&prime; direction '
	question_base += 'produced from transcription of the DNA template strand above.</p>'
	question_base += "<p><i> you may include a comma every 3 letters, but "
	question_base += "do NOT include any extra commas or spaces in your answer. </i>"
	question_base += "<br/> <i> also do NOT include the 5' and 3' in your answer. </i></p>"

	question_seq = seqlib.makeSequence(args.seqlen)
	question_table = seqlib.Single_Strand_Table(question_seq, fivetothree=False)

	answer_seq = seqlib.transcribe(seqlib.complement(question_seq))
	comma_seq = seqlib.insertCommas(answer_seq)
	answers_list = [answer_seq, addTextPrimes(answer_seq)]
	answers_list += [comma_seq, addTextPrimes(comma_seq)]

	question_text = question_table + question_base
	bbformat = bptools.formatBB_FIB_Question(N, question_text, answers_list)
	return bbformat


def parse_arguments():
	parser = bptools.make_arg_parser(description='Generate RNA transcription FIB questions.')
	parser.add_argument('-s', '--seqlen', dest='seqlen', type=int, default=9,
		help='Set the length of the sequence. Default is 9.')
	args = parser.parse_args()
	return args


def main():
	args = parse_arguments()
	outfile = bptools.make_outfile()
	bptools.collect_and_write_questions(write_question, args, outfile)


if __name__ == '__main__':
	main()
