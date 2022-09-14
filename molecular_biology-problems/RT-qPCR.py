#!/usr/bin/env python3

import os
import random
import seqlib

raw_table = """
<table border="1" style="border-collapse: collapse;">
<tbody>
<tr>
<td rowspan="2" style="width: 20%; text-align: center; vertical-align: middle;">&nbsp;</td>
<td colspan="2" style="width: 40%; text-align: center; background-color: #ecf0f1; vertical-align: middle;"><strong>Untreated Cells</strong></td>
<td colspan="2" style="width: 40%; text-align: center; background-color: #ecf0f1; vertical-align: middle;"><strong>Cells Treated with Experimental Drug</strong></td>
</tr>
<tr>
<td style="width: 20%; text-align: center; background-color: #ecf0f1; vertical-align: middle;"><strong>House Keeping Gene</strong></td>
<td style="width: 20%; text-align: center; background-color: #ecf0f1; vertical-align: middle;"><strong>Gene of Interest</strong></td>
<td style="width: 20%; text-align: center; background-color: #ecf0f1; vertical-align: middle;"><strong>House Keeping Gene</strong></td>
<td style="width: 20%; text-align: center; background-color: #ecf0f1; vertical-align: middle;"><strong>Gene of Interest</strong></td>
</tr>
<tr>
<td style="width: 20%; text-align: center; background-color: #ecf0f1; vertical-align: middle;"><strong>Well 1</strong></td>
<td style="width: 20%; text-align: right; vertical-align: middle;">w1</td>
<td style="width: 20%; text-align: right; vertical-align: middle;">x1</td>
<td style="width: 20%; text-align: right; vertical-align: middle;">y1</td>
<td style="width: 20%; text-align: right; vertical-align: middle;">z1</td>
</tr>
<tr>
<td style="width: 20%; text-align: center; background-color: #ecf0f1; vertical-align: middle;"><strong>Well 2</strong></td>
<td style="width: 20%; text-align: right; vertical-align: middle;">w2</td>
<td style="width: 20%; text-align: right; vertical-align: middle;">x2</td>
<td style="width: 20%; text-align: right; vertical-align: middle;">y2</td>
<td style="width: 20%; text-align: right; vertical-align: middle;">z2</td>
</tr>
<tr>
<td style="width: 20%; text-align: center; background-color: #ecf0f1; vertical-align: middle;"><strong>Well 3</strong></td>
<td style="width: 20%; text-align: right; vertical-align: middle;">w3</td>
<td style="width: 20%; text-align: right; vertical-align: middle;">x3</td>
<td style="width: 20%; text-align: right; vertical-align: middle;">y3</td>
<td style="width: 20%; text-align: right; vertical-align: middle;">z3</td>
</tr>
<tr>
<td style="width: 20%; text-align: center; background-color: #ecf0f1; vertical-align: middle;"><strong>mean Ct</strong></td>
<td style="width: 20%; text-align: right; background-color: #ced4d9; vertical-align: middle;">mean1</td>
<td style="width: 20%; text-align: right; background-color: #ced4d9; vertical-align: middle;">mean2</td>
<td style="width: 20%; text-align: right; background-color: #ced4d9; vertical-align: middle;">mean3</td>
<td style="width: 20%; text-align: right; background-color: #ced4d9; vertical-align: middle;">mean4</td>
</tr>
<tr>
<td style="width: 20%; text-align: center; background-color: #ecf0f1; vertical-align: middle;"><strong>&Delta;Ct</strong></td>
<td colspan="2" style="width: 40%; text-align: center; vertical-align: middle;">&nbsp;</td>
<td colspan="2" style="width: 40%; text-align: center; vertical-align: middle;">&nbsp;</td>
</tr>
<tr>
<td style="width: 20%; text-align: center; background-color: #ecf0f1; vertical-align: middle;"><strong>&Delta;&Delta;Ct</strong></td>
<td colspan="4" style="width: 80%; text-align: center; vertical-align: middle;">&nbsp;</td>
</tr>
</tbody>
</table>
"""


def makeDataTable():
	return "x"


def makeCompleteQuestion():
	table = makeDataTable()
	question = "<p>Given the data in the table above calculate the fold change (2<sup>|&Delta;&Delta;Ct|</sup>) value for the effect of the drug on the cells.</p>"
	bb_format = 'NUM\t' + table + question
	max_power = 3
	answer_choices = []
	for n in range(-max_power, max_power+1):
		if n != 0:
			answer_choices.append(2**n)
	answer = random.choice(answer_choices)
	print(answer_choices)
	tolerance = 0.01
	return bb_format

#=====================
#=====================
#=====================
#=====================
if __name__ == '__main__':
	sequence_len = 36
	primer_len = 9
	num_questions = 199
	makeCompleteQuestion()
	sys.exit(1)
	N = 0
	outfile = 'bbq-' + os.path.splitext(os.path.basename(__file__))[0] + '-questions.txt'
	print('writing to file: '+outfile)
	f = open(outfile, 'w')
	for i in range(num_questions):
		N += 1
		number = "{0}. ".format(N)
		#header = "{0} primer design".format(N)
		question = ("<p>Choose the correct pair of RNA primers that will amplify the entire region of DNA shown above using PCR. "
		+"The RNA primers are {0} bases in length.</p> ".format(primer_len)
		+"<p>Pay close attention to the 5&prime; and 3&prime; ends of the primers.</p> " )

		top_sequence, primer_set, answer_set = getSequence(sequence_len, primer_len)
		answer_tuple = tuple(answer_set)
		table = seqlib.DNA_Table(top_sequence)
		choices = makeChoices(primer_set, answer_set)

		bottom_sequence = seqlib.complement(top_sequence)
		f.write("MC\t{0}\t".format(number + table + question))
		print("5'-" + top_sequence + "-3'")
		print("3'-" + bottom_sequence + "-5'")
		print("{0}. {1}".format(N, question))

		letters = "ABCDEF"
		for i, choice in enumerate(choices):
			f.write('{0} AND {1}\t'.format(seqlib.Primer_Table(choice[0]), seqlib.Primer_Table(choice[1])))
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
