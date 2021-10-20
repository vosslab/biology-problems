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
	big_table += '  <td bgcolor="#ecb3ff" align="center"><i>Eco</i>R1<br/>overhang</td>'
	big_table += '  <td bgcolor="#ffff99" align="center">left<br/>unknown<br/>sequence</td>'	
	big_table += '  <td bgcolor="#99ff99" align="center">central<br/>known<br/>sequence</td>'	
	big_table += '  <td bgcolor="#ffff99" align="center">right<br/>unknown<br/>sequence</td>'	
	big_table += '  <td bgcolor="#ecb3ff" align="center"><i>Eco</i>R1<br/>overhang</td>'
	big_table += '</tr>'
	big_table += '<tr>'
	big_table += '  <td bgcolor="#ecb3ff" align="left">{0}</td>'.format(
		DNA_Table(' AATTC', '     G',  left_primes=True,  right_primes=False))
	big_table += '  <td bgcolor="#ffff99" align="right">{0}</td>'.format(
		DNA_Table(sequence_tuple[0], left_primes=False, right_primes=False))
	big_table += '  <td bgcolor="#99ff99" align="center">{0}</td>'.format(
		DNA_Table(sequence_tuple[1], left_primes=False, right_primes=False))
	big_table += '  <td bgcolor="#ffff99" align="left">{0}</td>'.format(
		DNA_Table(sequence_tuple[2], left_primes=False, right_primes=False))
	big_table += '  <td bgcolor="#ecb3ff" align="left">{0}</td>'.format(
		DNA_Table('G     ', 'CTTAA ',  left_primes=False, right_primes=True ))
	big_table += '</tr>'
	big_table += '<tr>'
	big_table += '  <td bgcolor="#ecb3ff" align="center">&nbsp;</td>'	
	big_table += '  <td bgcolor="#ffff99" align="center">&nbsp;</td>'	
	big_table += '  <td bgcolor="#99ff99" align="center">&nbsp;</td>'	
	big_table += '  <td bgcolor="#ffff99" align="center">&nbsp;</td>'	
	big_table += '  <td bgcolor="#ecb3ff" align="center">&nbsp;</td>'	
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
	else:
		table += '<td>&ndash;</td>'
	for i, c in enumerate(list(top_sequence)):
		if i > 0 and i % 3 == 0:
			table += '<td>,</td> '
		table += '<td {1}>{0}</td>'.format(c, colorNucleotide(c))
	if right_primes is True:
		table += '<td>&ndash;3&prime;</td>'
	else:
		table += '<td>&ndash;</td>'
	table += '</tr>  '

	if bottom_sequence is None:
		bottom_sequence = seqlib.complement(top_sequence)
	table += '<tr>'
	if left_primes is True:
		table += '<td>3&prime;&ndash;</td>'
	else:
		table += '<td>&ndash;</td>'
	for i, c in enumerate(list(bottom_sequence)):
		if i > 0 and i % 3 == 0:
			table += '<td>,</td> '
		table += '<td {1}>{0}</td>'.format(c, colorNucleotide(c))
	if right_primes is True:
		table += '<td>&ndash;5&prime;</td>'
	else:
		table += '<td>&ndash;</td>'
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
def getInversePrimerChoices(top_sequence, primer_len):
	bottom_sequence = seqlib.complement(top_sequence)
	primer_set = []
	
	primer = top_sequence[:primer_len]
	primer_set.append(primer) 
	primer_set.append(seqlib.flip(primer)) 

	primer = bottom_sequence[:primer_len]
	primer_set.append(primer)
	primer_set.append(seqlib.flip(primer)) #answer1
	answer1 = seqlib.flip(primer)
	
	primer = top_sequence[-primer_len:]
	primer_set.append(primer)
	primer_set.append(seqlib.flip(primer))
	answer2 = primer
	
	primer = bottom_sequence[-primer_len:]
	primer_set.append(primer)  #answer2
	primer_set.append(seqlib.flip(primer)) 
	
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
def getSequence(sequence_len, primer_len):
	primer_set = False
	side_len = sequence_len//2 + 2
	side_len -= side_len%3
	while primer_set is False:
		left_top_sequence = "N" * side_len
		known_top_sequence = seqlib.makeSequence(sequence_len)
		right_top_sequence = "N" * side_len
		primer_set, answer_set = getInversePrimerChoices(known_top_sequence, primer_len)
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
	sequence_len = 15
	primer_len = 6
	num_questions = 199

	N = 0
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	for i in range(num_questions):
		N += 1
		number = "{0}. ".format(N)
		question = ("Choose the correct pair of RNA primers that will amplify the "
		+"both the known and unknown region of DNA shown above using Inverse PCR. "
		+"The RNA primers are {0} bases in length. ".format(primer_len)
		+"Pay close attention to the 5&prime; and 3&prime; ends of the primers. " )

		sequence_tuple, primer_set, answer_set = getSequence(sequence_len, primer_len)
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

