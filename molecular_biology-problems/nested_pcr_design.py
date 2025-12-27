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
def BIG_Table(sequence_tuple):
	big_table = '<table style="border-collapse: collapse; border: 1px solid silver;"> '
	big_table += '<tr>'
	big_table += '  <td align="right">{0}</td>'.format(
		seqlib.DNA_Table(sequence_tuple[0], left_primes=True, right_primes=False))
	big_table += '  <td>&nbsp;</td>'
	big_table += '  <td align="center">{0}</td>'.format(
		seqlib.DNA_Table(sequence_tuple[1], left_primes=False, right_primes=False))
	big_table += '  <td>&nbsp;</td>'
	big_table += '  <td align="left">{0}</td>'.format(
		seqlib.DNA_Table(sequence_tuple[2], left_primes=False, right_primes=True))
	big_table += '</tr>'
	big_table += '</table>'
	return big_table

#=====================
#=====================
def getPrimerChoices(top_sequence, primer_len):
	bottom_sequence = seqlib.complement(top_sequence)
	primer_set = []
	
	primer = top_sequence[:primer_len]
	primer_set.append(primer) 
	primer_set.append(seqlib.flip(primer)) 
	answer1 = primer

	primer = bottom_sequence[:primer_len]
	primer_set.append(primer)
	primer_set.append(seqlib.flip(primer)) #answer1
	
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
def getSequence(sequence_len, round1_primer_len, round2_primer_len):
	primer_set = False
	side_len = round1_primer_len
	while primer_set is False:
		left_top_sequence = seqlib.makeSequence(side_len)
		known_top_sequence = seqlib.makeSequence(sequence_len)
		right_top_sequence = seqlib.makeSequence(side_len)
		primer_set, answer_set = getPrimerChoices(known_top_sequence, round2_primer_len)
		sequence_tuple = (left_top_sequence, known_top_sequence, right_top_sequence)
	return sequence_tuple, primer_set, answer_set 

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
def write_question(N, args):
	sequence_tuple, primer_set, answer_set = getSequence(
		args.sequence_len,
		args.round1_primer_len,
		args.round2_primer_len
	)
	old_primer1 = sequence_tuple[0]
	old_primer2 = seqlib.flip(seqlib.complement(sequence_tuple[2]))

	question = (
		"<p>The amplicon sequence of DNA shown above was replicated using 30 cycles of PCR, "
		+ "using the primers 5&prime;-{0}-3&prime; and 5&prime;-{1}-3&prime;.</p>".format(
			old_primer1, old_primer2
		)
		+ "<p>But the first PCR run contained significant contamination due to mispriming. "
		+ "Probably from using too short of primers "
		+ f"that were only {args.round1_primer_len} nucleotide in length.</p>"
		+ "<p>Choose the correct pair of RNA primers that will amplify the remaining region of DNA "
		+ "inside the old primers using <strong>nested PCR</strong>. "
		+ f"The nested RNA primers are {args.round2_primer_len} bases in length.</p>"
		+ "<p>Pay close attention to the 5&prime; and 3&prime; ends of the primers.</p>"
	)

	answer_tuple = tuple(answer_set)
	table = BIG_Table(sequence_tuple)
	choices = makeChoices(primer_set, answer_set)

	choice_tables = []
	answer_text = None
	for choice in choices:
		choice_text = '{0} AND {1}'.format(
			seqlib.Primer_Table(choice[0]),
			seqlib.Primer_Table(choice[1])
		)
		choice_tables.append(choice_text)
		if choice == answer_tuple:
			answer_text = choice_text
	if answer_text is None:
		return None
	bb_question = bptools.formatBB_MC_Question(N, table + question, choice_tables, answer_text)
	return bb_question


#=====================
def apply_difficulty_defaults(args):
	presets = {
		'easy': {
			'sequence_len': 18,
			'round1_primer_len': 6,
			'round2_primer_len': 5,
		},
		'medium': {
			'sequence_len': 24,
			'round1_primer_len': 6,
			'round2_primer_len': 6,
		},
		'rigorous': {
			'sequence_len': 30,
			'round1_primer_len': 7,
			'round2_primer_len': 7,
		},
	}
	preset = presets.get(args.difficulty, presets['medium'])

	if args.sequence_len is None:
		args.sequence_len = preset['sequence_len']
	if args.round1_primer_len is None:
		args.round1_primer_len = preset['round1_primer_len']
	if args.round2_primer_len is None:
		args.round2_primer_len = preset['round2_primer_len']

	return args


#=====================
def parse_arguments():
	parser = bptools.make_arg_parser(description="Generate nested PCR primer questions.")
	parser = bptools.add_difficulty_args(parser)
	parser.add_argument(
		'-s', '--sequence-length', type=int, dest='sequence_len',
		default=None, help='Length of the known sequence.'
	)
	parser.add_argument(
		'-p', '--round1-primer-length', type=int, dest='round1_primer_len',
		default=None, help='Length of the round 1 primers.'
	)
	parser.add_argument(
		'-q', '--round2-primer-length', type=int, dest='round2_primer_len',
		default=None, help='Length of the round 2 primers.'
	)
	args = parser.parse_args()
	args = apply_difficulty_defaults(args)
	return args


#=====================
def main():
	args = parse_arguments()
	outfile = bptools.make_outfile(__file__, f"len_{args.sequence_len}")
	bptools.collect_and_write_questions(write_question, args, outfile)


#=====================
if __name__ == '__main__':
	main()
