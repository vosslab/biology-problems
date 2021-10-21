#!/usr/bin/env python

import os
import random
import seqlib

"""
                                                3'  GGCATCGACCTCCCT  5'
5'  GGATCGATCAAGAACAATGACAGGATCGAGGAATTCAGCCTACGCAGCCCGTAGCTGGAGGGA  3'
3'  CCTAGCTAGTTCTTGTTACTGTCCTAGCTCCTTAAGTCGGATGCGTCGGGCATCGACCTCCCT  5'
5'  GGATCGATCAAGAAC  3'
"""

#=====================
#=====================
def colorNucleotide(nt):
	adenine = ' bgcolor="#e6ffe6"' #green
	cytosine = ' bgcolor="#e6f3ff"' #blue
	thymine = ' bgcolor="#ffe6e6"' #red
	guanine = ' bgcolor="#f2f2f2"' #black
	uracil = ' bgcolor="#f3e6ff"' #purple
	if nt == 'A':
		return adenine
	elif nt == 'C':
		return cytosine
	elif nt == 'G':
		return guanine
	elif nt == 'T':
		return thymine
	elif nt == 'U':
		return thymine
	return ''


#=====================
#=====================
def BIG_Table(sequence_tuple):
	big_table = '<table style="border-collapse: collapse; border: 1px solid silver;"> '
	big_table += '<tr>'
	big_table += '  <td align="right">{0}</td>'.format(
		DNA_Table(sequence_tuple[0], left_primes=True, right_primes=False))
	big_table += '  <td>&nbsp;</td>'
	big_table += '  <td align="center">{0}</td>'.format(
		DNA_Table(sequence_tuple[1], left_primes=False, right_primes=False))
	big_table += '  <td>&nbsp;</td>'
	big_table += '  <td align="left">{0}</td>'.format(
		DNA_Table(sequence_tuple[2], left_primes=False, right_primes=True))
	big_table += '</tr>'
	big_table += '</table>'
	return big_table

#=====================
#=====================
def DNA_Table(top_sequence, bottom_sequence=None, left_primes=True, right_primes=True):
	table = '<table style="border-collapse: collapse; border: 1px solid silver;"> '

	table += '<tr>'
	if left_primes is True:
		table += '<td>5&prime;&ndash;</td>'
	for i, c in enumerate(list(top_sequence)):
		if i > 0 and i % 3 == 0:
			table += '<td>,</td> '
		table += '<td {1}>{0}</td>'.format(c, colorNucleotide(c))
	if right_primes is True:
		table += '<td>&ndash;3&prime;</td>'
	table += '</tr>  '

	if bottom_sequence is None:
		bottom_sequence = seqlib.complement(top_sequence)
	table += '<tr>'
	if left_primes is True:
		table += '<td>3&prime;&ndash;</td>'
	for i, c in enumerate(list(bottom_sequence)):
		if i > 0 and i % 3 == 0:
			table += '<td>,</td> '
		table += '<td {1}>{0}</td>'.format(c, colorNucleotide(c))
	if right_primes is True:
		table += '<td>&ndash;5&prime;</td>'
	table += '</tr>  '
	table += '</table>'
	return table

#=====================
#=====================
def Primer_Table(primer):
	table = '<table style="border-collapse: collapse; border: 0px; display:inline-table"> '

	table += '<tr>'
	table += '<td>5&prime;&ndash;</td>'
	rna_list = list(seqlib.transcribe(primer))
	for i, c in enumerate(rna_list):
		if i > 0 and i % 3 == 0:
			table += '<td>,</td> '
		table += '<td {1}>{0}</td>'.format(c, colorNucleotide(c))
	table += '<td>&ndash;3&prime;</td>'
	table += '</tr>  '

	table += '</table>'
	return table

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
	print(primer_set)
	print(answer_set)

	convert_set = []
	for primer in primer_set:
		subprimer = primer.replace('T', 'A')
		convert_set.append(subprimer)
		subprimer = primer.replace('C', 'G')
		convert_set.append(subprimer)
	if len(list(set(convert_set))) < 16:
		print("BAD PRIMERS")
		#sys.exit(1)
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
	print(choices_list)
	random.shuffle(choices_list)
	return choices_list


#=====================
#=====================
#=====================
#=====================
if __name__ == '__main__':
	sequence_len = 24
	round1_primer_len = 6
	round2_primer_len = 6
	num_questions = 199

	N = 0
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	for i in range(num_questions):
		N += 1
		number = "{0}. ".format(N)
		sequence_tuple, primer_set, answer_set = getSequence(sequence_len, round1_primer_len, round2_primer_len)
		old_primer1 = sequence_tuple[0]
		old_primer2 = seqlib.flip(seqlib.complement(sequence_tuple[2]))

		question = ("<p>The amplicon sequence of DNA shown above was replicated using 30 cycles of PCR, "
		+"using the primers 5&prime;-{0}-3&prime; and 5&prime;-{1}-3&prime;.</p>".format(old_primer1, old_primer2)
		+"<p>But the first PCR run contained significant contamination due to mispriming. "
		+"Probably from using too short of primers "
		+"that were only {0} nucleotide in length.</p>".format(round1_primer_len)
		+"<p>Choose the correct pair of RNA primers that will amplify the remaining region of DNA "
		+"inside the old primers using nested PCR. "
		+"The nested RNA primers are {0} bases in length.</p>".format(round2_primer_len)
		+"<p>Pay close attention to the 5&prime; and 3&prime; ends of the primers.</p>" )

		answer_tuple = tuple(answer_set)
		table = BIG_Table(sequence_tuple)
		choices = makeChoices(primer_set, answer_set)

		top_sequence = sequence_tuple[0] + "-" + sequence_tuple[1] + "-" + sequence_tuple[2]
		bottom_sequence = seqlib.complement(top_sequence)
		
		f.write("MC\t{0}\t".format(number + table + question))
		print("5'-" + top_sequence + "-3'")
		print("3'-" + bottom_sequence + "-5'")
		print("{0}. {1}".format(N, question))

		letters = "ABCDEF"
		for i, choice in enumerate(choices):
			f.write('{0} AND {1}\t'.format(Primer_Table(choice[0]), Primer_Table(choice[1])))
			if choice == answer_tuple:
				prefix = 'x'
				f.write('Correct\t')
			else:
				prefix = ' '
				f.write('Incorrect\t')
			print("- [{0}] {1}. 5'-{2}-3' AND 5'-{3}-3'".format(prefix, letters[i], choice[0], choice[1]))
		print("")
		f.write('\n')
	f.close()

