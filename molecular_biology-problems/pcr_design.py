#!/usr/bin/env python3

import random
import seqlib
import bptools

"""
                                                3'  GGCATCGACCTCCCT  5'
5'  GGATCGATCAAGAACAATGACAGGATCGAGGAATTCAGCCTACGCAGCCCGTAGCTGGAGGGA  3'
3'  CCTAGCTAGTTCTTGTTACTGTCCTAGCTCCTTAAGTCGGATGCGTCGGGCATCGACCTCCCT  5'
5'  GGATCGATCAAGAAC  3'
"""

#=====================
#=====================
def getPrimerChoices(top_sequence, primer_len):
	bottom_sequence = seqlib.complement(top_sequence)
	primer_set = []
	
	primer = top_sequence[:primer_len]
	primer_set.append(primer) #answer1
	answer1 = primer
	primer_set.append(seqlib.flip(primer))

	primer = bottom_sequence[:primer_len]
	primer_set.append(primer)
	primer_set.append(seqlib.flip(primer))
	
	primer = top_sequence[-primer_len:]
	primer_set.append(primer)
	primer_set.append(seqlib.flip(primer))
	
	primer = bottom_sequence[-primer_len:]
	primer_set.append(primer)
	primer_set.append(seqlib.flip(primer)) #answer2
	answer2 = seqlib.flip(primer)
	
	answer_set = [answer1, answer2]
	for ans in answer_set:
		for nt in list('ACGT'):
			if not nt in ans:
				return False, answer_set

	primer_set.sort()
	print(primer_set)
	print(answer_set)

	convert_set = []
	for primer in primer_set:
		subprimer = primer.replace('T', 'A')
		convert_set.append(subprimer)
		subprimer = primer.replace('C', 'G')
		convert_set.append(subprimer)
	if len(list(set(convert_set))) < 16:
		return False, answer_set
	return primer_set, answer_set

#=====================
#=====================
def getSequence(sequence_len, primer_len):
	primer_set = False
	while primer_set is False:
		top_sequence = seqlib.makeSequence(sequence_len)
		primer_set, answer_set = getPrimerChoices(top_sequence, primer_len)
	return top_sequence, primer_set, answer_set 


#=====================
#=====================
def makeChoices(primer_set, answer_set):
	choices = set()
	choices.add(tuple(answer_set))

	wrong = (answer_set[0], seqlib.flip(answer_set[1]))
	choices.add(wrong)
	wrong = (answer_set[1], seqlib.flip(answer_set[0]))
	choices.add(wrong)
	wrong = (seqlib.flip(answer_set[0]), seqlib.flip(answer_set[1]))
	choices.add(wrong)
	
	while len(choices) < 6:
		c1 = random.choice(primer_set)
		c2 = random.choice(primer_set)
		if c1 != c2:
			choices.add((c1, c2))
	choices_list = list(choices)
	random.shuffle(choices_list)
	return choices_list


#=====================
#=====================
#=====================
#=====================
def write_question(N: int, args) -> str:
	question_text = (
		"<p>Choose the correct pair of RNA primers that will amplify the entire region of DNA "
		"shown above using PCR. The RNA primers are {0} bases in length.</p> "
		"<p>Pay close attention to the 5&prime; and 3&prime; ends of the primers.</p> "
	).format(args.primer_len)

	top_sequence, primer_set, answer_set = getSequence(args.sequence_len, args.primer_len)
	answer_tuple = tuple(answer_set)
	table = seqlib.DNA_Table(top_sequence)
	choices = makeChoices(primer_set, answer_set)

	choices_list = []
	answer_text = None
	for choice in choices:
		choice_text = '{0} AND {1}'.format(seqlib.Primer_Table(choice[0]), seqlib.Primer_Table(choice[1]))
		choices_list.append(choice_text)
		if choice == answer_tuple:
			answer_text = choice_text
	if answer_text is None:
		return None

	complete_question = bptools.formatBB_MC_Question(N, table + question_text, choices_list, answer_text)
	return complete_question

#=====================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate PCR primer design questions.")
	parser.add_argument(
		'-s', '--sequence-len', dest='sequence_len', type=int,
		default=36, help='Length of the template DNA sequence.'
	)
	parser.add_argument(
		'-p', '--primer-len', dest='primer_len', type=int,
		default=9, help='Length of each primer.'
	)
	args = parser.parse_args()
	return args

#=====================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile(None, f"{args.sequence_len}_bp", f"{args.primer_len}_primer")
	bptools.collect_and_write_questions(write_question, args, outfile)

#=====================
if __name__ == '__main__':
	main()
